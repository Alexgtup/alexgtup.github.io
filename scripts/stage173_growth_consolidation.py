#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html, json, re, sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
TODAY = '2026-09-17'
MARKER = 'stage173-growth-consolidation'

STYLE = r'''<style id="stage173-growth-consolidation">
.stage173-map{padding:clamp(72px,7vw,112px) 0;background:#090c0f;color:#f2f5f3;border-top:1px solid rgba(255,255,255,.09);border-bottom:1px solid rgba(255,255,255,.09)}
.stage173-shell{width:min(1320px,calc(100% - 64px));margin:0 auto}.stage173-head{display:grid;grid-template-columns:minmax(120px,.3fr) minmax(0,1.2fr);gap:clamp(28px,5vw,78px);align-items:start;margin-bottom:clamp(34px,4vw,58px)}
.stage173-eyebrow{margin:0;color:#818b91;font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.15em;text-transform:uppercase}.stage173-head h2{margin:0;max-width:15ch;font-size:clamp(40px,4.5vw,70px);line-height:.96;letter-spacing:-.052em;color:#f2f5f3}.stage173-head div>p{max-width:64ch;margin:18px 0 0;color:rgba(226,233,230,.7);font-size:clamp(15px,1.05vw,18px);line-height:1.7}
.stage173-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.stage173-group{position:relative;overflow:hidden;padding:clamp(24px,3vw,38px);border:1px solid rgba(255,255,255,.1);border-radius:20px;background:linear-gradient(145deg,rgba(255,255,255,.035),rgba(255,255,255,.012))}.stage173-group:before{content:"";position:absolute;inset:0 auto 0 0;width:2px;background:#c9ff4a;opacity:.35}.stage173-group>p{margin:0;color:#818b91;font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase}.stage173-group h3{margin:12px 0 22px;font-size:clamp(24px,2.2vw,34px);line-height:1;letter-spacing:-.04em;color:#f2f5f3}.stage173-group nav{display:grid}.stage173-group nav a{display:grid;grid-template-columns:minmax(0,1fr) auto 20px;gap:14px;align-items:center;padding:15px 0;border-top:1px solid rgba(255,255,255,.1);color:#f2f5f3!important;text-decoration:none!important;transition:padding-left .18s ease,color .18s ease}.stage173-group nav a:hover{padding-left:8px;color:#c9ff4a!important}.stage173-group nav strong{font-size:15px;letter-spacing:-.015em}.stage173-group nav span{font-size:12px;color:#818b91}.stage173-group nav b{font-size:14px;font-weight:500}
.stage173-case-links{padding:clamp(64px,6vw,92px) 0;background:#0a0d10;color:#f2f5f3;border-top:1px solid rgba(255,255,255,.09)}.stage173-case-links .stage173-head{margin-bottom:30px}.stage173-case-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.stage173-case-row a{min-height:150px;padding:24px;border:1px solid rgba(255,255,255,.1);border-radius:16px;text-decoration:none!important;color:#f2f5f3!important;background:rgba(255,255,255,.02);display:flex;flex-direction:column;justify-content:space-between}.stage173-case-row a:hover{border-color:rgba(201,255,74,.42);transform:translateY(-3px)}.stage173-case-row small{color:#818b91;font:700 10px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase}.stage173-case-row strong{font-size:clamp(20px,1.8vw,28px);line-height:1;letter-spacing:-.035em}.stage173-case-row span{font-size:13px;color:#a5adb2}
.stage173-guide-strip{padding:clamp(68px,6vw,96px) 0;background:#f1eee7;color:#171914;border-top:1px solid rgba(27,31,25,.12)}.stage173-guide-strip .stage173-head h2{color:#171914}.stage173-guide-strip .stage173-head div>p{color:#555c53}.stage173-guide-strip .stage173-eyebrow{color:#6b7167}.stage173-guide-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 34px}.stage173-guide-grid a{padding:24px 0;border-top:1px solid rgba(27,31,25,.14);text-decoration:none!important;color:#171914!important}.stage173-guide-grid small{display:block;margin-bottom:9px;color:#6b7167;font:700 10px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase}.stage173-guide-grid strong{display:block;font-size:clamp(18px,1.55vw,24px);line-height:1.15;letter-spacing:-.03em}.stage173-guide-grid span{display:block;margin-top:10px;color:#5b6159;font-size:14px;line-height:1.55}
.stage173-endcap{padding:28px 0;background:#c9ff4a;color:#071008}.stage173-endcap__inner{width:min(1320px,calc(100% - 64px));margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:24px}.stage173-endcap strong{font-size:clamp(22px,2vw,30px);letter-spacing:-.035em}.stage173-endcap span{display:block;margin-top:4px;color:#35412a}.stage173-endcap a{padding:13px 18px;border-radius:999px;background:#071008;color:white!important;text-decoration:none!important;font-weight:750;white-space:nowrap}
.ux-guide-main .stage173-related{margin-top:3.5rem;padding-top:2rem;border-top:1px solid rgba(255,255,255,.1)}.ux-guide-main .stage173-related h2{margin-top:0}.ux-guide-main .stage173-related__links{display:flex;flex-wrap:wrap;gap:.6rem}.ux-guide-main .stage173-related__links a{padding:.7rem .9rem;border:1px solid rgba(255,255,255,.12);border-radius:.8rem;text-decoration:none}
.stage173-guide-nudge{width:min(1320px,calc(100% - 64px));margin:0 auto;padding:24px 0;border-top:1px solid rgba(255,255,255,.1);display:grid;grid-template-columns:minmax(150px,.3fr) minmax(0,1fr);gap:24px;align-items:center}.stage173-guide-nudge>span{color:#818b91;font:700 10px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.13em}.stage173-guide-nudge>a{display:flex;align-items:center;justify-content:space-between;gap:18px;color:#f2f5f3!important;text-decoration:none!important}.stage173-guide-nudge strong{font-size:clamp(17px,1.45vw,22px);letter-spacing:-.025em}.stage173-guide-nudge b{color:#c9ff4a;font-size:13px;white-space:nowrap}
@media(max-width:900px){.stage173-guide-nudge{width:min(100% - 28px,860px);grid-template-columns:1fr;gap:10px}.stage173-shell,.stage173-endcap__inner{width:min(100% - 28px,860px)}.stage173-head{grid-template-columns:1fr;gap:18px}.stage173-grid,.stage173-case-row,.stage173-guide-grid{grid-template-columns:1fr}.stage173-endcap__inner{align-items:flex-start;flex-direction:column}.stage173-endcap a{white-space:normal}}
@media(max-width:600px){.stage173-shell,.stage173-endcap__inner{width:calc(100% - 24px)}.stage173-group{padding:22px 18px}.stage173-group nav a{grid-template-columns:minmax(0,1fr) 18px}.stage173-group nav a span{display:none}}
</style>'''

