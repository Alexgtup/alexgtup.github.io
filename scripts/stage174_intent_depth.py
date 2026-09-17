#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html, json, re, sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'
TODAY='2026-09-17'
STYLE='''<style id="stage174-intent-depth">
.stage174-faq{padding:clamp(68px,6vw,96px) 0;background:#080b0e;color:#f2f5f3;border-top:1px solid rgba(255,255,255,.09)}
.stage174-shell{width:min(1320px,calc(100% - 64px));margin:0 auto}.stage174-head{display:grid;grid-template-columns:minmax(120px,.3fr) minmax(0,1.2fr);gap:clamp(28px,5vw,78px);margin-bottom:34px}.stage174-head>p{margin:0;color:#818b91;font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.15em;text-transform:uppercase}.stage174-head h2{margin:0;max-width:16ch;font-size:clamp(38px,4.2vw,66px);line-height:.98;letter-spacing:-.05em}.stage174-head div>p{max-width:62ch;margin:16px 0 0;color:rgba(226,233,230,.7);line-height:1.7}
.stage174-faq__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.stage174-faq details{border:1px solid rgba(255,255,255,.1);border-radius:16px;background:rgba(255,255,255,.022);padding:0 22px}.stage174-faq summary{cursor:pointer;list-style:none;padding:21px 30px 21px 0;font-weight:700;letter-spacing:-.02em;position:relative}.stage174-faq summary::-webkit-details-marker{display:none}.stage174-faq summary:after{content:'+';position:absolute;right:0;top:19px;color:#c9ff4a;font-size:22px;font-weight:400}.stage174-faq details[open] summary:after{content:'−'}.stage174-faq details p{margin:0;padding:0 0 22px;color:#a8b0b4;line-height:1.68}
.stage174-guide-depth{margin:2.2rem 0 0;padding:1.4rem 0 0;border-top:1px solid rgba(255,255,255,.1)}.stage174-guide-depth ul{margin:.9rem 0 0;padding-left:1.2rem}.stage174-guide-depth li{margin:.55rem 0;line-height:1.65}.stage174-guide-depth .stage174-note{margin-top:1rem;padding:1rem 1.1rem;border-left:2px solid #c9ff4a;background:rgba(201,255,74,.055)}
.stage174-popular{padding:clamp(56px,5vw,78px) 0;background:#f1eee7;color:#171914}.stage174-popular .stage174-head h2{color:#171914}.stage174-popular .stage174-head div>p{color:#555c53}.stage174-popular__links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 28px}.stage174-popular__links a{padding:18px 0;border-top:1px solid rgba(27,31,25,.14);display:flex;align-items:center;justify-content:space-between;gap:14px;text-decoration:none!important;color:#171914!important}.stage174-popular__links strong{font-size:17px;letter-spacing:-.025em}.stage174-popular__links span{color:#65705f;font-size:12px}
@media(max-width:900px){.stage174-shell{width:min(100% - 28px,860px)}.stage174-head{grid-template-columns:1fr;gap:16px}.stage174-faq__grid,.stage174-popular__links{grid-template-columns:1fr}}
@media(max-width:600px){.stage174-shell{width:calc(100% - 24px)}}
</style>'''

