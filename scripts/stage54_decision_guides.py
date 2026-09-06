#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from urllib.parse import quote
import hashlib, html as H, json, re, sys, xml.etree.ElementTree as ET

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
home=root/'index.html'; home_hash=hashlib.sha256(home.read_bytes()).hexdigest()
BASE='https://alexgtup.github.io'
TG='https://t.me/Alexuys?text='+quote('Здравствуйте. Прочитал разбор на сайте.\n\nЗадача: ')

GUIDES={
'n8n-vs-backend':{
 'title':'n8n или backend: что выбрать для автоматизации | Alexuys',
 'desc':'Когда задачу лучше собрать в n8n/Make, а когда нужен собственный backend. Сравнение по логике, данным, нагрузке, ошибкам и стоимости поддержки.',
 'h1':'n8n или backend: <em>где заканчивается workflow и начинается разработка.</em>',
 'lead':'Оба подхода умеют получать данные, вызывать API и запускать действия. Разница проявляется не в первом успешном сценарии, а в сложности правил, объёме данных, требованиях к отказоустойчивости и дальнейшем развитии.',
 'kicker':'N8N · MAKE · BACKEND',
 'service':'/n8n-automation/','service_name':'Автоматизация n8n / Make','second':'/backend-development/','second_name':'Backend-разработка',
 'cards':[
  ('n8n / Make','Подходит, когда процесс можно нарисовать как последовательность событий: webhook → проверка → API → уведомление. Особенно удобен для CRM, Telegram, таблиц и SaaS с нормальными API.'),
  ('Собственный backend','Нужен, когда логика становится продуктовой: сложные права, транзакции, большие объёмы данных, нестандартные алгоритмы, высокая нагрузка или строгие требования к состоянию системы.'),
  ('Гибрид','Часто лучший вариант: n8n управляет понятным процессом и интеграциями, а сложная операция вынесена в небольшой API-сервис. Так workflow остаётся читаемым, а код — локальным.'),],
 'sections':[
  ('Смотрите не на количество блоков, а на природу логики','Workflow хорош там, где видно начало и конец операции. Если менеджер отправил форму, данные проверились, создалась сделка в CRM и ушло уведомление — это естественный сценарий n8n. Если внутри появляются десятки состояний пользователя, конкурирующие изменения одних данных и сложные правила доступа, visual workflow постепенно превращается в код, только менее удобный для тестирования.'),
  ('Данные и состояние — главный водораздел','Передать заявку между сервисами и хранить полноценную модель продукта — разные задачи. n8n может хранить промежуточные значения, но не обязан становиться основной базой бизнес-логики. Если несколько интерфейсов одновременно работают с общими сущностями, чаще нужен backend и нормальная база данных.'),
  ('Ошибки должны иметь предсказуемый путь','В простой автоматизации достаточно увидеть сбой шага, сохранить контекст и повторить операцию. В критичном backend-процессе важны идемпотентность, транзакции, очереди, контроль параллельности и восстановление состояния. Чем дороже ошибка для продукта, тем осторожнее стоит относиться к попытке решить всё одним workflow.'),
  ('Когда начать с n8n всё равно разумно','Если бизнес-процесс ещё проверяется, n8n позволяет быстро увидеть реальное движение данных и найти лишние шаги. После этого сложную часть можно вынести в код, не переписывая весь процесс. Такой путь часто дешевле архитектуры «на будущее», которую никто ещё не проверял.'),],
 'matrix':[('Нужно связать 2–5 готовых сервисов','n8n / Make'),('Много ролей и собственных сущностей','Backend'),('Есть один сложный алгоритм среди простых интеграций','Гибрид'),('Нужна прозрачность процесса для команды','n8n / Make'),('Высокая нагрузка и строгая консистентность','Backend')],
 'faq':[('Можно ли сделать весь backend в n8n?','Технически многие операции возможны. Вопрос не в возможности, а в поддерживаемости: если workflow начинает исполнять роль большой модели данных, авторизации и сложной бизнес-логики, отдельный backend обычно становится понятнее.'),('Нужно ли переписывать n8n, если проект вырос?','Нет. Часто достаточно вынести только перегруженные шаги в API-сервис, а orchestration оставить в n8n.')]
},
'site-vs-web-app':{
 'title':'Сайт или веб-приложение: что нужно проекту | Alexuys',
 'desc':'Как понять, нужен обычный сайт, веб-приложение или внутренний сервис. Сравнение по задачам пользователя, данным, авторизации, SEO и стоимости разработки.',
 'h1':'Сайт или веб-приложение: <em>разница начинается с действия пользователя.</em>',
 'lead':'Внешне оба варианта открываются в браузере, поэтому их часто смешивают в одном ТЗ. Но маркетинговая страница, каталог, личный кабинет и рабочая система требуют разной архитектуры и по-разному зависят от SEO, backend и данных.',
 'kicker':'WEB · PRODUCT · UX',
 'service':'/web-development/','service_name':'Разработка сайтов и веб-сервисов','second':'/mvp-development/','second_name':'Разработка MVP',
 'cards':[
  ('Сайт','Основная задача — объяснить, показать, помочь найти информацию и привести к заявке. Контент, скорость, мобильная версия и поисковая доступность здесь обычно важнее сложного состояния пользователя.'),
  ('Веб-приложение','Пользователь регулярно что-то делает: создаёт объекты, меняет статусы, работает в кабинете, видит персональные данные. Нужны авторизация, backend и управление состояниями.'),
  ('Внутренний сервис','Поисковый трафик почти не важен. Ценность — в рабочем процессе команды: роли, документы, фильтры, интеграции, история действий и сокращение ручных операций.'),],
 'sections':[
  ('Первый вопрос — что человек делает после открытия страницы','Если основной путь — прочитать информацию, сравнить варианты и отправить заявку, это ближе к сайту. Если после входа пользователь проводит в интерфейсе время, создаёт и изменяет данные, это уже продуктовый сценарий веб-приложения.'),
  ('SEO важно не каждому экрану','Публичные страницы сайта должны быть понятны поисковику без авторизации и тяжёлого клиентского состояния. В кабинете или внутренней CRM индексация, наоборот, чаще не нужна. Попытка сделать весь проект одинаково «SEO-ориентированным» добавляет сложность без пользы.'),
  ('Backend появляется из данных, а не из модного стека','Форма обратной связи может работать с минимальной серверной частью. Но как только появляются аккаунты, права, сохранённые объекты, история операций или интеграции, серверная модель становится частью продукта. Тогда выбор frontend-фреймворка уже не главный архитектурный вопрос.'),
  ('Один проект может содержать оба слоя','У SaaS часто есть публичный сайт для поиска и продаж плюс авторизованное веб-приложение. Их можно визуально объединить брендом, но требования к рендерингу, аналитике, безопасности и данным будут разными.'),],
 'matrix':[('Лендинг услуги или компании','Сайт'),('Каталог с заявкой без аккаунта','Сайт / каталог'),('Личный кабинет клиента','Веб-приложение'),('CRM или панель сотрудников','Внутренний сервис'),('SaaS с публичной витриной','Сайт + веб-приложение')],
 'faq':[('Можно ли начать с сайта, а потом добавить кабинет?','Да, если заранее не строить публичную часть так, что любое расширение требует переписывания всего проекта. Backend и авторизацию можно подключить отдельным этапом.'),('Нужен ли Next.js или React обычному лендингу?','Не обязательно. Технология должна оправдываться требованиями к контенту, интерактивности, поддержке и дальнейшему развитию.')]
},
'repair-vs-rewrite':{
 'title':'Дорабатывать или переписывать проект с нуля | Alexuys',
 'desc':'Когда существующий сайт, бот или приложение стоит доработать, а когда переписывание оправдано. Практические критерии: воспроизводимость ошибок, архитектура и цена изменений.',
 'h1':'Дорабатывать или переписывать: <em>сначала измерьте цену следующего изменения.</em>',
 'lead':'Старый код сам по себе не является причиной начинать заново. И наоборот, бесконечные локальные исправления могут стать дороже переноса действительно нужной логики. Решение принимается после диагностики конкретного сценария, а не по возрасту проекта.',
 'kicker':'PROJECT REPAIR · LEGACY · RELEASE',
 'service':'/project-repair/','service_name':'Доработка существующего проекта','second':'/development/','second_name':'Разработка цифровых продуктов',
 'cards':[
  ('Дорабатывать','Проект запускается, ошибка воспроизводится, зависимости ещё поддерживаются, а нужное изменение локально и не ломает модель данных или ключевые интерфейсы.'),
  ('Заменить часть','Один модуль, интеграция или экран создаёт большинство проблем. Его можно отделить контрактом и заменить, сохранив остальной рабочий продукт.'),
  ('Переписывать','Каждая небольшая правка требует менять несвязанные участки, нет воспроизводимой сборки, зависимости критически устарели или текущая модель данных блокирует необходимый продуктовый сценарий.'),],
 'sections':[
  ('Rewrite почти всегда недооценивают','В старом проекте уже зашиты десятки мелких решений: edge cases, форматы данных, права, поведение пользователей. При полном переписывании их приходится заново обнаруживать. Поэтому новая кодовая база не означает автоматически меньший риск.'),
  ('Начните с одного критичного сценария','Полезнее воспроизвести конкретную проблему — например, пользователь не может оплатить или заявка не попадает в CRM — и пройти путь от интерфейса до данных. Это показывает реальные границы дефекта и качество соседних модулей лучше, чем абстрактная оценка «код плохой».'),
  ('Частичная замена часто даёт лучший баланс','Если проблемный участок имеет понятные входы и выходы, его можно вынести в новый модуль или сервис. Такой подход сохраняет работающие части и одновременно снижает риск будущих изменений в самом слабом месте.'),
  ('Переписывание оправдано, когда меняется сам продукт','Если новая версия требует другой модели ролей, данных и пользовательского пути, сохранение старой архитектуры может стать искусственным ограничением. Тогда задача уже не «починить код», а перенести подтверждённую бизнес-логику в новую систему.'),],
 'matrix':[('Одна воспроизводимая ошибка','Доработать'),('Нестабильна одна интеграция','Заменить часть'),('Нет воспроизводимой сборки и тестового окружения','Сначала диагностика'),('Меняется только интерфейс','Обычно доработать'),('Меняется модель данных и основной пользовательский путь','Рассмотреть rewrite')],
 'faq':[('Можно ли оценить чужой код без полного аудита?','Первую задачу — часто да. Для точной оценки всего будущего развития нужен больший контекст, но воспроизводимый проблемный сценарий уже даёт полезную информацию.'),('Что прислать для диагностики?','Ссылку или архив проекта, способ запуска, шаги воспроизведения проблемы и ожидаемое поведение. Если есть логи или доступ к тестовой среде, они сокращают время поиска причины.')]
}}