GROUPS = [
 ('01 / PRODUCT','Продукт и интерфейс',[
   ('/web-development/','Сайт / web app','Интерфейс + backend'),('/personal-cabinet-development/','Личный кабинет','Пользователи и роли'),('/saas-development/','SaaS-сервис','Продукт с аккаунтами'),('/mvp-development/','MVP','Первая рабочая версия')]),
 ('02 / AUTOMATION','Автоматизация и данные',[
   ('/n8n-automation/','n8n / workflows','Связать сервисы'),('/excel-google-sheets-automation/','Excel / Sheets','Убрать ручную обработку'),('/python-scripts/','Python-скрипты','Утилиты и данные'),('/ai-automation/','AI-автоматизация','AI внутри процесса')]),
 ('03 / INTEGRATIONS','Интеграции',[
   ('/api-development/','API','Контракт для систем'),('/crm-integration/','CRM','Сайт, Telegram, CRM'),('/1c-integration/','1С','Каталог и заказы'),('/payment-integration/','Оплата','Webhooks и статусы')]),
 ('04 / REPAIR','Доработка',[
   ('/site-repair/','Сайт','Ошибки и новые функции'),('/wordpress-development/','WordPress','Тема, плагины, формы'),('/tilda-development/','Tilda','Zero Block + код'),('/bitrix-development/','1С-Битрикс','Компоненты и интеграции')]),
]

def task_map(title='Что именно нужно запустить?', lead='Можно начать не с технологии, а с результата. Выберите ближайший сценарий - внутри уже собраны связанные услуги и реальные примеры.'):
    cards=[]
    for eyebrow, heading, items in GROUPS:
        rows=''.join(f'<a href="{u}"><strong>{html.escape(t)}</strong><span>{html.escape(d)}</span><b>↗</b></a>' for u,t,d in items)
        cards.append(f'<article class="stage173-group"><p>{eyebrow}</p><h3>{html.escape(heading)}</h3><nav aria-label="{html.escape(heading)}">{rows}</nav></article>')
    return f'<section class="stage173-map" data-stage173-map="true"><div class="stage173-shell"><div class="stage173-head"><p class="stage173-eyebrow">TASK MAP</p><div><h2>{html.escape(title)}</h2><p>{html.escape(lead)}</p></div></div><div class="stage173-grid">{"".join(cards)}</div></div></section>'

