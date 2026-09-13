#!/usr/bin/env python3
from pathlib import Path
import re, sys, html

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

CFG = {
'/telegram-bots/':('01','TELEGRAM PRODUCTS', [('Один понятный сценарий','Пользователь понимает, что делать, а данные доходят до нужного результата.'),('Оплаты, заявки и данные','Подключаются только те сервисы, которые реально нужны процессу.'),('Запуск без привязки','Исходники и настройки остаются у заказчика.')],('/cases/fin-planner/','Fin Planner','/assets/cases/fin-planner/fin-planner-original-800w.webp','Telegram-продукт для ежедневного учета денег.'), [('/telegram-mini-apps/','Нужен интерфейс сложнее бота'),('/guides/telegram-bot-cost/','Как оценить бюджет'),('/project-repair/','Доработать существующего бота')]),
'/telegram-mini-apps/':('02','TELEGRAM MINI APPS',[('Интерфейс внутри Telegram','Когда обычных кнопок бота уже мало.'),('Данные и действия','Формы, каталоги, личные сценарии и интеграции работают как единый продукт.'),('Понятный путь пользователя','Не набор экранов, а законченное действие от входа до результата.')],None,[('/telegram-bots/','Когда достаточно обычного бота'),('/web-development/','Веб-сервис вне Telegram'),('/mvp-development/','Запустить первую версию')]),
'/web-development/':('03','WEB PRODUCTS',[('Интерфейс под задачу','Не шаблон ради картинки, а путь пользователя до нужного действия.'),('Рабочая логика','Формы, кабинеты, роли, данные и интеграции собираются в один продукт.'),('Адаптив и запуск','Версия должна нормально работать не только в макете, но и на реальных устройствах.')],('/cases/sheetpilot-ai/','SheetPilot AI','/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp','Веб-сервис с загрузкой файла, обработкой и выдачей результата.'),[('/mvp-development/','Запустить MVP'),('/api-integrations/','Связать сервисы'),('/project-repair/','Доработать готовый сайт')]),
'/n8n-automation/':('04','AUTOMATION',[('Убрать ручное действие','Сначала выбираем конкретный повторяющийся шаг, а не строим схему ради схемы.'),('Связать рабочие сервисы','CRM, формы, Telegram, таблицы и API участвуют только там, где это полезно.'),('Обработать сбой','Workflow должен понятно вести себя не только в идеальном сценарии.')],None,[('/api-integrations/','Нужна более сложная интеграция'),('/guides/n8n-vs-backend/','n8n или backend'),('/telegram-bots/','Telegram как интерфейс')]),
'/api-integrations/':('05','INTEGRATIONS',[('Данные доходят до места','Заявка, клиент, статус или платеж не теряются между системами.'),('Ошибки видны','Проблемный запрос не должен молча исчезать.'),('Связь можно развивать','Интеграция не превращается в одноразовый хрупкий скрипт.')],('/cases/auto-crm/','CRM автосалона',None,'Внутренняя система, где важен связный путь данных и статусов.'),[('/crm-development/','Своя CRM'),('/n8n-automation/','Автоматизация процессов'),('/backend-development/','Серверная логика')]),
'/crm-development/':('06','CRM / INTERNAL TOOLS',[('Только нужные функции','Без лишней тяжести большой коробочной системы.'),('Один рабочий процесс','Заявки, статусы, сотрудники и данные связаны между собой.'),('Развитие по этапам','Сначала основной контур, затем дополнительные роли и автоматизация.')],('/cases/auto-crm/','CRM автосалона',None,'Рабочий контур для заявок, статусов и данных сотрудников.'),[('/api-integrations/','Интеграции CRM'),('/web-development/','Внутренний веб-интерфейс'),('/guides/custom-crm-or-ready/','Своя CRM или готовая')]),
'/project-repair/':('07','PROJECT REPAIR',[('Сначала причина','Не переписываем всё, пока не понятно, что действительно сломано.'),('Чужой код не проблема','Можно продолжать существующий проект без обязательного старта с нуля.'),('Минимальный рабочий шаг','Исправляем критичный путь и только потом расширяем объем.')],('/cases/taxi-app/','Приложение такси',None,'Пример работы с уже существующим мобильным продуктом.'),[('/telegram-bot-repair/','Доработать Telegram-бота'),('/guides/repair-vs-rewrite/','Чинить или переписывать'),('/web-development/','Продолжить веб-проект')]),
'/telegram-bot-repair/':('08','BOT REPAIR',[('Найти точку сбоя','Сначала воспроизводим проблему и проверяем текущую логику.'),('Сохранить рабочее','Не ломать то, что уже приносит пользу.'),('Передать исправление','Фикс и изменённый код остаются у заказчика.')],('/cases/fin-planner/','Fin Planner','/assets/cases/fin-planner/fin-planner-card-02-720w.webp','Пример сложного Telegram-сценария с данными и состояниями.'),[('/telegram-bots/','Новая разработка'),('/project-repair/','Доработка другого проекта'),('/python-development/','Python-разработка')]),
'/app-development/':('09','MOBILE PRODUCTS',[('Главный сценарий первым','Пользователь должен быстро решить основную задачу приложения.'),('Интерфейс под телефон','Не уменьшенная веб-страница, а нормальный мобильный опыт.'),('Версия, которую можно проверить','Сначала рабочий пользовательский путь, потом расширение продукта.')],('/cases/swift-calendar/','Swift Calendar','/assets/cases/swift-calendar/calendar-original-800w.webp','Нативное iOS-приложение с календарной логикой.'),[('/ios-development/','Нативная iOS-разработка'),('/mvp-development/','Первая версия продукта'),('/project-repair/','Доработка приложения')]),
'/ios-development/':('10','iOS / SWIFT',[('Нативное поведение','Интерфейс ощущается частью iOS, а не компромиссом.'),('Сценарии и состояние','Работаем не только с экранами, но и с логикой между ними.'),('Подготовка к релизу','Делаем проверяемую сборку и исправляем критичные состояния.')],('/cases/swift-calendar/','Swift Calendar','/assets/cases/swift-calendar/calendar-card-02-720w.webp','Календарь на Swift с событиями и продуктовой логикой.'),[('/app-development/','Другие мобильные задачи'),('/mvp-development/','MVP приложения'),('/project-repair/','Доработка готового продукта')]),
'/python-development/':('11','PYTHON DEVELOPMENT',[('Логика, а не язык ради языка','Python выбирается там, где он действительно подходит задаче.'),('Интеграции и данные','Скрипты, боты, API и обработка данных собираются в поддерживаемый процесс.'),('Можно продолжить существующий код','Не обязательно начинать проект заново.')],('/cases/fin-planner/','Fin Planner','/assets/cases/fin-planner/fin-planner-card-01-720w.webp','Telegram-продукт с прикладной бизнес-логикой.'),[('/backend-development/','Backend-разработка'),('/telegram-bots/','Telegram на Python'),('/project-repair/','Доработка Python-проекта')]),
'/backend-development/':('12','BACKEND',[('Серверная логика','Правила, данные и действия находятся там, где ими можно управлять.'),('API для интерфейса','Frontend, бот или приложение получают предсказуемый контракт.'),('Ошибки и состояния','Критичные сценарии не остаются без обработки.')],('/cases/sheetpilot-ai/','SheetPilot AI','/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp','Веб-продукт, где интерфейс связан с серверной обработкой файлов.'),[('/api-integrations/','Интеграции'),('/python-development/','Python'),('/mvp-development/','Backend для MVP')]),
'/mvp-development/':('13','MVP',[('Одна сильная версия','Не строим будущую корпорацию до первого пользователя.'),('Главный сценарий','Собираем путь, который доказывает ценность идеи.'),('Основа для следующего этапа','После проверки понятно, что действительно стоит развивать.')],('/cases/sheetpilot-ai/','SheetPilot AI','/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp','Рабочий продукт с публичным демо и понятным пользовательским сценарием.'),[('/web-development/','Веб-MVP'),('/app-development/','Мобильный MVP'),('/guides/development-cost/','Оценка стоимости')]),
'/ai-automation/':('14','AI AUTOMATION',[('AI внутри процесса','Модель решает конкретный шаг, а не становится декоративной надписью.'),('Контроль результата','Нужны понятные входы, выходы и поведение при ошибке.'),('Интеграция с текущей работой','Автоматизация должна встраиваться в используемые инструменты.')],('/cases/sheetpilot-ai/','SheetPilot AI','/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp','AI-функция встроена в понятный пользовательский сценарий обработки файла.'),[('/n8n-automation/','Автоматизация процессов'),('/api-integrations/','Связать сервисы'),('/mvp-development/','AI-функция в MVP')]),
'/development/':('15','DIGITAL DEVELOPMENT',[('Сначала задача','Формат продукта выбирается после того, как понятен результат.'),('Один ответственный контур','Интерфейс, логика и интеграции рассматриваются как части одного продукта.'),('Запуск по этапам','Большую задачу можно разбить на проверяемые законченные части.')],('/cases/sheetpilot-ai/','SheetPilot AI','/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp','Пример продукта от интерфейса до рабочей серверной логики.'),[('/services/','Все направления'),('/cases/','Смотреть кейсы'),('/project-repair/','Продолжить готовый проект')]),
}

