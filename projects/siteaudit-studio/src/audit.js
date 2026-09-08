import * as cheerio from 'cheerio';
import { fetchSafe, headSafe, parseTargetUrl } from './network.js';

const MAX_CRAWL_PAGES = 10;
const MAX_LINK_PROBES = 18;
const SEVERITY_WEIGHT = { critical: 22, error: 12, warning: 5, info: 0 };
const cleanText = (value) => String(value || '').replace(/\s+/g, ' ').trim();
const uniq = (values) => [...new Set(values.filter(Boolean))];

function normalizeLink(href, base) {
  const raw = String(href || '').trim();
  if (!raw || raw.startsWith('#') || /^(mailto:|tel:|javascript:|data:)/i.test(raw)) return null;
  try { const url = new URL(raw, base); if (!['http:', 'https:'].includes(url.protocol)) return null; url.hash = ''; return url.toString(); }
  catch { return null; }
}

export function analyzeHtml(html, pageUrl) {
  const $ = cheerio.load(html || '');
  const title = cleanText($('title').first().text());
  const description = cleanText($('meta[name="description" i]').attr('content'));
  const canonicalRaw = $('link[rel="canonical" i]').first().attr('href');
  const canonical = canonicalRaw ? normalizeLink(canonicalRaw, pageUrl) : null;
  const robots = cleanText($('meta[name="robots" i]').attr('content')).toLowerCase();
  const h1 = $('h1').map((_, el) => cleanText($(el).text())).get().filter(Boolean);
  const links = uniq($('a[href]').map((_, el) => normalizeLink($(el).attr('href'), pageUrl)).get());
  const images = $('img');
  let missingAlt = 0;
  images.each((_, el) => { if ($(el).attr('alt') === undefined) missingAlt += 1; });
  const origin = new URL(pageUrl).origin;
  return {
    title, titleLength: title.length, description, descriptionLength: description.length, canonical, robots,
    noindex: /(^|[,\s])noindex([,\s]|$)/i.test(robots), h1, h1Count: h1.length, h2Count: $('h2').length,
    htmlLang: cleanText($('html').attr('lang')), hasViewport: Boolean($('meta[name="viewport" i]').attr('content')),
    links, internalLinks: links.filter((link) => new URL(link).origin === origin), externalLinks: links.filter((link) => new URL(link).origin !== origin),
    images: { total: images.length, missingAlt }
  };
}