GUIDES = [
 dict(slug='brief-personal-cabinet', title='Что написать в ТЗ на личный кабинет | Alexuys', h1='ТЗ на личный кабинет: что описать до разработки', desc='Практический чек-лист для личного кабинета: роли, вход, данные, ключевые действия, статусы, документы, интеграции и критерии готовности.', kicker='ЛИЧНЫЙ КАБИНЕТ · БРИФ', intro='Большое техническое задание не обязательно. Для адекватной оценки важнее описать пользователей, их действия и данные, которые должны меняться после каждого действия.', sections=[
 ('Начните с ролей, а не с экранов','Запишите, кто входит в систему: клиент, партнёр, менеджер, администратор. Для каждой роли достаточно перечислить 3-7 действий, которые она должна выполнять. Это сразу показывает границы кабинета и права доступа.'),
 ('Опишите одно главное действие','Фраза «нужен личный кабинет» слишком широкая. Гораздо полезнее: клиент видит заявку, загружает документ, получает статус и может повторить заказ. Такой сценарий уже можно разбить на интерфейс, backend и данные.'),
 ('Зафиксируйте источник данных','Отдельно укажите, откуда берутся клиенты, заказы, документы, цены и статусы. Это может быть CRM, 1С, существующая база, API или ручной ввод. Без этого невозможно честно оценить интеграционную часть.'),
 ('Продумайте состояния и ошибки','Что видит пользователь до загрузки документа, после отправки, при отказе, после оплаты? Как восстановить доступ? Что происходит, если внешний API недоступен? Состояния важнее количества страниц.'),
 ('Критерий готовности','В конце сформулируйте 3-5 проверок: новый пользователь может зарегистрироваться; заявка появляется у менеджера; статус возвращается клиенту; документы доступны только своей роли. Это превращает описание в проверяемый результат.')], related=[('/personal-cabinet-development/','Разработка личного кабинета'),('/admin-panel-development/','Админ-панель'),('/api-integrations/','API-интеграции')]),
 dict(slug='api-integration-checklist', title='Интеграция API: чек-лист перед разработкой | Alexuys', h1='Что проверить перед интеграцией API', desc='Чек-лист API-интеграции: авторизация, сущности, webhooks, лимиты, ошибки, идемпотентность, тестовый контур и журнал обмена.', kicker='API · CHECKLIST', intro='Главный риск интеграции обычно не в HTTP-запросе. Он появляется в авторизации, повторных событиях, несовпадении сущностей и ситуациях, когда одна из систем временно недоступна.', sections=[
 ('Есть ли нормальная документация','Нужны endpoint-ы, схема авторизации, примеры запросов и ответов, коды ошибок, лимиты и правила тестового окружения. Если этого нет, оценка должна учитывать исследование API.'),
 ('Кто источник истины','Для каждого поля определите владельца. Например, цена меняется в 1С, статус оплаты - в платёжной системе, комментарий менеджера - в CRM. Если обе системы одновременно «главные», синхронизация начинает конфликтовать.'),
 ('Событие или опрос','Если сервис поддерживает webhooks, обычно лучше реагировать на событие. Если нет - нужен polling с расписанием и контролем повторов. В обоих случаях важно не создавать дубль при повторной доставке.'),
 ('Ошибки должны быть видимы','Интеграция не должна молча терять заявку. Нужны лог, понятный статус, повторная попытка там, где она безопасна, и способ вручную переотправить проблемную запись.'),
 ('Проверьте тестовый сценарий','До релиза стоит пройти минимум: успешный запрос, неверные данные, таймаут, повтор webhook, недоступность внешнего сервиса и восстановление после ошибки.')], related=[('/api-development/','Разработка API'),('/api-integrations/','Интеграции API'),('/payment-integration/','Интеграция оплаты')]),
 dict(slug='automation-first-step', title='Что автоматизировать первым в бизнес-процессе | Alexuys', h1='Автоматизация: какой процесс брать первым', desc='Как выбрать первый процесс для автоматизации: частота, повторяемость, цена ошибки, доступность API, исключения и измеримый результат.', kicker='AUTOMATION · PRIORITY', intro='Первый workflow лучше выбирать не по принципу «это раздражает», а по сочетанию частоты, понятных правил и измеримого результата. Тогда автоматизация быстро проверяется и не превращается в бесконечную схему.', sections=[
 ('Ищите повторяемый шаг','Хороший кандидат повторяется часто и выглядит почти одинаково: перенести заявку, сверить статус, собрать отчёт, обновить таблицу, уведомить ответственного.'),
 ('Не начинайте с хаоса','Если сотрудники каждый раз принимают решение по разным правилам, сначала стоит описать процесс. Автоматизация нестабильного процесса обычно просто делает нестабильность быстрее.'),
 ('Посчитайте цену ошибки','Чем критичнее операция, тем больше нужны проверки, журналы, подтверждение человеком и сценарий отката. Не каждый шаг стоит полностью отдавать workflow.'),
 ('Проверьте доступы и API','До сборки нужно понять, дают ли используемые CRM, таблицы, формы и сервисы нужные API/webhook. Иногда узкое место - не n8n, а отсутствие доступа к данным.'),
 ('Сформулируйте метрику','Например: заявка попадает в CRM за минуту; ежедневный отчёт собирается без ручного копирования; дубли не создаются; ошибка отправляет уведомление. Такая метрика даёт понятное «готово».')], related=[('/automation-services/','Автоматизация процессов'),('/n8n-automation/','n8n'),('/excel-google-sheets-automation/','Excel / Google Sheets')]),
 dict(slug='site-repair-handoff', title='Как передать сайт на доработку другому разработчику | Alexuys', h1='Как подготовить сайт к доработке чужим разработчиком', desc='Что передать разработчику для доработки сайта: ссылка, доступы, репозиторий, воспроизведение ошибки, окружение, резервная копия и критерий проверки.', kicker='SITE REPAIR · HANDOFF', intro='Для точечной доработки не нужен идеальный архив проекта. Но несколько вещей сильно сокращают время на диагностику и снижают риск сломать то, что уже работает.', sections=[
 ('Ссылка и конкретный сценарий','Вместо «форма не работает» полезно написать путь: открыть страницу, заполнить поля, нажать кнопку, ожидать письмо, фактически получить ошибку. Это делает проблему воспроизводимой.'),
 ('Доступы разделяйте по задаче','Не всегда нужен полный root. Для WordPress может хватить админки и SFTP, для frontend - репозитория и staging, для API - тестового ключа. Доступ даётся минимально необходимый.'),
 ('Сохраните рабочее состояние','Перед изменениями нужен backup или git-состояние, к которому можно вернуться. На живом коммерческом сайте это важнее скорости первой правки.'),
 ('Покажите, что уже пробовали','Если ошибка появилась после обновления плагина, переноса домена или изменения API - это полезный контекст. Даже неудачная попытка помогает сузить поиск.'),
 ('Опишите проверку после фикса','Например: форма уходит на нужную почту, меню не прыгает на 390 px, webhook приходит один раз, страница не теряет canonical. Проверка должна быть наблюдаемой.')], related=[('/site-repair/','Доработка сайта'),('/project-repair/','Доработка проекта'),('/wordpress-development/','WordPress')]),
 dict(slug='saas-mvp-scope', title='Как сократить SaaS до MVP без потери основной идеи | Alexuys', h1='SaaS MVP: что оставить в первой версии', desc='Как выбрать состав первой версии SaaS: core-flow, роли, тарифы, платежи, админка, интеграции и функции, которые можно отложить.', kicker='SAAS · MVP SCOPE', intro='MVP не обязан быть маленьким по количеству экранов. Он должен быть маленьким по количеству гипотез: один пользователь получает один ценный результат без ручной подмены ключевой функции.', sections=[
 ('Оставьте один core-flow','Опишите путь от регистрации до результата в одном предложении. Всё, что не помогает пройти этот путь, кандидат на перенос во вторую версию.'),
 ('Роли только необходимые','Если в будущем будет пять ролей, но для проверки нужны пользователь и администратор - начинайте с двух. Сложная permission-модель быстро увеличивает объём.'),
 ('Платежи можно отделить от ценности','Иногда достаточно ручного тарифа на первых клиентах; иногда платёж - часть самой гипотезы и нужен сразу. Решение зависит от того, что именно проверяется.'),
 ('Админка должна закрывать поддержку','Не стройте отдельную ERP. Достаточно функций, которые нужны для пользователей, ошибок, тарифов и ручного исправления критичных состояний.'),
 ('Интеграции подключайте по необходимости','Если ценность можно проверить на одном источнике данных, не нужно сразу подключать все CRM, почты и аналитические системы. Сначала докажите основной сценарий.')], related=[('/saas-development/','Разработка SaaS'),('/mvp-development/','Разработка MVP'),('/admin-panel-development/','Админ-панель')]),
 dict(slug='parser-vs-api', title='Парсер или API: как выбрать способ получения данных | Alexuys', h1='Парсер или API: что использовать для данных', desc='Когда использовать официальный API, а когда HTML-парсер: стабильность, лимиты, авторизация, структура данных, частота обновления и поддержка.', kicker='DATA · API VS PARSER', intro='Если источник даёт официальный API с нужными полями, обычно это первый выбор. Парсер нужен, когда API отсутствует или не покрывает данные, но тогда нужно заранее принять стоимость поддержки изменений источника.', sections=[
 ('API обычно стабильнее структуры страницы','API предназначен для машинного обмена: поля типизированы, ошибки описаны, версия меняется контролируемо. HTML создавался для браузера и может измениться из-за редизайна.'),
 ('Но API может не отдавать всё','Иногда нужные данные видны на странице, а публичного endpoint нет. Тогда HTML-парсинг может быть техническим вариантом, если доступ к данным допустим и нагрузка разумна.'),
 ('Сравните лимиты и частоту','Для ежедневного каталога одного запроса в минуту достаточно, а для realtime-мониторинга - нет. Лимиты API, частота обхода и объём страниц напрямую влияют на архитектуру.'),
 ('Продумайте изменения источника','У парсера должны быть проверки, которые замечают пропавший блок или неожиданно пустое поле. Иначе он продолжит работать технически, но начнёт сохранять неверные данные.'),
 ('Выходной формат одинаково важен','Независимо от способа получения, нужно заранее определить результат: CSV/XLSX, база, webhook, API или обновление CRM. Сбор данных - только первая половина задачи.')], related=[('/web-scraping-parsers/','Парсеры данных'),('/api-integrations/','API-интеграции'),('/python-scripts/','Python-скрипты')]),
]