CSS='''
:root{--bg:#08090b;--surface:#101319;--text:#f4f5f2;--muted:#969da6;--line:rgba(255,255,255,.11);--lime:#c9ff4a;--blue:#8195ff;--page:clamp(1rem,4vw,4.5rem);--max:86rem}*{box-sizing:border-box}html{background:var(--bg);scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 80% 0,rgba(129,149,255,.11),transparent 34rem),var(--bg);color:var(--text);font-family:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.6}a{color:inherit}.container{width:min(100%,var(--max));margin:auto;padding-inline:var(--page)}.header{position:sticky;top:0;z-index:20;background:rgba(8,9,11,.82);backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}.head{min-height:4.6rem;display:flex;align-items:center;justify-content:space-between;gap:1rem}.brand{font-weight:900;text-decoration:none}.nav{display:flex;gap:1rem;align-items:center}.nav a{font-size:.78rem;text-decoration:none;color:#a0a7af}.nav .cta{background:var(--lime);color:#08090b;padding:.65rem .85rem;border-radius:.8rem;font-weight:850}.hero{padding:6rem 0 5rem}.kicker{font:700 .66rem/1.2 ui-monospace,monospace;letter-spacing:.09em;color:#7c858f}.hero h1{font-size:clamp(3rem,7vw,6.7rem);line-height:.92;letter-spacing:-.063em;margin:1rem 0 0;max-width:13ch}.hero h1 em,.section h2 em{font-style:normal;color:#9299a2}.hero p{max-width:51rem;color:#9ca3ac;font-size:clamp(1rem,1.5vw,1.16rem);line-height:1.75}.actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1.6rem}.btn{display:inline-flex;min-height:3rem;align-items:center;justify-content:center;padding:.72rem 1rem;border:1px solid var(--line);border-radius:.9rem;text-decoration:none;font-weight:800;font-size:.82rem}.btn.primary{background:var(--lime);border-color:var(--lime);color:#090a0b}.section{padding:5.5rem 0;border-top:1px solid rgba(255,255,255,.055)}.section-head{display:grid;grid-template-columns:.34fr 1.66fr;gap:2rem;margin-bottom:2.2rem}.section-head>span{color:#737c86;font:700 .64rem/1.3 ui-monospace,monospace;letter-spacing:.08em}.section h2{margin:0;font-size:clamp(2.35rem,5vw,4.8rem);line-height:.98;letter-spacing:-.052em;max-width:15ch}.section-head p{color:#929aa4;max-width:54rem}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem}.card{border:1px solid var(--line);border-radius:1.05rem;padding:1.3rem;background:linear-gradient(145deg,#11151a,#0d1014)}.card h3{margin:0;font-size:1.1rem}.card p,.prose p,.faq p{color:#929aa4}.prose{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem}.prose article{padding:1.35rem;border:1px solid var(--line);border-radius:1.05rem}.prose h3{margin:0}.matrix{border-top:1px solid var(--line)}.row{display:grid;grid-template-columns:1.4fr .6fr;gap:1rem;padding:1rem 0;border-bottom:1px solid var(--line)}.row strong:last-child{color:var(--lime)}.faq details{border-bottom:1px solid var(--line);padding:1rem 0}.faq summary{cursor:pointer;font-weight:850}.related{display:flex;flex-wrap:wrap;gap:.65rem}.related a{padding:.8rem 1rem;border:1px solid var(--line);border-radius:.9rem;text-decoration:none}.footer{padding:2.5rem 0;color:#6f7780;font-size:.74rem;border-top:1px solid var(--line)}@media(max-width:850px){.section-head,.prose{grid-template-columns:1fr}.cards{grid-template-columns:1fr}.nav a:not(.cta){display:none}}@media(max-width:560px){.hero{padding:4.5rem 0 3.5rem}.section{padding:4rem 0}.actions{display:grid}.btn{width:100%}.row{grid-template-columns:1fr}.hero h1,.section h2{max-width:100%}}
'''

