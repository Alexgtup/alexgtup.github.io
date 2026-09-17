from __future__ import annotations
from pathlib import Path
import html, re, sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-17'

DATA={
'personal-cabinet-development':('Личный кабинет', ['Регистрация, вход и восстановление доступа','Профиль, заявки, документы и статусы','Роли пользователя и администратора','Интеграция с CRM, оплатой или API'], ['Количество ролей и различия между ними','Источник данных и двусторонняя синхронизация','Документы, оплаты и история изменений'], '/guides/brief-personal-cabinet/'),
'admin-panel-development':('Админ-панель', ['Пользователи, роли и права','Таблицы, фильтры, поиск и статусы','Редактирование данных и журнал действий','Связь с основным приложением через API'], ['Количество сущностей и бизнес-правил','Нужны ли массовые операции и импорт','Права доступа, аудит и история изменений'], '/guides/brief-personal-cabinet/'),
'saas-development':('SaaS-сервис', ['Регистрация и аккаунт пользователя','Основной рабочий сценарий продукта','Админка для поддержки и управления','Тарифы, оплата или ограничения доступа'], ['Количество ролей и тарифов','Сложность core-flow и фоновых задач','Интеграции, биллинг и требования к надёжности'], '/guides/saas-mvp-scope/'),
'ecommerce-development':('Интернет-магазин', ['Каталог, категории и карточка товара','Корзина и оформление заказа','Оплата, доставка и статусы','Передача заказов в CRM или 1С'], ['Размер каталога и структура фильтров','Синхронизация цен, остатков и заказов','Логика доставки, оплаты и возвратов'], '/guides/api-integration-checklist/'),
'excel-google-sheets-automation':('Excel / Google Sheets', ['Загрузка или чтение таблиц','Очистка, объединение и расчёты','Автоматические отчёты и выгрузки','Передача данных в CRM, API или документы'], ['Количество форматов входных файлов','Правила обработки и исключения','Частота запуска и объём данных'], '/guides/automation-first-step/'),
'python-scripts':('Python-скрипт', ['Чтение файлов, API или базы данных','Обработка и проверка данных','Логи, ошибки и безопасный повтор','Результат в CSV, XLSX, API или системе'], ['Объём данных и частота запуска','Нестандартные форматы и исключения','Авторизация и ограничения внешних сервисов'], '/guides/parser-vs-api/'),
'web-scraping-parsers':('Парсер данных', ['Получение HTML, JSON или API-ответов','Извлечение и нормализация полей','Дедупликация и проверка пустых значений','Экспорт, база или передача дальше'], ['Количество источников и страниц','Защита, авторизация и динамический контент','Как часто меняется структура источника'], '/guides/parser-vs-api/'),
'1c-integration':('Интеграция 1С', ['Синхронизация товаров и справочников','Цены, остатки и статусы','Заказы, клиенты и документы','Логи обмена и повтор ошибок'], ['Направление обмена и источник истины','Формат API, CommerceML или промежуточный слой','Объём каталога и частота синхронизации'], '/guides/api-integration-checklist/'),
'payment-integration':('Онлайн-оплата', ['Создание платежа из сайта или бота','Webhook и проверка статуса','Возвраты и повторные уведомления','Запись результата в CRM или базу'], ['Разовые платежи или подписки','Чеки, возвраты и дополнительные статусы','Связь с заказами и внутренней учётной системой'], '/guides/api-integration-checklist/'),
'crm-integration':('CRM-интеграция', ['Создание и обновление лидов','Передача контактов, заказов и статусов','Webhooks и реакция на события CRM','Лог ошибок и защита от дублей'], ['Какая CRM и доступный API','Односторонний или двусторонний обмен','Правила сопоставления сущностей и дублей'], '/guides/api-integration-checklist/'),
'api-development':('REST API', ['Контракт endpoints и схема данных','Авторизация, валидация и права','База данных и бизнес-правила','Документация, ошибки и журналирование'], ['Количество сущностей и связей','Роли, безопасность и ограничения доступа','Webhooks, фоновые задачи и внешние интеграции'], '/guides/api-integration-checklist/'),
'automation-services':('Автоматизация процесса', ['Триггер: форма, CRM, расписание или webhook','Проверка и преобразование данных','Действия в нужных сервисах','Лог, уведомление и обработка ошибки'], ['Количество сервисов в цепочке','Сколько исключений требует ручного решения','Цена ошибки и требования к повтору'], '/guides/automation-first-step/'),
'site-repair':('Доработка сайта', ['Воспроизведение проблемы и диагностика','Точечная правка без лишнего переписывания','Проверка desktop и mobile сценария','Резервная точка и проверка после релиза'], ['Состояние исходного кода и доступов','Есть ли staging или только боевой сайт','Связана ли ошибка с внешними API и плагинами'], '/guides/site-repair-handoff/'),
'ai-chatbot-development':('AI-ассистент', ['Канал: сайт, Telegram или внутренний интерфейс','Контекст, база знаний или инструменты','Structured output и безопасные действия','Передача человеку и журнал диалогов'], ['Какие данные можно передавать модели','Нужны ли действия через API, а не только ответы','Требования к контролю ошибок и human handoff'], '/guides/automation-first-step/'),
'tilda-development':('Tilda / Zero Block', ['Адаптив блоков и форм','HTML, CSS и JavaScript для нестандартной логики','Интеграция форм, CRM и API','Исправление текущих визуальных и технических ошибок'], ['Насколько страница собрана в Zero Block','Нужны ли кастомные калькуляторы и скрипты','Есть ли сторонние виджеты и интеграции'], '/guides/site-repair-handoff/'),
'bitrix-development':('1С-Битрикс', ['Доработка шаблона и компонентов','Формы, каталог и пользовательские сценарии','API и интеграции с внешними системами','Техническая диагностика и производительность'], ['Редакция Битрикс и текущее решение','Количество кастомных компонентов','Интеграция с 1С, CRM и внешними модулями'], '/guides/site-repair-handoff/'),
}