CASE_LINKS = {
 'fin-planner': [('/telegram-bots/','Telegram-боты'),('/payment-integration/','Онлайн-оплата'),('/backend-development/','Backend')],
 'swift-calendar': [('/ios-development/','iOS / Swift'),('/app-development/','Мобильные приложения'),('/mvp-development/','MVP')],
 'sheetpilot-ai': [('/excel-google-sheets-automation/','Excel / Sheets'),('/ai-chatbot-development/','AI-ассистенты'),('/saas-development/','SaaS')],
 'seo-control-center': [('/admin-panel-development/','Админ-панели'),('/saas-development/','SaaS'),('/backend-development/','Backend')],
 'auto-crm': [('/crm-development/','CRM'),('/crm-integration/','CRM-интеграции'),('/admin-panel-development/','Админ-панели')],
 'factory-catalog': [('/1c-integration/','Интеграция 1С'),('/ecommerce-development/','Ecommerce'),('/web-development/','Web-разработка')],
 'taxi-app': [('/app-development/','Мобильные приложения'),('/project-repair/','Доработка проекта'),('/backend-development/','Backend')],
 'siteaudit-studio': [('/web-scraping-parsers/','Парсеры / crawler'),('/python-scripts/','Python-скрипты'),('/backend-development/','Backend')],
 'freelance-os': [('/saas-development/','SaaS'),('/admin-panel-development/','Админ-панели'),('/automation-services/','Автоматизация')],
}

