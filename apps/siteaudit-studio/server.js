import express from 'express';
import * as cheerio from 'cheerio';
import dns from 'node:dns/promises';
import net from 'node:net';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const app = express();
const PORT = Number(process.env.PORT || 10000);
const __dirname = path.dirname(fileURLToPath(import.meta.url));

app.use(express.json({ limit: '64kb' }));
app.use(express.static(path.join(__dirname, 'public')));

const PRIVATE_V4 = [
  /^10\./,
  /^127\./,
  /^169\.254\./,
  /^192\.168\./,
  /^172\.(1[6-9]|2\d|3[01])\./,
  /^0\./
];

function isPrivateIp(ip) {
  if (net.isIPv4(ip)) return PRIVATE_V4.some((rx) => rx.test(ip));
  if (net.isIPv6(ip)) {
    const x = ip.toLowerCase();
    return x === '::1' || x.startsWith('fc') || x.startsWith('fd') || x.startsWith('fe80:');
  }
  return true;
}

async function normalizeAndValidateUrl(input) {
  let value = String(input || '').trim();
  if (!value) throw new Error('Введите адрес сайта');
  if (!/^https?:\/\//i.test(value)) value = `https://${value}`;
  const url = new URL(value);
  if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Разрешены только http/https URL');
  if (url.username || url.password) throw new Error('URL с логином/паролем не поддерживается');
  if (['localhost', 'localhost.localdomain'].includes(url.hostname.toLowerCase())) throw new Error('Локальные адреса запрещены');

  const records = await dns.lookup(url.hostname, { all: true, verbatim: true });
  if (!records.length || records.some((r) => isPrivateIp(r.address))) throw new Error('Приватные и локальные адреса запрещены');
  return url;
}

async function safeFetch(url, options = {}) {
  const target = await normalizeAndValidateUrl(url.toString());
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), options.timeout || 9000);
  try {
    return await fetch(target, {
      redirect: options.redirect || 'follow',
      signal: controller.signal,
      headers: {
        'user-agent': 'SiteAuditStudio/0.1 (+https://alexgtup.github.io/)',
        accept: options.accept || 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      }
    });
  } finally {
    clearTimeout(timer);
  }
}

function absoluteUrl(href, base) {
  try {
    const u = new URL(href, base);
    return ['http:', 'https:'].includes(u.protocol) ? u : null;
  } catch {
    return null;
  }
}

function scoreFromIssues(issues) {
  const penalty = issues.reduce((sum, x) => sum + ({ high: 18, medium: 8, low: 3 }[x.severity] || 0), 0);
  return Math.max(0, Math.min(100, 100 - penalty));
}

function issue(id, severity, title, detail) {
  return { id, severity, title, detail };
}

async function checkBrokenLinks(urls) {
  const sample = [...new Set(urls)].slice(0, 25);
  const results = [];
  for (const href of sample) {
    try {
      const res = await safeFetch(href, { timeout: 5000 });
      if (res.status >= 400) results.push({ url: href, status: res.status });
    } catch {
      results.push({ url: href, status: 'error' });
    }
  }
  return { checked: sample.length, broken: results };
}