FAQS={
'development': [('С чего начать, если стек ещё не выбран?','С пользовательского результата: кто что делает, какие данные участвуют и что должно измениться после действия. Технологию лучше выбирать после этого.'),('Можно начать с небольшой части проекта?','Да. Для большой системы разумно выделить законченный первый этап: один сценарий, интеграцию или проблемный участок, который можно отдельно проверить.'),('Можно продолжить уже существующий проект?','Да. Нужны ссылка, репозиторий или доступ к текущей версии и описание ожидаемого результата. Переписывать всё с нуля обычно не является первым шагом.')],
'web-development': [('Сайт и веб-приложение — это одно и то же?','Нет. Для сайта основная ценность часто в контенте и заявке, для web app — в состоянии пользователя, данных, ролях и действиях внутри интерфейса.'),('Нужна ли отдельная админка?','Только если контентом, пользователями, заявками или состояниями нужно управлять регулярно. Иногда достаточно существующей CMS или небольшого служебного интерфейса.'),('Можно подключить существующую CRM или API?','Да. Интеграции лучше проектировать вместе с основным сценарием, чтобы формы, статусы и данные не расходились между системами.')],
'telegram-bots': [('Когда достаточно обычного Telegram-бота?','Когда сценарий линейный: сообщения, кнопки, формы, статусы, уведомления и простые операции. Сложный интерфейс чаще удобнее вынести в Mini App.'),('Можно подключить оплаты и CRM?','Да, если у платёжного сервиса и CRM есть подходящий API или webhook. Важно заранее определить статусы и обработку повторных событий.'),('Что нужно для оценки бота?','Короткий сценарий пользователя, список внешних сервисов и понимание, где должны храниться данные. Количество кнопок само по себе почти ничего не говорит об объёме.')],
'n8n-automation': [('Когда n8n подходит лучше собственного backend?','Когда процесс состоит из понятной цепочки событий между сервисами и не требует сложного пользовательского состояния или высокой нагрузки.'),('Что происходит, если один сервис недоступен?','Для критичных workflow нужны обработка ошибок, повторные попытки, журнал и уведомление. Просто соединить блоки недостаточно.'),('Можно автоматизировать процесс постепенно?','Да. Лучше начать с повторяемого участка с измеримым результатом и уже после проверки расширять цепочку.')],
'crm-development': [('Когда нужна своя CRM, а не готовая?','Когда процесс заметно отличается от стандартной воронки и постоянные обходные решения в готовой CRM уже стоят дороже собственной логики.'),('Можно интегрировать сайт, Telegram и 1С?','Да. Главное заранее определить источник истины для клиентов, заказов, статусов и документов, чтобы системы не перезаписывали друг друга.'),('Нужно ли переносить все старые данные?','Не всегда. Часто разумнее перенести только активные сущности и нужную историю, а архив оставить доступным отдельно.')],
'api-integrations': [('Что нужно предоставить для интеграции?','Документацию API, тестовые доступы, описание нужного сценария и примеры данных. Если документации нет, сначала закладывается этап исследования.'),('Как избежать дублей при webhook?','Обработчик должен учитывать повторную доставку одного события и быть идемпотентным: повтор не должен создавать вторую оплату, заявку или запись.'),('Можно связать сервисы без официального API?','Иногда можно через экспорт, почту, CSV или парсинг, но такой вариант обычно менее устойчив и его риски стоит оценить отдельно.')],
'backend-development': [('Что входит в backend?','API, бизнес-логика, работа с базой, авторизация, интеграции, фоновые задачи и обработка ошибок — в зависимости от продукта.'),('Как выбрать базу данных?','От модели данных и запросов. Для большинства прикладных систем PostgreSQL является хорошей отправной точкой, но выбор должен следовать из сценария.'),('Можно вынести backend из существующего проекта постепенно?','Да. Часто безопаснее выделять API и отдельные модули по одному, сохраняя рабочий продукт во время перехода.')],
'python-development': [('Для каких задач подходит Python?','Backend, боты, обработка данных, парсеры, интеграции, автоматизация файлов и небольшие внутренние инструменты.'),('Можно доработать чужой Python-проект?','Да. Сначала воспроизводится проблема и проверяются зависимости, окружение и точки интеграции, после чего меняется минимально необходимый участок.'),('Нужен ли сервер для Python-скрипта?','Не всегда. Разовая утилита может запускаться локально, а регулярная автоматизация обычно требует стабильного окружения, расписания и логирования.')],
'mvp-development': [('Что обязательно должно войти в MVP?','Один законченный путь пользователя до ценного результата. Всё, что не проверяет основную гипотезу, можно рассматривать для следующего этапа.'),('Нужно ли делать красивый дизайн сразу?','Интерфейс должен быть понятным и аккуратным, но уникальная дизайн-система редко важнее работающего core-flow на первой версии.'),('Можно сделать MVP так, чтобы потом не переписывать всё?','Да, если границы первой версии известны заранее и критичные данные, роли и интеграции не собираются как временные хаки.')],
'app-development': [('Нужен ли сразу iOS и Android?','Не обязательно. Если аудитория позволяет, старт с одной платформы сокращает объём первой версии и быстрее показывает качество основного сценария.'),('Когда выбрать React Native, а когда native?','React Native удобен для общей кодовой базы, native нужен при глубокой работе с платформой или когда системный UX и API особенно важны.'),('Что нужно подготовить до разработки приложения?','Основной пользовательский путь, список API и системных функций: push, камера, карты, подписки, офлайн-режим и авторизация.')],
'ai-automation': [('Где AI действительно полезен в автоматизации?','В задачах с текстом, классификацией, извлечением данных и подготовкой черновиков, где результат можно проверить правилами или человеком.'),('Нужно ли отдавать AI весь процесс?','Обычно нет. Надёжнее оставить детерминированные шаги обычной логике, а AI использовать там, где действительно нужна работа с неструктурированными данными.'),('Как контролировать ошибки модели?','Ограничивать формат ответа, валидировать результат, хранить исходные данные и добавлять ручное подтверждение для критичных действий.')],
'project-repair': [('Нужно ли переписывать чужой проект?','Не по умолчанию. Сначала нужно воспроизвести проблему, понять архитектуру и стоимость точечного исправления. Переписывание оправдано только если оно дешевле дальнейшей поддержки.'),('Какие доступы нужны для диагностики?','Минимально необходимые: ссылка, репозиторий, логи, staging или нужный административный доступ. Полный root нужен далеко не всегда.'),('Можно исправлять прямо на production?','Для мелких безопасных изменений иногда да, но нормальный подход — иметь backup или git-состояние и по возможности проверять изменение до production.')],
}