def inject_style(text:str)->str:
    text=re.sub(r'<style\s+id=["\']stage173-growth-consolidation["\']>.*?</style>','',text,flags=re.I|re.S)
    return text.replace('</head>',STYLE+'</head>',1) if '</head>' in text else text

def set_meta(text:str, title:str, desc:str, url:str)->str:
    text=re.sub(r'<title>.*?</title>',f'<title>{html.escape(title)}</title>',text,count=1,flags=re.I|re.S)
    def set_tag(pattern,repl):
        nonlocal text
        if re.search(pattern,text,re.I): text=re.sub(pattern,repl,text,count=1,flags=re.I)
        else: text=text.replace('</head>',repl+'</head>',1)
    set_tag(r'<meta[^>]+name=["\']description["\'][^>]*>',f'<meta name="description" content="{html.escape(desc,quote=True)}"/>')
    set_tag(r'<link[^>]+rel=["\']canonical["\'][^>]*>',f'<link rel="canonical" href="{url}"/>')
    set_tag(r'<meta[^>]+property=["\']og:url["\'][^>]*>',f'<meta property="og:url" content="{url}"/>')
    set_tag(r'<meta[^>]+property=["\']og:title["\'][^>]*>',f'<meta property="og:title" content="{html.escape(title,quote=True)}"/>')
    set_tag(r'<meta[^>]+property=["\']og:description["\'][^>]*>',f'<meta property="og:description" content="{html.escape(desc,quote=True)}"/>')
    return text