def page(route): return ROOT / route.strip('/') / 'index.html'
def strip_tags(s): return re.sub(r'<[^>]+>','',s).replace('&nbsp;',' ').strip()

def extract_hero(src):
    hero = re.search(r'<section[^>]*class="[^"]*s48-hero[^"]*"[^>]*>(.*?)</section>', src, re.S|re.I)
    chunk = hero.group(1) if hero else src
    h = re.search(r'<h1\b[^>]*>(.*?)</h1>', chunk, re.S|re.I)
    p = re.search(r'<p\b[^>]*class="[^"]*(?:s48-lead|lead)[^"]*"[^>]*>(.*?)</p>', chunk, re.S|re.I)
    if not p: p = re.search(r'<p\b[^>]*>(.*?)</p>', chunk, re.S|re.I)
    if not h or not p: raise SystemExit('stage129: hero extraction failed')
    return h.group(1).strip(), p.group(1).strip()

def build(route, cfg, old):
    no,label,outcomes,case,related=cfg
    title,lead=extract_hero(old)
    outcome_html=''.join(f'<article class="p129-outcome"><span>0{i}</span><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>' for i,(t,d) in enumerate(outcomes,1))
    board=''.join(f'<li>{html.escape(t)}</li>' for t,_ in outcomes)
    rel=''.join(f'<a href="{u}"><span>Следующий шаг</span><strong>{html.escape(t)}</strong><b>↗</b></a>' for u,t in related)
    if case:
        u,name,img,desc=case
        if img:
            case_html=f'''<section class="p129-case"><div class="p129-shell"><a class="p129-case-card" href="{u}"><div class="p129-case-media"><img src="{img}" alt="{html.escape(name)}" loading="lazy" decoding="async"></div><div class="p129-case-copy"><span class="p129-kicker"><i></i>REAL WORK</span><h2>{html.escape(name)}</h2><p>{html.escape(desc)}</p><span class="p129-textlink">Открыть кейс ↗</span></div></a></div></section>'''
        else:
            case_html=f'''<section class="p129-case"><div class="p129-shell"><div class="p129-no-case"><div><span class="p129-kicker"><i></i>REAL WORK</span><h2>{html.escape(name)}</h2><p>{html.escape(desc)}</p></div><a class="p129-btn" href="{u}">Открыть кейс ↗</a></div></div></section>'''
    else:
        case_html='''<section class="p129-case"><div class="p129-shell"><div class="p129-no-case"><div><span class="p129-kicker"><i></i>WORKING FORMAT</span><h2>Сначала один законченный результат.</h2><p>Большую задачу разбиваю на этапы так, чтобы первый результат можно было проверить отдельно.</p></div><a class="p129-btn" href="/cases/">Смотреть работы ↗</a></div></div></section>'''
    return f'''<main id="main-content" class="p129-service" data-stage129-service="true">
<section class="p129-svc-hero"><div class="p129-shell p129-svc-grid"><div class="p129-svc-copy"><p class="p129-kicker"><i></i>{html.escape(label)}</p><h1>{title}</h1><p class="p129-lead">{lead}</p><div class="p129-svc-actions"><a class="p129-btn" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить задачу ↗</a><a class="p129-textlink" href="#result">Что получится ↓</a></div></div><aside class="p129-svc-board"><span class="p129-svc-no">{no}</span><h2>Фокус на результате.</h2><ul>{board}</ul></aside></div></section>
<section class="p129-outcomes" id="result"><div class="p129-shell"><div class="p129-section-head"><p class="p129-kicker">RESULT / {no}</p><h2>Не набор технологий. <span>Три вещи, которые должны работать.</span></h2></div><div class="p129-outcome-list">{outcome_html}</div></div></section>
{case_html}
<section class="p129-related"><div class="p129-shell"><div class="p129-section-head"><p class="p129-kicker">EXPLORE</p><h2>Если задача рядом, <span>вот куда смотреть дальше.</span></h2></div><div class="p129-related-grid">{rel}</div></div></section>
<section class="p129-contact"><div class="p129-shell"><div class="p129-contact-card"><div><p class="p129-kicker">START</p><h2>Покажите, что должно заработать.</h2><p>Ссылка, код, макет, описание ошибки или просто идея. Для первого сообщения достаточно текущего состояния и желаемого результата.</p></div><a class="p129-btn" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Написать в Telegram ↗</a></div></div></section>
</main>'''

changed=[]
for route,cfg in CFG.items():
    p=page(route)
    if not p.is_file(): raise SystemExit(f'stage129: missing {route}')
    src=p.read_text(encoding='utf-8')
    new_main=build(route,cfg,src)
    src,n=re.subn(r'<main\b[^>]*id="main-content"[^>]*>.*?</main>',new_main,src,count=1,flags=re.S|re.I)
    if n!=1: raise SystemExit(f'stage129: main replacement failed {route}')
    p.write_text(src,encoding='utf-8'); changed.append(route)
print(f'stage129 service rebuild: {len(changed)} service pages replaced with premium result-led DOM')