GUIDE_DEPTH={
'brief-personal-cabinet': ('Что приложить к первому сообщению',['список ролей и 3–7 действий каждой роли','1–2 примера реальных данных или документов','ссылки на CRM, 1С или API, если кабинет должен с ними работать'],'Если пока есть только идея, достаточно описать один путь пользователя от входа до результата.'),
'api-integration-checklist': ('Минимальный пакет для оценки',['ссылка на документацию API и способ авторизации','пример сущности или ответа, который нужно передать','описание, что считать успешной синхронизацией и как обрабатывать ошибку'],'Если API внешней системы нестабилен или закрыт, это лучше выяснить до оценки основного интерфейса.'),
'automation-first-step': ('Быстрая проверка кандидата',['процесс повторяется минимум несколько раз в неделю','решение в большинстве случаев определяется правилами','результат автоматизации можно проверить цифрой, статусом или записью'],'Если каждый случай требует уникального решения человека, сначала стандартизируйте сам процесс.'),
'site-repair-handoff': ('Что сильно ускорит диагностику',['точный URL и последовательность действий до ошибки','скрин или текст ошибки вместе со временем возникновения','backup, git или понимание, как вернуть рабочую версию'],'Не передавайте пароли в публичных сообщениях — доступы лучше выдавать отдельно и минимально необходимыми.'),
'saas-mvp-scope': ('Тест на лишнюю функцию',['без функции пользователь всё ещё получает основной результат','функция нужна только редкому исключению или будущей роли','её можно временно заменить ручной операцией без подмены ключевой ценности'],'Если без функции невозможно проверить, заплатит ли пользователь за основной результат, она относится к core-flow.'),
'parser-vs-api': ('Что сравнить до выбора',['есть ли официальный API и нужные поля','какие лимиты, частота обновления и объём данных','как быстро источник меняет HTML и насколько критичны пропуски'],'Если данные нужны для критичного процесса, стоимость поддержки парсера нужно учитывать так же, как стоимость первой разработки.'),
}

def add_style(text):
    text=re.sub(r'<style\s+id=["\']stage174-intent-depth["\']>.*?</style>','',text,flags=re.I|re.S)
    return text.replace('</head>',STYLE+'</head>',1)

def insert_before_end(text, block):
    for pat in (r'<section class="p129-contact',r'<section class="s165-bridge',r'</main>'):
        m=re.search(pat,text,re.I)
        if m: return text[:m.start()]+block+text[m.start():]
    raise SystemExit('stage174 insertion marker missing')