def guide_main(g):
    parts=[]
    for i,(h,p) in enumerate(g['sections'],1):
        parts.append(f'<section id="step-{i}"><h2>{html.escape(h)}</h2><p>{html.escape(p)}</p></section>')
    rel=''.join(f'<a href="{u}">{html.escape(t)} ↗</a>' for u,t in g['related'])
    return f'''<main id="main-content" class="ux-guide-main"><div class="container crumbs"><a href="/">Главная</a> / <a href="/guides/">Разборы</a> / {html.escape(g['h1'])}</div><section class="container hero"><div class="kicker" data-nosnippet="">{html.escape(g['kicker'])}</div><h1>{html.escape(g['h1'])}</h1><p class="lead">{html.escape(g['intro'])}</p><div class="meta" data-nosnippet=""><span>Обновлено 17.09.2026</span><span>Автор: Александр · Alexuys</span></div></section><div class="container layout"><article class="article"><section id="short"><h2>Короткий ответ</h2><div class="answer"><b>{html.escape(g['intro'])}</b></div></section>{''.join(parts)}<section class="stage173-related"><h2>Связанные направления</h2><div class="stage173-related__links">{rel}</div></section></article><aside class="sidebar"><div class="side-card"><small>ПРАКТИЧЕСКИЙ РАЗБОР</small><h2>Нужно применить это к вашему проекту?</h2><p>Пришлите ссылку или короткое описание текущего состояния. Для первого шага большой документ не нужен.</p><a class="button primary" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Написать в Telegram ↗</a></div></aside></div></main>'''

def add_schema(text,g,url):
    text=re.sub(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>','',text,flags=re.I|re.S)
    article={'@context':'https://schema.org','@type':'Article','headline':g['h1'],'description':g['desc'],'dateModified':TODAY,'datePublished':TODAY,'author':{'@type':'Person','@id':BASE+'/#person','name':'Александр'},'publisher':{'@id':BASE+'/#person'},'url':url,'mainEntityOfPage':url,'inLanguage':'ru-RU','image':{'@type':'ImageObject','url':BASE+'/assets/og/alexuys-default.jpg','width':1200,'height':630}}
    crumbs={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Главная','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Разборы','item':BASE+'/guides/'},{'@type':'ListItem','position':3,'name':g['h1'],'item':url}]}
    blob=''.join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False,separators=(',',':'))+'</script>' for x in (article,crumbs))
    return text.replace('</head>',blob+'</head>',1)

# 1. Homepage: one useful chooser instead of keyword stuffing.
home=ROOT/'index.html'; ht=home.read_text(encoding='utf-8')
if 'data-stage173-map="true"' not in ht:
    marker=re.search(r'<section class="p128-proof',ht,re.I)
    if not marker: raise SystemExit('stage173: homepage insertion marker missing')
    ht=ht[:marker.start()]+task_map()+ht[marker.start():]
ht=inject_style(ht); home.write_text(ht,encoding='utf-8')

# 2. Services hub: replace the flat 16-link SEO list with a grouped task map.
svc=ROOT/'services'/'index.html'; st=svc.read_text(encoding='utf-8')
st,n=re.subn(r'<section class="p130-list-section stage172-service-expansion".*?</section>',task_map('Все услуги - по типу результата.','Ниже не каталог технологий, а четыре понятных сценария: создать продукт, автоматизировать работу, связать системы или доработать существующее.'),st,count=1,flags=re.I|re.S)
if n!=1 and 'data-stage173-map="true"' not in st: raise SystemExit('stage173: service expansion replacement failed')
st=inject_style(st); svc.write_text(st,encoding='utf-8')

# 3. New decision guides, cloned from the fully styled existing guide shell.
template=(ROOT/'guides'/'development-cost'/'index.html').read_text(encoding='utf-8')
for g in GUIDES:
    url=f'{BASE}/guides/{g["slug"]}/'
    x=template
    x=set_meta(x,g['title'],g['desc'],url)
    x=re.sub(r'<main\b.*?</main>',guide_main(g),x,count=1,flags=re.I|re.S)
    x=add_schema(x,g,url)
    x=inject_style(x)
    dest=ROOT/'guides'/g['slug']/'index.html'; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(x,encoding='utf-8')