function parseRobots(body) {
  const sitemaps = [];
  let inWildcardGroup = false, blocksRoot = false, allowsRoot = false;
  for (const sourceLine of String(body || '').split(/\r?\n/)) {
    const line = sourceLine.replace(/#.*$/, '').trim(); if (!line) continue;
    const split = line.indexOf(':'); if (split === -1) continue;
    const key = line.slice(0, split).trim().toLowerCase(), value = line.slice(split + 1).trim();
    if (key === 'sitemap' && value) sitemaps.push(value);
    if (key === 'user-agent') { inWildcardGroup = value === '*'; continue; }
    if (inWildcardGroup && key === 'disallow' && value === '/') blocksRoot = true;
    if (inWildcardGroup && key === 'allow' && value === '/') allowsRoot = true;
  }
  return { sitemaps: uniq(sitemaps), blocksRoot: blocksRoot && !allowsRoot };
}

const sitemapUrlCount = (xml) => (String(xml || '').match(/<loc(?:\s[^>]*)?>[\s\S]*?<\/loc>/gi) || []).length;
const issue = (category, severity, code, title, detail, recommendation) => ({ category, severity, code, title, detail, recommendation });

function buildIssues({ target, root, page, robots, sitemap, crawled, brokenLinks }) {
  const issues = [];
  if (root.status >= 400 || root.status === 0) issues.push(issue('crawl','critical','http-status',`Главная отвечает HTTP ${root.status || 'error'}`,'Поисковик и пользователь могут не получить страницу.','Исправьте статус главной страницы до 200 или корректного редиректа на 200.'));
  if (root.redirects.length > 2) issues.push(issue('crawl','warning','redirect-chain',`Цепочка из ${root.redirects.length} редиректов`,'Лишние переходы замедляют загрузку и усложняют обход.','Сократите цепочку до одного прямого редиректа.'));
  if (!page.title) issues.push(issue('seo','error','title-missing','Нет title','Страница не задаёт основной заголовок сниппета.','Добавьте уникальный и конкретный title.'));
  else if (page.titleLength < 25 || page.titleLength > 70) issues.push(issue('seo','warning','title-length',`Title: ${page.titleLength} символов`,page.title,'Сделайте title более компактным и соответствующим поисковому интенту.'));
  if (!page.description) issues.push(issue('seo','warning','description-missing','Нет meta description','Поисковик сам сформирует описание сниппета.','Добавьте уникальное описание страницы.'));
  else if (page.descriptionLength < 60 || page.descriptionLength > 180) issues.push(issue('seo','warning','description-length',`Description: ${page.descriptionLength} символов`,page.description,'Уточните описание и держите его в разумном диапазоне.'));
  if (page.h1Count === 0) issues.push(issue('content','error','h1-missing','Нет H1','Основной видимый заголовок страницы не найден.','Добавьте один содержательный H1.'));
  else if (page.h1Count > 1) issues.push(issue('content','warning','h1-multiple',`Найдено H1: ${page.h1Count}`,page.h1.join(' · '),'Оставьте один основной H1, остальные уровни оформите H2/H3.'));
  if (!page.canonical) issues.push(issue('seo','warning','canonical-missing','Нет canonical','Канонический URL явно не задан.','Добавьте self-canonical на индексируемой странице.'));
  else if (new URL(page.canonical).origin !== new URL(root.finalUrl).origin) issues.push(issue('seo','error','canonical-external','Canonical ведёт на другой домен',page.canonical,'Проверьте, что внешний canonical установлен намеренно.'));
  if (page.noindex) issues.push(issue('seo','critical','meta-noindex','Страница закрыта noindex',page.robots || 'noindex','Удалите noindex, если страница должна участвовать в поиске.'));
  if (!robots.present) issues.push(issue('crawl','warning','robots-missing','robots.txt не найден',`HTTP ${robots.status || 'error'}`,'Опубликуйте robots.txt и укажите sitemap.'));
  else if (robots.blocksRoot) issues.push(issue('crawl','critical','robots-block-root','robots.txt закрывает весь сайт','Для User-agent: * найден Disallow: /.','Откройте нужные разделы для обхода.'));
  if (!sitemap.present) issues.push(issue('crawl','warning','sitemap-missing','Sitemap не обнаружен','Не удалось получить sitemap из robots.txt или /sitemap.xml.','Опубликуйте sitemap.xml и укажите его в robots.txt.'));
  if (brokenLinks.length) issues.push(issue('crawl',brokenLinks.length >= 3 ? 'error' : 'warning','broken-internal-links',`Проблемных внутренних ссылок: ${brokenLinks.length}`,brokenLinks.slice(0,5).map(x=>`${x.status}: ${x.url}`).join(' · '),'Исправьте URL, редиректы и страницы с ошибочными статусами.'));
  if (page.images.total && page.images.missingAlt) { const ratio=Math.round(page.images.missingAlt/page.images.total*100); issues.push(issue('accessibility',ratio>=30?'error':'warning','image-alt',`Без alt: ${page.images.missingAlt} из ${page.images.total}`,`${ratio}% изображений без alt-атрибута.`,'Добавьте осмысленный alt для контентных изображений; декоративным задайте alt="".')); }
  if (!page.htmlLang) issues.push(issue('accessibility','warning','html-lang','Не указан язык документа','<html> без lang.','Добавьте lang="ru", lang="en" или фактический язык страницы.'));
  if (!page.hasViewport) issues.push(issue('accessibility','warning','viewport','Нет viewport meta','Мобильная адаптация может работать некорректно.','Добавьте meta viewport для responsive layout.'));
  const headers=root.headers;
  if (target.protocol !== 'https:') issues.push(issue('security','error','https','Сайт открыт по HTTP',target.toString(),'Настройте HTTPS и редирект HTTP → HTTPS.'));
  if (!headers['content-security-policy']) issues.push(issue('security','warning','csp','Нет Content-Security-Policy','CSP не найден в ответе главной.','Добавьте CSP, совместимую с реальными ресурсами сайта.'));
  if (!headers['x-content-type-options']) issues.push(issue('security','warning','x-content-type-options','Нет X-Content-Type-Options','Заголовок nosniff не найден.','Добавьте X-Content-Type-Options: nosniff.'));
  if (!headers['referrer-policy']) issues.push(issue('security','warning','referrer-policy','Нет Referrer-Policy','Политика referrer явно не задана.','Добавьте подходящую Referrer-Policy.'));
  if (target.protocol === 'https:' && !headers['strict-transport-security']) issues.push(issue('security','warning','hsts','Нет HSTS','Strict-Transport-Security не найден.','После проверки HTTPS добавьте HSTS.'));
  if (crawled.length < 2 && page.internalLinks.length > 0) issues.push(issue('crawl','info','crawl-sample-small','Не удалось собрать достаточную выборку внутренних страниц',`Успешно разобрано страниц: ${crawled.length}.`,'Проверьте таймауты, блокировки и доступность внутренних URL.'));
  return issues;
}

export function scoreIssues(issues) {
  const categories=['seo','crawl','content','accessibility','security'];
  const categoryScores=Object.fromEntries(categories.map(c=>[c,100])); let overall=100;
  for (const item of issues) { const weight=SEVERITY_WEIGHT[item.severity]??0; overall-=weight; if(categoryScores[item.category]!==undefined) categoryScores[item.category]-=weight; }
  for(const c of categories) categoryScores[c]=Math.max(0,categoryScores[c]);
  return { overall:Math.max(0,overall), categories:categoryScores };
}

async function mapLimit(items, limit, worker) {
  const output=new Array(items.length); let cursor=0;
  const runners=Array.from({length:Math.min(limit,items.length)},async()=>{ while(true){ const index=cursor++; if(index>=items.length)return; try{output[index]=await worker(items[index],index);}catch(error){output[index]={error:error instanceof Error?error.message:String(error),input:items[index]};} } });
  await Promise.all(runners); return output;
}

async function probeInternalLink(url) {
  let response=await headSafe(url,{timeoutMs:5000,maxRedirects:4});
  if(response.status===405||response.status===501) response=await fetchSafe(url,{timeoutMs:5000,maxRedirects:4,maxBytes:128*1024});
  return {url,status:response.status,finalUrl:response.finalUrl,redirects:response.redirects.length};
}

async function fetchRobots(origin) {
  const url=new URL('/robots.txt',origin).toString();
  try{const response=await fetchSafe(url,{timeoutMs:6000,maxBytes:512*1024,maxRedirects:3}); const parsed=response.status>=200&&response.status<300?parseRobots(response.body):{sitemaps:[],blocksRoot:false}; return {url,status:response.status,present:response.status>=200&&response.status<300,...parsed};}
  catch(error){return {url,status:0,present:false,sitemaps:[],blocksRoot:false,error:error instanceof Error?error.message:String(error)};}
}

async function fetchSitemap(origin,robots){
  const candidates=uniq([...robots.sitemaps,new URL('/sitemap.xml',origin).toString()]).slice(0,4); const attempts=[];
  for(const candidate of candidates){try{const response=await fetchSafe(candidate,{timeoutMs:6500,maxBytes:1024*1024,maxRedirects:3}); const count=sitemapUrlCount(response.body); const attempt={url:candidate,status:response.status,urlCount:count}; attempts.push(attempt); if(response.status>=200&&response.status<300&&count>0)return {present:true,...attempt,attempts};}catch(error){attempts.push({url:candidate,status:0,urlCount:0,error:error instanceof Error?error.message:String(error)});}}
  return {present:false,status:attempts[0]?.status||0,url:attempts[0]?.url||null,urlCount:0,attempts};
}

export async function auditSite(rawUrl){
  const target=parseTargetUrl(rawUrl);
  const root=await fetchSafe(target.toString(),{timeoutMs:10000,maxBytes:2*1024*1024,maxRedirects:5});
  const contentType=root.headers['content-type']||'';
  if(!/text\/html|application\/xhtml\+xml/i.test(contentType)&&root.body.trim().startsWith('<')===false) throw new Error(`URL не похож на HTML-страницу (${contentType||'content-type неизвестен'})`);
  const page=analyzeHtml(root.body,root.finalUrl); const finalOrigin=new URL(root.finalUrl).origin;
  const robots=await fetchRobots(finalOrigin); const sitemap=await fetchSitemap(finalOrigin,robots);
  const crawlTargets=page.internalLinks.filter(url=>new URL(url).origin===finalOrigin).filter(url=>new URL(url).pathname!==new URL(root.finalUrl).pathname).slice(0,MAX_CRAWL_PAGES-1);
  const crawledChildren=await mapLimit(crawlTargets,3,async(url)=>{const response=await fetchSafe(url,{timeoutMs:6500,maxBytes:1024*1024,maxRedirects:4}); const ct=response.headers['content-type']||''; if(response.status>=400||!/text\/html|application\/xhtml\+xml/i.test(ct))return{url,finalUrl:response.finalUrl,status:response.status,title:'',h1Count:0,noindex:false}; const a=analyzeHtml(response.body,response.finalUrl); return{url,finalUrl:response.finalUrl,status:response.status,title:a.title,h1Count:a.h1Count,noindex:a.noindex,canonical:a.canonical};});
  const crawled=[{url:root.requestedUrl,finalUrl:root.finalUrl,status:root.status,title:page.title,h1Count:page.h1Count,noindex:page.noindex,canonical:page.canonical},...crawledChildren.filter(item=>item&&!item.error)];
  const probeTargets=page.internalLinks.slice(0,MAX_LINK_PROBES); const probes=await mapLimit(probeTargets,5,probeInternalLink);
  const brokenLinks=probes.filter(item=>item&&!item.error&&(item.status>=400||item.status===0)).map(item=>({url:item.url,status:item.status}));
  const probeErrors=probes.filter(item=>item?.error).map(item=>({url:item.input,status:0,error:item.error}));
  const issues=buildIssues({target,root,page,robots,sitemap,crawled,brokenLinks}); const score=scoreIssues(issues);
  const severityCounts=issues.reduce((acc,item)=>{acc[item.severity]=(acc[item.severity]||0)+1;return acc;},{critical:0,error:0,warning:0,info:0});
  return {version:1,auditedAt:new Date().toISOString(),requestedUrl:target.toString(),finalUrl:root.finalUrl,score,severityCounts,response:{status:root.status,durationMs:root.durationMs,redirects:root.redirects,contentType,headers:root.headers},page,discovery:{robots,sitemap,crawledPages:crawled.length,sampledInternalLinks:probeTargets.length,brokenInternalLinks:brokenLinks,probeErrors},crawl:crawled,issues};
}