# Main commercial pages: answer actual pre-sale questions visibly and in structured data.
for slug,items in FAQS.items():
    fp=ROOT/slug/'index.html'
    if not fp.is_file(): continue
    text=fp.read_text(encoding='utf-8')
    if 'data-stage174-faq="true"' not in text:
        details=''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q,a in items)
        block=f'<section class="stage174-faq" data-stage174-faq="true"><div class="stage174-shell"><div class="stage174-head"><p>BEFORE START</p><div><h2>Частые вопросы до оценки.</h2><p>Коротко о границах задачи, доступах и том, что реально влияет на разработку.</p></div></div><div class="stage174-faq__grid">{details}</div></div></section>'
        text=insert_before_end(text,block)
    schema={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in items]}
    text=re.sub(r'<script[^>]+id=["\']stage174-faq-schema["\'][^>]*>.*?</script>','',text,flags=re.I|re.S)
    text=text.replace('</head>','<script id="stage174-faq-schema" type="application/ld+json">'+json.dumps(schema,ensure_ascii=False,separators=(',',':'))+'</script></head>',1)
    text=add_style(text)
    fp.write_text(text,encoding='utf-8')

# Deepen the six new guides with a practical checkpoint instead of creating more thin URLs.
for slug,(title,bullets,note) in GUIDE_DEPTH.items():
    fp=ROOT/'guides'/slug/'index.html'
    if not fp.is_file(): continue
    text=fp.read_text(encoding='utf-8')
    if 'data-stage174-guide-depth="true"' not in text:
        li=''.join(f'<li>{html.escape(x)}</li>' for x in bullets)
        block=f'<section class="stage174-guide-depth" data-stage174-guide-depth="true"><h2>{html.escape(title)}</h2><ul>{li}</ul><p class="stage174-note">{html.escape(note)}</p></section>'
        text=text.replace('<section class="stage173-related">',block+'<section class="stage173-related">',1)
    text=add_style(text)
    fp.write_text(text,encoding='utf-8')

# Home and services: surface high-intent pages people can recognize immediately.
popular=[('/site-repair/','Доработать сайт'),('/personal-cabinet-development/','Сделать личный кабинет'),('/api-integrations/','Связать сервисы по API'),('/telegram-bots/','Запустить Telegram-бота'),('/excel-google-sheets-automation/','Автоматизировать таблицы'),('/saas-development/','Запустить SaaS / MVP')]
links=''.join(f'<a href="{u}"><strong>{html.escape(t)}</strong><span>Открыть ↗</span></a>' for u,t in popular)
block=f'<section class="stage174-popular" data-stage174-popular="true"><div class="stage174-shell"><div class="stage174-head"><p>POPULAR TASKS</p><div><h2>Если задача уже понятна.</h2><p>Самые частые входы без выбора стека и длинного каталога услуг.</p></div></div><nav class="stage174-popular__links" aria-label="Популярные задачи">{links}</nav></div></section>'
for rel in ('index.html','services/index.html'):
    fp=ROOT/rel; text=fp.read_text(encoding='utf-8')
    if 'data-stage174-popular="true"' not in text:
        m=re.search(r'<section class="stage173-map',text,re.I)
        if m: text=text[:m.start()]+block+text[m.start():]
        else: text=text.replace('</main>',block+'</main>',1)
    text=add_style(text); fp.write_text(text,encoding='utf-8')

# Freshness for pages materially changed by this stage.
changed=['/','/services/']+[f'/{s}/' for s in FAQS]+[f'/guides/{s}/' for s in GUIDE_DEPTH]
for fname in ('sitemap.xml','sitemap-google.xml'):
    fp=ROOT/fname
    if not fp.exists(): continue
    text=fp.read_text(encoding='utf-8')
    for route in changed:
        url=BASE+route
        text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',r'\g<1>'+TODAY,text,count=1)
    fp.write_text(text,encoding='utf-8')

# Guards.
for slug,items in FAQS.items():
    text=(ROOT/slug/'index.html').read_text(encoding='utf-8')
    if text.count('data-stage174-faq="true"')!=1 or text.count('stage174-faq-schema')!=1: raise SystemExit('stage174 FAQ guard '+slug)
for slug in GUIDE_DEPTH:
    if 'data-stage174-guide-depth="true"' not in (ROOT/'guides'/slug/'index.html').read_text(encoding='utf-8'): raise SystemExit('stage174 guide guard '+slug)
print(f'stage174 intent depth: service_faq={len(FAQS)}, guide_depth={len(GUIDE_DEPTH)}, popular_maps=2')