# 4. Guide hub: visible long-tail discovery section.
gh=ROOT/'guides'/'index.html'; gt=gh.read_text(encoding='utf-8')
if 'data-stage173-guides="true"' not in gt:
    cards=''.join(f'<a href="/guides/{g["slug"]}/"><small>{html.escape(g["kicker"])}</small><strong>{html.escape(g["h1"])}</strong><span>{html.escape(g["desc"])}</span></a>' for g in GUIDES)
    block=f'<section class="stage173-guide-strip" data-stage173-guides="true"><div class="stage173-shell"><div class="stage173-head"><p class="stage173-eyebrow">NEW GUIDES</p><div><h2>Перед разработкой.</h2><p>Практические разборы по тем вопросам, которые сильнее всего меняют объём, риски и архитектуру проекта.</p></div></div><div class="stage173-guide-grid">{cards}</div></div></section>'
    m=re.search(r'<section class="[^"\']*p130-footer-cta',gt,re.I)
    if not m: m=re.search(r'</main>',gt,re.I)
    gt=gt[:m.start()]+block+gt[m.start():]
gt=set_meta(gt,'Гайды по разработке: API, SaaS, автоматизация и CRM | Alexuys','Практические разборы перед разработкой: личные кабинеты, API, автоматизация, SaaS MVP, доработка сайтов, парсеры, Telegram, CRM и стоимость проекта.',BASE+'/guides/')
gt=inject_style(gt); gh.write_text(gt,encoding='utf-8')

# Broaden services hub snippet now that the catalog covers more commercial intents.
st=set_meta(st,'Разработка на заказ: сайты, SaaS, Telegram и автоматизация | Alexuys','Разработка на заказ: сайты и web apps, SaaS, Telegram, CRM, Python, API, n8n, 1С, WordPress, Tilda, Битрикс и доработка существующих проектов.',BASE+'/services/')
st=inject_style(st); svc.write_text(st,encoding='utf-8')

# 4b. Two contextual inbound links per new guide: hub + two service sources => no isolated long-tail pages.
GUIDE_INBOUND = {
 'brief-personal-cabinet': ['/personal-cabinet-development/','/admin-panel-development/'],
 'api-integration-checklist': ['/api-development/','/api-integrations/'],
 'automation-first-step': ['/automation-services/','/n8n-automation/'],
 'site-repair-handoff': ['/site-repair/','/project-repair/'],
 'saas-mvp-scope': ['/saas-development/','/mvp-development/'],
 'parser-vs-api': ['/web-scraping-parsers/','/python-development/'],
}
for g in GUIDES:
    for route in GUIDE_INBOUND[g['slug']]:
        fp=ROOT/route.strip('/')/'index.html'
        if not fp.is_file(): continue
        x=fp.read_text(encoding='utf-8')
        token=f'data-stage173-guide-nudge="{g["slug"]}"'
        if token in x: continue
        nudge=f'<aside class="stage173-guide-nudge" {token}><span>ПРАКТИЧЕСКИЙ РАЗБОР</span><a href="/guides/{g["slug"]}/"><strong>{html.escape(g["h1"])}</strong><b>Читать ↗</b></a></aside>'
        markers=[r'<section class="p129-contact',r'<section class="s165-bridge',r'</main>']
        for pat in markers:
            m=re.search(pat,x,re.I)
            if m: x=x[:m.start()]+nudge+x[m.start():]; break
        x=inject_style(x); fp.write_text(x,encoding='utf-8')

# 5. Case -> service bridges. Real work now points directly to commercially relevant capabilities.
for slug, links in CASE_LINKS.items():
    fp=ROOT/'cases'/slug/'index.html'
    if not fp.is_file(): continue
    x=fp.read_text(encoding='utf-8')
    if 'data-stage173-case-links="true"' in x: continue
    cards=''.join(f'<a href="{u}"><small>RELATED SERVICE</small><strong>{html.escape(t)}</strong><span>Посмотреть направление ↗</span></a>' for u,t in links)
    block=f'<section class="stage173-case-links" data-stage173-case-links="true"><div class="stage173-shell"><div class="stage173-head"><p class="stage173-eyebrow">FROM CASE TO TASK</p><div><h2>Похожая задача?</h2><p>Кейс показывает реальную работу, а эти страницы - варианты реализации для нового проекта.</p></div></div><div class="stage173-case-row">{cards}</div><div class="stage173-case-action"><a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить похожую задачу ↗</a></div></div></section>'
    markers=[r'<section class="s165-bridge',r'<section class="p132-contact',r'</main>']
    for pat in markers:
        m=re.search(pat,x,re.I)
        if m: x=x[:m.start()]+block+x[m.start():]; break
    x=inject_style(x); fp.write_text(x,encoding='utf-8')