STYLE='''<style id="stage175-secondary-depth">.s175-depth{padding:clamp(70px,7vw,108px) 0;background:#0b0e11;color:#eef2ef;border-top:1px solid rgba(255,255,255,.09)}.s175-shell{width:min(1180px,calc(100% - 64px));margin:auto}.s175-head{display:grid;grid-template-columns:.55fr 1.2fr;gap:40px;margin-bottom:34px}.s175-k{font:700 11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.14em;color:#879198}.s175-head h2{margin:0;font-size:clamp(34px,4vw,58px);line-height:.98;letter-spacing:-.045em}.s175-head p{margin:14px 0 0;color:#aab2b7;line-height:1.7;max-width:62ch}.s175-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.s175-card{padding:26px;border:1px solid rgba(255,255,255,.1);border-radius:18px;background:rgba(255,255,255,.025)}.s175-card small{color:#879198;font:700 10px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.13em}.s175-card h3{margin:10px 0 18px;font-size:24px;letter-spacing:-.03em}.s175-card ul{margin:0;padding:0;list-style:none}.s175-card li{padding:11px 0;border-top:1px solid rgba(255,255,255,.09);line-height:1.55;color:#d8deda}.s175-brief{margin-top:14px;padding:22px 26px;border-radius:18px;background:#c9ff4a;color:#0c1309;display:flex;gap:24px;align-items:center;justify-content:space-between}.s175-brief p{margin:0;max-width:70ch;line-height:1.55}.s175-brief a{flex:0 0 auto;padding:12px 16px;border-radius:999px;background:#0c1309;color:#fff!important;text-decoration:none!important;font-weight:750}@media(max-width:780px){.s175-shell{width:calc(100% - 28px)}.s175-head,.s175-grid{grid-template-columns:1fr}.s175-brief{align-items:flex-start;flex-direction:column}.s175-brief a{white-space:normal}}</style>'''

for slug,(label,first,factors,guide) in DATA.items():
    fp=ROOT/slug/'index.html'
    if not fp.is_file(): continue
    x=fp.read_text(encoding='utf-8')
    x=re.sub(r'<style id="stage175-secondary-depth">.*?</style>','',x,flags=re.I|re.S)
    if 'data-stage175-depth="true"' not in x:
        a=''.join(f'<li>{html.escape(v)}</li>' for v in first)
        b=''.join(f'<li>{html.escape(v)}</li>' for v in factors)
        block=f'''<section class="s175-depth" data-stage175-depth="true"><div class="s175-shell"><div class="s175-head"><span class="s175-k">SCOPE / ESTIMATE</span><div><h2>Что входит в рабочую версию.</h2><p>{html.escape(label)} оценивается не по количеству экранов, а по сценариям, данным и внешним системам. Ниже - минимальный набор, от которого удобно отталкиваться перед оценкой.</p></div></div><div class="s175-grid"><article class="s175-card"><small>FIRST VERSION</small><h3>Базовый контур</h3><ul>{a}</ul></article><article class="s175-card"><small>WHAT CHANGES SCOPE</small><h3>Что меняет объём</h3><ul>{b}</ul></article></div><div class="s175-brief"><p><strong>Для оценки не нужен большой документ.</strong> Пришлите ссылку или текущее состояние, основной сценарий и что должно получиться после запуска.</p><a href="{guide}">Чек-лист перед стартом ↗</a></div></div></section>'''
        marker=None
        for pat in [r'<section class="p129-case',r'<section class="secondary-demand" data-stage172-faq',r'<section class="p129-contact',r'</main>']:
            marker=re.search(pat,x,re.I)
            if marker: break
        if not marker: raise SystemExit('stage175 marker '+slug)
        x=x[:marker.start()]+block+x[marker.start():]
    x=x.replace('</head>',STYLE+'</head>',1)
    fp.write_text(x,encoding='utf-8')

# Freshness for materially expanded commercial pages.
for fname in ('sitemap.xml','sitemap-google.xml'):
    fp=ROOT/fname
    if not fp.exists(): continue
    x=fp.read_text(encoding='utf-8')
    for slug in DATA:
        url=f'{BASE}/{slug}/'
        x=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',r'\g<1>'+TODAY,x,count=1)
    fp.write_text(x,encoding='utf-8')

for slug in DATA:
    text=(ROOT/slug/'index.html').read_text(encoding='utf-8')
    if text.count('data-stage175-depth="true"')!=1: raise SystemExit('stage175 depth '+slug)
    if '/guides/' not in text: raise SystemExit('stage175 guide '+slug)
print(f'stage175 secondary service depth: expanded={len(DATA)}')