async function audit(input) {
  const requested = await normalizeAndValidateUrl(input);
  const startedAt = Date.now();
  const response = await safeFetch(requested);
  const finalUrl = new URL(response.url || requested.toString());
  const html = await response.text();
  const $ = cheerio.load(html);

  const title = $('title').first().text().trim();
  const description = $('meta[name="description"]').attr('content')?.trim() || '';
  const h1s = $('h1').map((_, el) => $(el).text().trim()).get().filter(Boolean);
  const canonicalRaw = $('link[rel="canonical"]').attr('href') || '';
  const canonical = canonicalRaw ? absoluteUrl(canonicalRaw, finalUrl)?.toString() || canonicalRaw : '';
  const robotsMeta = $('meta[name="robots"]').attr('content')?.toLowerCase() || '';

  const links = $('a[href]').map((_, el) => absoluteUrl($(el).attr('href'), finalUrl)?.toString()).get().filter(Boolean);
  const internalLinks = links.filter((href) => {
    try { return new URL(href).hostname === finalUrl.hostname; } catch { return false; }
  });

  const images = $('img').length;
  const imagesWithoutAlt = $('img').filter((_, el) => !($(el).attr('alt') || '').trim()).length;

  const robotsUrl = new URL('/robots.txt', finalUrl.origin);
  const sitemapUrl = new URL('/sitemap.xml', finalUrl.origin);
  let robots = { status: null, exists: false, content: '' };
  let sitemap = { status: null, exists: false, urls: null };

  try {
    const r = await safeFetch(robotsUrl, { timeout: 6000, accept: 'text/plain,*/*' });
    const text = await r.text();
    robots = { status: r.status, exists: r.ok, content: text.slice(0, 5000) };
  } catch {}

  try {
    const s = await safeFetch(sitemapUrl, { timeout: 6000, accept: 'application/xml,text/xml,*/*' });
    const text = await s.text();
    const count = (text.match(/<loc>/gi) || []).length;
    sitemap = { status: s.status, exists: s.ok, urls: count || null };
  } catch {}

  const brokenLinks = await checkBrokenLinks(internalLinks);
  const headers = Object.fromEntries(response.headers.entries());
  const issues = [];

  if (response.status >= 400) issues.push(issue('http-status', 'high', `HTTP ${response.status}`, 'Главная страница возвращает ошибочный HTTP-статус.'));
  if (!title) issues.push(issue('title-missing', 'high', 'Нет title', 'Добавьте уникальный title для страницы.'));
  else if (title.length < 20 || title.length > 70) issues.push(issue('title-length', 'low', 'Длина title вне ориентира', `Сейчас: ${title.length} символов.`));
  if (!description) issues.push(issue('description-missing', 'medium', 'Нет meta description', 'Добавьте осмысленное описание страницы.'));
  if (h1s.length === 0) issues.push(issue('h1-missing', 'high', 'Нет H1', 'На странице не найден основной заголовок H1.'));
  if (h1s.length > 1) issues.push(issue('h1-multiple', 'medium', 'Несколько H1', `Найдено H1: ${h1s.length}.`));
  if (!canonical) issues.push(issue('canonical-missing', 'medium', 'Нет canonical', 'Добавьте rel=canonical на основной URL страницы.'));
  if (robotsMeta.includes('noindex')) issues.push(issue('noindex', 'high', 'Страница закрыта noindex', 'Meta robots содержит noindex.'));
  if (!robots.exists) issues.push(issue('robots-missing', 'medium', 'robots.txt не найден', `Проверено: ${robotsUrl}`));
  if (!sitemap.exists) issues.push(issue('sitemap-missing', 'medium', 'sitemap.xml не найден', `Проверено: ${sitemapUrl}`));
  if (images && imagesWithoutAlt) issues.push(issue('alt-missing', 'low', 'Изображения без alt', `${imagesWithoutAlt} из ${images} изображений без alt.`));
  if (brokenLinks.broken.length) issues.push(issue('broken-links', 'high', 'Обнаружены битые внутренние ссылки', `Проблемных ссылок: ${brokenLinks.broken.length} из ${brokenLinks.checked} проверенных.`));
  if (!headers['strict-transport-security'] && finalUrl.protocol === 'https:') issues.push(issue('hsts-missing', 'low', 'Нет HSTS', 'Для HTTPS не найден Strict-Transport-Security.'));
  if (!headers['content-security-policy']) issues.push(issue('csp-missing', 'low', 'Нет Content-Security-Policy', 'CSP помогает снизить риск XSS и инъекций.'));

  const score = scoreFromIssues(issues);
  return {
    ok: true,
    auditedAt: new Date().toISOString(),
    durationMs: Date.now() - startedAt,
    requestedUrl: requested.toString(),
    finalUrl: finalUrl.toString(),
    score,
    summary: {
      status: response.status,
      title,
      description,
      h1Count: h1s.length,
      canonical,
      indexable: !robotsMeta.includes('noindex') && response.status < 400,
      robots: robots.exists,
      sitemap: sitemap.exists,
      sitemapUrls: sitemap.urls,
      internalLinks: new Set(internalLinks).size,
      checkedLinks: brokenLinks.checked,
      brokenLinks: brokenLinks.broken.length,
      images,
      imagesWithoutAlt
    },
    issues: issues.sort((a, b) => ({ high: 0, medium: 1, low: 2 }[a.severity] - ({ high: 0, medium: 1, low: 2 }[b.severity])),
    broken: brokenLinks.broken,
    headers: {
      server: headers.server || null,
      contentType: headers['content-type'] || null,
      hsts: Boolean(headers['strict-transport-security']),
      csp: Boolean(headers['content-security-policy']),
      xContentTypeOptions: Boolean(headers['x-content-type-options'])
    }
  };
}

app.get('/api/health', (_req, res) => res.json({ ok: true, service: 'siteaudit-studio' }));

app.get('/api/audit', async (req, res) => {
  try {
    const result = await audit(req.query.url);
    res.json(result);
  } catch (error) {
    const message = error?.name === 'AbortError' ? 'Сайт отвечает слишком долго' : (error?.message || 'Не удалось выполнить аудит');
    res.status(400).json({ ok: false, error: message });
  }
});

app.get('/report', (_req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));
app.get('*', (_req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));

app.listen(PORT, '0.0.0.0', () => console.log(`SiteAudit Studio listening on ${PORT}`));