def make(slug,c):
    url=f'{BASE}/guides/{slug}/'
    cards=''.join(f'<article class="card"><h3>{H.escape(a)}</h3><p>{H.escape(b)}</p></article>' for a,b in c['cards'])
    prose=''.join(f'<article><h3>{H.escape(a)}</h3><p>{H.escape(b)}</p></article>' for a,b in c['sections'])
    matrix=''.join(f'<div class="row"><span>{H.escape(a)}</span><strong>{H.escape(b)}</strong></div>' for a,b in c['matrix'])
    faq=''.join(f'<details><summary>{H.escape(a)}</summary><p>{H.escape(b)}</p></details>' for a,b in c['faq'])
    schema={'@context':'https://schema.org','@type':'Article','headline':re.sub('<.*?>','',c['h1']),'description':c['desc'],'url':url,'author':{'@type':'Person','name':'Александр Александров','alternateName':['Alexuys','gglalex'],'url':f'{BASE}/about/','sameAs':['https://github.com/Alexgtup','https://freelance.ru/gglalex','https://t.me/Alexuys']},'publisher':{'@type':'Person','name':'Александр Александров'},'inLanguage':'ru-RU','dateModified':'2026-09-06'}
    crumbs={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Портфолио','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Гайды','item':BASE+'/guides/'},{'@type':'ListItem','position':3,'name':re.sub('<.*?>','',c['h1']),'item':url}]}
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="color-scheme" content="dark"><meta name="theme-color" content="#08090b"><title>{H.escape(c['title'])}</title><meta name="description" content="{H.escape(c['desc'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><meta name="author" content="Александр Александров (Alexuys)"><link rel="canonical" href="{url}"><meta property="og:type" content="article"><meta property="og:site_name" content="Alexuys"><meta property="og:locale" content="ru_RU"><meta property="og:title" content="{H.escape(c['title'],quote=True)}"><meta property="og:description" content="{H.escape(c['desc'],quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/og/alexuys-default.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{H.escape(c['title'],quote=True)}"><meta name="twitter:description" content="{H.escape(c['desc'],quote=True)}"><meta name="twitter:image" content="{BASE}/assets/og/alexuys-default.jpg"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><style>{CSS}</style><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><script type="application/ld+json">{json.dumps(crumbs,ensure_ascii=False,separators=(',',':'))}</script></head><body><a class="skip-link" href="#main-content" style="position:absolute;left:-9999px">Перейти к содержанию</a><header class="header"><div class="container head"><a class="brand" href="/">ALEXUYS</a><nav class="nav" aria-label="Основная навигация"><a href="/services/">Услуги</a><a href="/cases/">Кейсы</a><a href="/guides/">Гайды</a><a class="cta" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Telegram ↗</a></nav></div></header><main id="main-content"><section class="hero"><div class="container"><span class="kicker">{H.escape(c['kicker'])} · DECISION GUIDE</span><h1>{c['h1']}</h1><p>{H.escape(c['lead'])}</p><div class="actions"><a class="btn primary" href="{c['service']}">{H.escape(c['service_name'])} →</a><a class="btn" href="#compare">Сравнить варианты ↓</a></div></div></section><section class="section" id="compare"><div class="container"><div class="section-head"><span>01 / ВАРИАНТЫ</span><div><h2>Выбирайте по <em>ограничениям задачи.</em></h2><p>Названия технологий полезны только после того, как понятны пользовательский сценарий, данные и требования к дальнейшему развитию.</p></div></div><div class="cards">{cards}</div></div></section><section class="section"><div class="container"><div class="section-head"><span>02 / КРИТЕРИИ</span><div><h2>Где решение <em>начинает отличаться.</em></h2></div></div><div class="prose">{prose}</div></div></section><section class="section"><div class="container"><div class="section-head"><span>03 / БЫСТРАЯ ПРОВЕРКА</span><div><h2>Ориентир до <em>технического задания.</em></h2></div></div><div class="matrix">{matrix}</div></div></section><section class="section faq"><div class="container"><div class="section-head"><span>04 / ВОПРОСЫ</span><div><h2>Два частых <em>пограничных случая.</em></h2></div></div>{faq}</div></section><section class="section"><div class="container"><div class="section-head"><span>05 / ДАЛЬШЕ</span><div><h2>Перейдите к <em>конкретному направлению.</em></h2><p>Если после сравнения формат понятен, коммерческая страница уже описывает состав результата, кейсы и следующий шаг.</p></div></div><div class="related"><a href="{c['service']}">{H.escape(c['service_name'])} →</a><a href="{c['second']}">{H.escape(c['second_name'])} →</a><a href="/cases/">Реальные кейсы →</a><a href="{TG}" target="_blank" rel="noopener noreferrer">Обсудить задачу ↗</a></div></div></section></main><footer class="footer"><div class="container">© Alexuys · Александр Александров · <a href="/guides/">Все гайды</a></div></footer></body></html>'''

for slug,c in GUIDES.items():
    d=root/'guides'/slug; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(make(slug,c),encoding='utf8')

# sitemap: built output only; source sitemap remains untouched.
sm=root/'sitemap.xml'; ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9'); ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml')
tree=ET.parse(sm); rt=tree.getroot(); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}; locs={(x.text or '').strip() for x in rt.findall('.//s:loc',ns)}
for slug in GUIDES:
    u=f'{BASE}/guides/{slug}/'
    if u not in locs:
        el=ET.SubElement(rt,'{http://www.sitemaps.org/schemas/sitemap/0.9}url');ET.SubElement(el,'{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text=u;ET.SubElement(el,'{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text='2026-09-06'
tree.write(sm,encoding='utf-8',xml_declaration=True)
st=root/'sitemap.txt'
if st.is_file():
    txt=st.read_text(encoding='utf8')
    for slug in GUIDES:
        u=f'{BASE}/guides/{slug}/'
        if u not in txt: txt=txt.rstrip()+f'\n{u}\n'
    st.write_text(txt,encoding='utf8')

# Link the new guides from the existing guide hub and the matching service pages.
hub=root/'guides/index.html'; text=hub.read_text(encoding='utf8')
for slug,c in GUIDES.items():
    href=f'/guides/{slug}/'
    if href not in text:
        card=f'<a href="{href}"><span>GUIDE</span><h3>{H.escape(re.sub("<.*?>","",c["h1"]))}</h3><p>{H.escape(c["desc"])}</p><b>Читать →</b></a>'
        marker='</div></div></section>'
        pos=text.find(marker,text.find('s50-guide-grid'))
        if pos>0:text=text[:pos]+card+text[pos:]
hub.write_text(text,encoding='utf8')
links=[('n8n-automation','/guides/n8n-vs-backend/','n8n или backend'),('backend-development','/guides/n8n-vs-backend/','n8n или backend'),('web-development','/guides/site-vs-web-app/','Сайт или веб-приложение'),('mvp-development','/guides/site-vs-web-app/','Сайт или веб-приложение'),('project-repair','/guides/repair-vs-rewrite/','Дорабатывать или переписывать')]
for route,href,label in links:
    p=root/route/'index.html'; t=p.read_text(encoding='utf8')
    if href not in t:
        marker='<div class="s48-related">'; i=t.find(marker)
        if i>=0:
            i+=len(marker);t=t[:i]+f'<a href="{href}"><strong>{H.escape(label)}</strong><span>Разбор →</span></a>'+t[i:]
    p.write_text(t,encoding='utf8')

if hashlib.sha256(home.read_bytes()).hexdigest()!=home_hash: raise SystemExit('stage54 invariant failed: homepage changed')
print('stage54 decision guides: 3 pages created; sitemap and contextual links updated; homepage unchanged')