# 6. Make selected high-intent pages end with a direct action, not another SEO block.
for route in ('cases/','guides/','telegram-bot-repair/','wordpress-development/'):
    fp=ROOT/route/'index.html'
    if not fp.is_file(): continue
    x=fp.read_text(encoding='utf-8')
    if 'data-stage173-endcap="true"' not in x:
        block='<section class="stage173-endcap" data-stage173-endcap="true"><div class="stage173-endcap__inner"><div><strong>Есть конкретная задача?</strong><span>Ссылка, ошибка или желаемый результат - достаточно для первого сообщения.</span></div><a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить в Telegram ↗</a></div></section>'
        x=x.replace('</main>',block+'</main>',1)
    x=inject_style(x); fp.write_text(x,encoding='utf-8')

# 7. Discovery files and freshness.
new_urls=[f'{BASE}/guides/{g["slug"]}/' for g in GUIDES]
for fname in ('sitemap.xml','sitemap-google.xml'):
    fp=ROOT/fname
    if not fp.exists(): continue
    x=fp.read_text(encoding='utf-8')
    add=''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.65</priority></url>' for u in new_urls if u not in x)
    if add: x=x.replace('</urlset>',add+'</urlset>',1)
    # Refresh every route materially changed by this batch.
    changed_routes=['/','/services/','/guides/','/development/','/cases/']
    changed_routes += [f'/cases/{slug}/' for slug in CASE_LINKS]
    changed_routes += sorted({route for routes in GUIDE_INBOUND.values() for route in routes})
    for route in changed_routes:
        u=BASE+route
        x=re.sub(r'(<loc>'+re.escape(u)+r'</loc><lastmod>)[^<]+',r'\g<1>'+TODAY,x,count=1)
    fp.write_text(x,encoding='utf-8')
sp=ROOT/'sitemap.txt'
if sp.exists():
    lines=sp.read_text(encoding='utf-8').splitlines(); sp.write_text('\n'.join(lines+[u for u in new_urls if u not in lines])+'\n',encoding='utf-8')
llms=ROOT/'llms.txt'
if llms.exists():
    x=llms.read_text(encoding='utf-8')
    if '## Новые практические разборы' not in x:
        x=x.rstrip()+'\n\n## Новые практические разборы\n'+'\n'.join(f'- {g["h1"]}: {BASE}/guides/{g["slug"]}/' for g in GUIDES)+'\n'
        llms.write_text(x,encoding='utf-8')

# Atom feed: publish the new guides as discoverable editorial entries and refresh feed date.
feed=ROOT/'feed.xml'
if feed.exists():
    import xml.etree.ElementTree as ET
    ET.register_namespace('', 'http://www.w3.org/2005/Atom')
    ns={'a':'http://www.w3.org/2005/Atom'}
    tree=ET.parse(feed); root=tree.getroot()
    updated=root.find('a:updated',ns)
    if updated is not None: updated.text=TODAY+'T00:00:00Z'
    existing={(e.find('a:id',ns).text or '') for e in root.findall('a:entry',ns) if e.find('a:id',ns) is not None}
    for g in GUIDES:
        url=f'{BASE}/guides/{g["slug"]}/'
        if url in existing: continue
        e=ET.SubElement(root,'{http://www.w3.org/2005/Atom}entry')
        ET.SubElement(e,'{http://www.w3.org/2005/Atom}title').text=g['h1']
        ET.SubElement(e,'{http://www.w3.org/2005/Atom}link',{'href':url})
        ET.SubElement(e,'{http://www.w3.org/2005/Atom}id').text=url
        ET.SubElement(e,'{http://www.w3.org/2005/Atom}updated').text=TODAY+'T00:00:00Z'
        ET.SubElement(e,'{http://www.w3.org/2005/Atom}summary').text=g['desc']
    tree.write(feed,encoding='utf-8',xml_declaration=True)

# Guardrails.
smap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
for g,u in zip(GUIDES,new_urls):
    fp=ROOT/'guides'/g['slug']/'index.html'; text=fp.read_text(encoding='utf-8')
    if text.count(f'<link rel="canonical" href="{u}"/>')!=1: raise SystemExit('stage173 canonical '+g['slug'])
    if smap.count(f'<loc>{u}</loc>')!=1: raise SystemExit('stage173 sitemap '+g['slug'])
    if text.count('<h1>')!=1: raise SystemExit('stage173 h1 '+g['slug'])
for slug in CASE_LINKS:
    if 'data-stage173-case-links="true"' not in (ROOT/'cases'/slug/'index.html').read_text(encoding='utf-8'): raise SystemExit('stage173 case link '+slug)
print(f'stage173 growth consolidation: guides={len(GUIDES)}, cases={len(CASE_LINKS)}, homepage/services task maps=2, direct endcaps=4')
