#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html as html_lib
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route_file(route: str) -> Path:
    return root / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def replace_main(route: str, main_html: str) -> None:
    path = route_file(route)
    if not path.is_file():
        raise SystemExit(f"stage44: missing {route}: {path}")
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r'<main\b[^>]*id="main-content"[^>]*>.*?</main>', re.S | re.I)
    text, count = pattern.subn(main_html, text, count=1)
    if count != 1:
        raise SystemExit(f"stage44: main-content not replaced: {route}")
    path.write_text(text, encoding="utf-8")


def set_head(route: str, *, title: str, description: str) -> None:
    path = route_file(route)
    text = path.read_text(encoding="utf-8")
    escaped_title = html_lib.escape(title, quote=True)
    escaped_desc = html_lib.escape(description, quote=True)
    text, n1 = re.subn(r'<title>.*?</title>', f'<title>{escaped_title}</title>', text, count=1, flags=re.S)
    if n1 != 1:
        raise SystemExit(f"stage44: title not found: {route}")
    fields = (
        ('name', 'description', escaped_desc),
        ('property', 'og:title', escaped_title),
        ('property', 'og:description', escaped_desc),
        ('name', 'twitter:title', escaped_title),
        ('name', 'twitter:description', escaped_desc),
    )
    for attr, key, value in fields:
        pat = re.compile(rf'(<meta\s+content=")[^"]*("\s+{attr}="{re.escape(key)}"\s*/?>)', re.I)
        text, _ = pat.subn(lambda m: m.group(1) + value + m.group(2), text, count=1)
    path.write_text(text, encoding="utf-8")


home_main = r'''<main id="main-content" data-stage44-home="true">
<section class="s44-hero" aria-labelledby="s44-hero-title">
  <div class="container s44-hero__grid">
    <div class="s44-hero__copy">
      <div class="s44-kicker" data-nosnippet="">ALEXUYS · DIGITAL DEVELOPMENT</div>
      <h1 id="s44-hero-title">Сайты, приложения, Telegram-боты <em>и автоматизация.</em></h1>
      <p class="s44-lead">Разрабатываю цифровые продукты с нуля и подключаюсь к уже существующим проектам. Веб-сервисы, мобильные приложения, боты, CRM, API-интеграции и автоматизация — напрямую с разработчиком, без передачи задачи между менеджерами.</p>
      <div class="s44-actions">
        <a class="button primary" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Обсудить задачу в Telegram ↗</a>
        <a class="button" href="#projects">Смотреть реальные проекты ↓</a>
      </div>
      <div class="s44-proofline" aria-label="Проверяемые факты">
        <a href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank"><strong>20</strong><span>публичных отзывов на Freelance.ru</span></a>
        <a href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank"><strong>9 / 10</strong><span>профессионализм и коммуникация</span></a>
        <div><strong>6 лет</strong><span>опыта в публичном профиле</span></div>
        <a href="/cases/"><strong>5</strong><span>подробных кейсов на сайте</span></a>
      </div>
    </div>
    <div class="s44-hero__visual" data-nosnippet="">
      <a class="s44-shot s44-shot--main" href="/cases/fin-planner/" aria-label="Открыть кейс Telegram-бота Фин Планер">
        <img src="/assets/cases/fin-planner/fin-planner-card-01-720w.webp" width="720" height="900" alt="Интерфейс Telegram-бота Фин Планер" decoding="async" fetchpriority="high"/>
        <span><b>FIN PLANNER</b><small>Telegram · product case</small></span>
      </a>
      <a class="s44-shot s44-shot--side" href="/cases/swift-calendar/" aria-label="Открыть кейс iOS-календаря на Swift">
        <img src="/assets/cases/swift-calendar/calendar-card-01-720w.webp" width="720" height="900" alt="Интерфейс iOS-календаря на Swift" loading="lazy" decoding="async"/>
        <span><b>SWIFT CALENDAR</b><small>iOS · real UI</small></span>
      </a>
      <div class="s44-visual-note"><i></i><span>Не концепты ради картинки — интерфейсы из реальных проектов.</span></div>
    </div>
  </div>
</section>

<section class="s44-section" aria-labelledby="choose-title">
  <div class="container">
    <div class="s44-section-head"><span class="s44-index" data-nosnippet="">01 / ЗАДАЧА</span><div><h2 id="choose-title">Начните не с технологии. <em>С результата.</em></h2><p>Если уже знаете стек — отлично. Если нет, достаточно выбрать, что должно заработать. Подход и технологии подбираются под задачу, а не наоборот.</p></div></div>
    <div class="s44-route-grid">
      <a class="s44-route s44-route--wide" href="/web-development/"><span>WEB</span><h3>Нужен сайт или веб-сервис</h3><p>Лендинг, каталог, кабинет, внутренний интерфейс, SaaS/MVP или полноценный веб-продукт.</p><b>Веб-разработка ↗</b></a>
      <a class="s44-route" href="/telegram-bots/"><span>TELEGRAM</span><h3>Нужен бот или Mini App</h3><p>Заявки, оплаты, подписки, CRM/API, база данных, служебная логика.</p><b>Telegram-разработка ↗</b></a>
      <a class="s44-route" href="/app-development/"><span>MOBILE</span><h3>Нужно приложение</h3><p>Мобильный пользовательский сценарий, iOS/Swift или кроссплатформенная реализация.</p><b>Приложения ↗</b></a>
      <a class="s44-route" href="/n8n-automation/"><span>AUTOMATION</span><h3>Нужно убрать ручную рутину</h3><p>n8n/Make, webhooks, CRM, Telegram, таблицы, уведомления и связанные процессы.</p><b>Автоматизация ↗</b></a>
      <a class="s44-route" href="/api-integrations/"><span>API / CRM</span><h3>Нужно связать несколько систем</h3><p>API, обмен данными, CRM, платежи, внешние сервисы и обработка ошибок интеграции.</p><b>Интеграции ↗</b></a>
      <a class="s44-route s44-route--accent" href="/project-repair/"><span>EXISTING PROJECT</span><h3>Проект уже есть, но застрял</h3><p>Чужой код, ошибка, сломанная форма, интеграция, адаптив или незавершённый релиз.</p><b>Доработка проекта ↗</b></a>
    </div>
  </div>
</section>

<section class="s44-section s44-projects" id="projects" aria-labelledby="projects-title">
  <div class="container">
    <div class="s44-section-head"><span class="s44-index" data-nosnippet="">02 / ПРОЕКТЫ</span><div><h2 id="projects-title">Показываю не стек. <em>Показываю, что было собрано.</em></h2><p>Подробные кейсы нужны, чтобы до обращения можно было оценить уровень интерфейса, сложность логики и тип задач, с которыми уже работал.</p></div></div>
    <div class="s44-case-grid">
      <a class="s44-case s44-case--visual" href="/cases/fin-planner/"><div class="s44-case__image"><img src="/assets/cases/fin-planner/fin-planner-card-02-720w.webp" width="720" height="900" loading="lazy" decoding="async" alt="Экран Telegram-бота Фин Планер"/></div><div class="s44-case__body"><span>TELEGRAM · FINANCE · AUTOMATION</span><h3>Фин Планер</h3><p>Telegram-продукт для бюджета: расходы, регулярные операции, цели, отчёты и пользовательские сценарии внутри бота.</p><b>Открыть полный кейс ↗</b></div></a>
      <a class="s44-case s44-case--visual" href="/cases/swift-calendar/"><div class="s44-case__image"><img src="/assets/cases/swift-calendar/calendar-card-02-720w.webp" width="720" height="900" loading="lazy" decoding="async" alt="Экран iOS-календаря на Swift"/></div><div class="s44-case__body"><span>iOS · SWIFT · PRODUCT UI</span><h3>Календарь на Swift</h3><p>Нативное iOS-приложение с календарными сценариями, событиями, продуктовой логикой и подпиской.</p><b>Открыть полный кейс ↗</b></div></a>
      <div class="s44-case-stack">
        <a href="/cases/auto-crm/"><span>CRM · INTERNAL SYSTEM</span><h3>CRM автосалона</h3><p>Рабочий контур для заявок, статусов и данных сотрудников.</p><b>Кейс ↗</b></a>
        <a href="/cases/factory-catalog/"><span>B2B · WEB</span><h3>Каталог завода</h3><p>Корпоративный каталог продукции, структура данных и заявки.</p><b>Кейс ↗</b></a>
        <a href="/cases/taxi-app/"><span>MOBILE · APP</span><h3>Приложение такси</h3><p>Мобильный интерфейс и пользовательские сценарии сервиса поездок.</p><b>Кейс ↗</b></a>
      </div>
    </div>
    <div class="s44-inline-actions"><a href="/cases/">Все кейсы →</a><a href="/services/">Все направления →</a></div>
  </div>
</section>

<section class="s44-section" aria-labelledby="difference-title">
  <div class="container">
    <div class="s44-section-head"><span class="s44-index" data-nosnippet="">03 / ПОДХОД</span><div><h2 id="difference-title">Меньше обещаний. <em>Больше проверяемых вещей.</em></h2><p>На странице должно быть понятно не только «что умею», но и как будет выглядеть работа после первого сообщения.</p></div></div>
    <div class="s44-value-grid">
      <article><span>01</span><h3>Напрямую с разработчиком</h3><p>Обсуждение задачи, оценка и реализация не проходят через цепочку менеджеров и посредников.</p></article>
      <article><span>02</span><h3>Можно прийти с чужим кодом</h3><p>Не обязательно начинать проект заново. Сначала смотрю текущее состояние и определяю минимальный рабочий следующий шаг.</p></article>
      <article><span>03</span><h3>Результат фиксируется до старта</h3><p>Для первого этапа определяем, какой сценарий должен заработать и где заканчивается согласованный объём.</p></article>
      <article><span>04</span><h3>Проект остаётся у заказчика</h3><p>Исходники, workflow и необходимые доступы передаются в согласованном объёме — без искусственной привязки к исполнителю.</p></article>
    </div>
    <div class="s44-trust-card">
      <div><span class="s44-kicker">НЕЗАВИСИМОЕ ПОДТВЕРЖДЕНИЕ</span><h3>Отзывы находятся не на этом сайте.</h3><p>Публичный профиль Freelance.ru можно открыть до обращения: 20 отзывов, оценки 9/10 по профессионализму и коммуникации, 6 лет опыта в профиле. Сайт использует внешнюю репутацию как проверяемый источник, а не рисует собственный рейтинг.</p></div>
      <div class="s44-trust-actions"><a class="button primary" href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank">Проверить профиль ↗</a><a class="button" href="https://freelance.ru/reviews/gglalex/" rel="noopener noreferrer" target="_blank">Читать отзывы ↗</a></div>
    </div>
  </div>
</section>

<section class="s44-section" aria-labelledby="budget-title">
  <div class="container">
    <div class="s44-section-head"><span class="s44-index" data-nosnippet="">04 / БЮДЖЕТ</span><div><h2 id="budget-title">Ориентир до переписки. <em>Не жёсткий тариф.</em></h2><p>Цена зависит от объёма, состояния проекта и интеграций. Эти значения нужны только для понимания порядка бюджета — крупные проекты не ограничиваются указанными рамками.</p></div></div>
    <div class="s44-price-grid">
      <article><span>ЛОКАЛЬНАЯ ЗАДАЧА</span><strong>от 5 000 ₽</strong><h3>Доработка / исправление</h3><p>Одна понятная проблема в существующем сайте, боте, интеграции или коде.</p><a href="/project-repair/">Подробнее →</a></article>
      <article><span>ПЕРВЫЙ ЭТАП</span><strong>от 15 000 ₽</strong><h3>Новый рабочий сценарий</h3><p>Бот, небольшая веб-реализация, workflow или другой законченный первый результат.</p><a href="/services/">Выбрать направление →</a></article>
      <article><span>СВЯЗАННАЯ СИСТЕМА</span><strong>от 30 000 ₽</strong><h3>Несколько частей проекта</h3><p>API, CRM, backend, база данных, несколько пользовательских сценариев или интеграций.</p><a href="/api-integrations/">Интеграции →</a></article>
      <article class="s44-price--custom"><span>PRODUCT / MVP</span><strong>по задаче</strong><h3>Полноценный продукт</h3><p>Приложение, веб-сервис, CRM, MVP или проект с несколькими этапами и ролями.</p><a href="/development/">Разработка →</a></article>
    </div>
  </div>
</section>

<section class="s44-section" aria-labelledby="process-title">
  <div class="container">
    <div class="s44-section-head"><span class="s44-index" data-nosnippet="">05 / ПРОЦЕСС</span><div><h2 id="process-title">От сообщения до запуска <em>без лишних ритуалов.</em></h2><p>Большое техническое задание для первого контакта не обязательно. Достаточно понять исходную точку и желаемый результат.</p></div></div>
    <ol class="s44-process">
      <li><span>01</span><div><h3>Вы присылаете задачу</h3><p>Описание своими словами, ссылку, скриншот, макет или репозиторий — в зависимости от того, что уже есть.</p></div></li>
      <li><span>02</span><div><h3>Определяем первый результат</h3><p>Разделяем обязательное и второстепенное, после чего становится понятен объём, срок и порядок бюджета.</p></div></li>
      <li><span>03</span><div><h3>Реализация и проверка</h3><p>Работа идёт по согласованному сценарию. Проверяется не только экран, но и фактическое прохождение пользовательского пути.</p></div></li>
      <li><span>04</span><div><h3>Запуск и передача</h3><p>Деплой, необходимые доступы и исходники передаются в согласованном формате; дальше проект можно развивать следующим этапом.</p></div></li>
    </ol>
  </div>
</section>

<section class="s44-section s44-brief-section" aria-labelledby="brief-title" id="brief">
  <div class="container">
    <div class="s44-section-head"><span class="s44-index" data-nosnippet="">06 / СТАРТ</span><div><h2 id="brief-title">Опишите задачу <em>в четырёх полях.</em></h2><p>Форма ничего не отправляет на сервер. Она только собирает текст и открывает Telegram с готовым сообщением — данные остаются у вас до перехода.</p></div></div>
    <form class="s44-brief" id="s44-brief-form">
      <label><span>Что нужно сделать</span><select name="type"><option>Сайт / веб-сервис</option><option>Telegram-бот / Mini App</option><option>Мобильное приложение</option><option>Автоматизация n8n / Make</option><option>API / CRM-интеграция</option><option>Доработка существующего проекта</option><option>Другое / пока не знаю</option></select></label>
      <label class="s44-brief__wide"><span>Задача своими словами</span><textarea name="task" required rows="5" placeholder="Что должно работать в итоге?"></textarea></label>
      <label><span>Что уже есть</span><input name="current" type="text" placeholder="Сайт, код, Figma, ТЗ или только идея"/></label>
      <label><span>Срок / бюджет, если есть</span><input name="limits" type="text" placeholder="Например: до 2 недель / ориентир 30–50 тыс."/></label>
      <div class="s44-brief__footer"><p>Можно оставить часть полей пустыми. Никакой регистрации.</p><button class="button primary" type="submit">Собрать сообщение в Telegram ↗</button></div>
    </form>
  </div>
</section>
</main>'''

services_main = r'''<main id="main-content" data-stage44-services="true">
<section class="s44-services-hero">
  <div class="container">
    <div class="s44-kicker" data-nosnippet="">УСЛУГИ · ВЫБОР ПО РЕЗУЛЬТАТУ</div>
    <h1>Что должно <em>заработать?</em></h1>
    <p>Не обязательно выбирать технологию до разговора. Здесь услуги сгруппированы по результату: новый продукт, автоматизация, интеграция или доработка уже существующего проекта.</p>
    <div class="s44-actions"><a class="button primary" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Описать задачу ↗</a><a class="button" href="/cases/">Сначала посмотреть кейсы</a></div>
  </div>
</section>
<section class="s44-section">
  <div class="container">
    <div class="s44-service-map">
      <a class="s44-service-map__item s44-service-map__item--lead" href="/web-development/"><span>01 · WEB</span><h2>Сайт, веб-сервис или MVP</h2><p>От лендинга и каталога до кабинета, внутренней системы и полноценного веб-продукта.</p><div><b>от 15 000 ₽ за первый этап</b><i>Подробнее ↗</i></div></a>
      <a class="s44-service-map__item" href="/telegram-bots/"><span>02 · TELEGRAM</span><h2>Telegram-бот или Mini App</h2><p>Заявки, платежи, подписки, CRM/API, базы данных и продуктовая логика.</p><div><b>от 15 000 ₽</b><i>Подробнее ↗</i></div></a>
      <a class="s44-service-map__item" href="/app-development/"><span>03 · MOBILE</span><h2>Мобильное приложение</h2><p>Пользовательские сценарии для смартфона: iOS/Swift и кроссплатформенная разработка.</p><div><b>оценка по объёму</b><i>Подробнее ↗</i></div></a>
      <a class="s44-service-map__item" href="/n8n-automation/"><span>04 · AUTOMATION</span><h2>Автоматизация процесса</h2><p>n8n/Make, webhooks, формы, CRM, Telegram, таблицы и уведомления без ручного переноса данных.</p><div><b>от 15 000 ₽</b><i>Подробнее ↗</i></div></a>
      <a class="s44-service-map__item" href="/api-integrations/"><span>05 · INTEGRATIONS</span><h2>API и связь систем</h2><p>Обмен данными между сервисами, CRM, платежами, backend и внешними API.</p><div><b>оценка после схемы</b><i>Подробнее ↗</i></div></a>
      <a class="s44-service-map__item s44-service-map__item--repair" href="/project-repair/"><span>06 · EXISTING PROJECT</span><h2>Доработка чужого или незавершённого проекта</h2><p>Ошибка, форма, адаптив, интеграция, новый функционал, старый код или проект, который нужно довести до релиза.</p><div><b>от 5 000 ₽</b><i>Подробнее ↗</i></div></a>
    </div>
  </div>
</section>
<section class="s44-section">
  <div class="container">
    <div class="s44-section-head"><span class="s44-index" data-nosnippet="">ЕСЛИ ЗАДАЧА СЛОЖНЕЕ</span><div><h2>Отдельные направления <em>для точного входа.</em></h2><p>Эти страницы раскрывают конкретный стек или тип проекта. Они полезны, если вы уже знаете, что именно требуется.</p></div></div>
    <div class="s44-special-grid">
      <a href="/crm-development/"><strong>CRM-разработка</strong><span>Внутренние системы, заявки, статусы и процессы →</span></a>
      <a href="/ai-automation/"><strong>AI-автоматизация</strong><span>AI-шаги внутри рабочего процесса и интеграций →</span></a>
      <a href="/ios-development/"><strong>iOS / Swift</strong><span>Нативные приложения и существующие iOS-проекты →</span></a>
      <a href="/python-development/"><strong>Python</strong><span>Backend, скрипты, парсинг и сервисная логика →</span></a>
      <a href="/backend-development/"><strong>Backend</strong><span>API, базы данных, авторизация и серверная часть →</span></a>
      <a href="/mvp-development/"><strong>MVP</strong><span>Первый рабочий релиз продукта без лишнего объёма →</span></a>
      <a href="/telegram-mini-apps/"><strong>Telegram Mini Apps</strong><span>Интерфейс внутри Telegram поверх backend/API →</span></a>
      <a href="/development/"><strong>Разработка под задачу</strong><span>Если проект не помещается в одну категорию →</span></a>
    </div>
  </div>
</section>
<section class="s44-section">
  <div class="container">
    <div class="s44-service-decision">
      <div><span class="s44-kicker">НЕ ЗНАЕТЕ, КУДА ОТНЕСТИ ЗАДАЧУ?</span><h2>Это нормально. <em>Можно начать с проблемы.</em></h2><p>Например: «форма перестала отправлять заявки», «нужно автоматизировать перенос заказов в CRM», «есть дизайн, нужен рабочий продукт» или «бот готов на 70%, нужно закончить». Этого уже достаточно для первого разбора.</p></div>
      <div class="s44-trust-actions"><a class="button primary" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Написать в Telegram ↗</a><a class="button" href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank">Проверить Freelance.ru ↗</a></div>
    </div>
    <div class="s44-proofline s44-proofline--services"><a href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank"><strong>20</strong><span>публичных отзывов</span></a><div><strong>6 лет</strong><span>опыта в профиле</span></div><a href="/cases/"><strong>5</strong><span>подробных кейсов</span></a><a href="/project-repair/"><strong>от 5 000 ₽</strong><span>небольшая доработка</span></a></div>
  </div>
</section>
</main>'''

replace_main("/", home_main)
replace_main("/services/", services_main)
set_head(
    "/",
    title="Сайты, приложения, Telegram-боты и автоматизация | Alexuys",
    description="Разработка сайтов, веб-сервисов, Telegram-ботов, мобильных приложений, автоматизации и API-интеграций. Реальные кейсы, 20 отзывов на Freelance.ru и прямой контакт с разработчиком.",
)
set_head(
    "/services/",
    title="Разработка сайтов, ботов, приложений и автоматизации | Alexuys",
    description="Услуги разработки под задачу: сайты и веб-сервисы, Telegram-боты, приложения, n8n/Make, API/CRM-интеграции и доработка существующих проектов.",
)

# Add a concise orientation block to the four highest-intent service pages. Stage 42
# already provides commercial price/result proof; this layer improves information
# scent without duplicating long SEO prose.
service_orientation = {
    "/telegram-bots/": (
        "Когда Telegram — правильный интерфейс",
        "Бот подходит, когда пользователь уже находится в Telegram, а процесс можно провести через сообщения, кнопки, формы, Mini App и уведомления. Если нужен сложный публичный каталог или SEO-трафик, веб-интерфейс может быть лучше — это определяется до разработки.",
        (("Заявки и запись", "Сбор данных, подтверждения, статусы и уведомления."), ("Оплата и подписка", "Платёжный сценарий, доступы и события после оплаты."), ("CRM / API", "Передача данных и синхронизация с внешней системой.")),
    ),
    "/web-development/": (
        "Веб-разработка от страницы до продукта",
        "Первый релиз не обязан включать весь будущий сервис. Можно начать с страницы, каталога или одного ключевого пользовательского сценария, а архитектуру оставить готовой к следующему этапу.",
        (("Маркетинговый сайт", "Структура, адаптив, формы, аналитика и SEO-ready основа."), ("Веб-сервис", "Интерфейс, backend/API, данные, авторизация и роли."), ("MVP", "Минимальный законченный продукт для проверки идеи и дальнейшего развития.")),
    ),
    "/n8n-automation/": (
        "Автоматизация должна убирать конкретное ручное действие",
        "Хороший workflow начинается не со списка сервисов, а с понятного события и результата: появилась заявка → данные проверились → попали в CRM → ответственный получил уведомление → ошибка не потерялась.",
        (("Вход", "Webhook, форма, сообщение, расписание или событие в сервисе."), ("Логика", "Проверка, преобразование данных, ветвление и вызовы API."), ("Результат", "CRM, таблица, Telegram, email или другое конечное действие.")),
    ),
    "/project-repair/": (
        "Не обязательно переписывать проект целиком",
        "Сначала определяется причина и минимальный объём, который возвращает нужный сценарий в рабочее состояние. Переписывание имеет смысл только когда оно действительно дешевле и безопаснее точечной доработки.",
        (("Прислать", "Ссылку, скриншот ошибки, репозиторий или краткое описание."), ("Проверить", "Где ломается сценарий и какие части проекта он затрагивает."), ("Исправить", "Согласованный участок с проверкой результата после изменения.")),
    ),
}

for route, (title, intro, cards) in service_orientation.items():
    path = route_file(route)
    if not path.is_file():
        raise SystemExit(f"stage44: missing service route: {route}")
    text = path.read_text(encoding="utf-8")
    if 'data-stage44-orientation="true"' in text:
        continue
    card_html = ''.join(f'<article><h3>{html_lib.escape(h)}</h3><p>{html_lib.escape(p)}</p></article>' for h, p in cards)
    block = f'''<section class="s44-orientation" data-stage44-orientation="true"><div class="container"><div class="s44-orientation__head"><span class="s44-kicker">БЫСТРАЯ ПРОВЕРКА СЦЕНАРИЯ</span><h2>{title}</h2><p>{intro}</p></div><div class="s44-orientation__grid">{card_html}</div></div></section>'''
    # Prefer insertion before Stage 42 packages/trust so the page reads: hero → proof →
    # decision explanation → detailed scope/prices → external trust → contact.
    markers = ('<section class="section market-packages"', '<section class="verified-trust', '<section class="contact"', '</main>')
    marker = next((m for m in markers if m in text), None)
    if not marker:
        raise SystemExit(f"stage44: no service insertion marker: {route}")
    text = text.replace(marker, block + '\n' + marker, 1)
    path.write_text(text, encoding="utf-8")

css = root / "assets" / "site-enhancements.css"
if not css.is_file():
    raise SystemExit("stage44: site-enhancements.css missing")
css_text = css.read_text(encoding="utf-8")
if "/* stage44 experience rebuild */" not in css_text:
    css_text += r'''

/* stage44 experience rebuild */
.s44-hero{padding:clamp(4rem,8vw,8rem) 0 clamp(5rem,9vw,9rem);border-bottom:1px solid rgba(255,255,255,.075);overflow:hidden}.s44-hero .container,.s44-section .container,.s44-services-hero .container,.s44-orientation .container{width:min(100%,92rem);margin-inline:auto;padding-inline:clamp(1.1rem,4vw,4.5rem)}.s44-hero__grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(24rem,.95fr);gap:clamp(2.2rem,5vw,6rem);align-items:center}.s44-kicker,.s44-index{font:800 .64rem/1.3 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.105em;text-transform:uppercase;color:#78828d}.s44-hero h1{margin:1rem 0 0;max-width:12.8ch;font-size:clamp(3.4rem,6.9vw,7.1rem);line-height:.9;letter-spacing:-.066em}.s44-hero h1 em,.s44-section h2 em,.s44-services-hero h1 em,.s44-service-decision h2 em{font-style:normal;color:#929aa5}.s44-lead{max-width:52rem;margin:1.5rem 0 0;color:#9da5ae;font-size:clamp(1rem,1.45vw,1.18rem);line-height:1.72}.s44-actions{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.8rem}.s44-proofline{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.55rem;margin-top:2rem}.s44-proofline>a,.s44-proofline>div{display:block;padding:.85rem .9rem;border-top:1px solid rgba(255,255,255,.11);text-decoration:none}.s44-proofline strong{display:block;font-size:1.25rem;letter-spacing:-.04em}.s44-proofline span{display:block;margin-top:.18rem;color:#7f8994;font-size:.68rem;line-height:1.35}.s44-hero__visual{position:relative;min-height:39rem}.s44-shot{position:absolute;display:block;overflow:hidden;border:1px solid rgba(255,255,255,.13);border-radius:1.45rem;background:#0d1117;box-shadow:0 30px 85px rgba(0,0,0,.36);text-decoration:none}.s44-shot img{display:block;width:100%;height:100%;object-fit:cover}.s44-shot>span{position:absolute;left:.8rem;right:.8rem;bottom:.8rem;padding:.68rem .75rem;border:1px solid rgba(255,255,255,.12);border-radius:.8rem;background:rgba(7,9,12,.78);backdrop-filter:blur(16px)}.s44-shot b,.s44-shot small{display:block}.s44-shot b{font-size:.72rem;letter-spacing:.05em}.s44-shot small{margin-top:.12rem;color:#8c96a1;font-size:.62rem}.s44-shot--main{width:min(72%,25rem);height:34rem;left:0;top:1.5rem;transform:rotate(-2.2deg)}.s44-shot--side{width:min(58%,20rem);height:27rem;right:0;top:7rem;transform:rotate(4deg)}.s44-shot:hover{z-index:4;transform:translateY(-5px) rotate(0)}.s44-visual-note{position:absolute;right:0;bottom:.6rem;width:min(75%,23rem);display:flex;gap:.65rem;align-items:flex-start;color:#8f98a3;font-size:.72rem;line-height:1.45}.s44-visual-note i{width:.58rem;height:.58rem;margin-top:.18rem;border-radius:50%;background:#c9ff4a;box-shadow:0 0 0 .35rem rgba(201,255,74,.08);flex:0 0 auto}.s44-section{padding:clamp(5rem,9vw,9rem) 0;border-bottom:1px solid rgba(255,255,255,.075)}.s44-section-head{display:grid;grid-template-columns:minmax(8rem,.28fr) minmax(0,1.72fr);gap:clamp(1.4rem,4vw,4rem);align-items:start;margin-bottom:2.2rem}.s44-section h2,.s44-section-head h2{margin:0;max-width:16ch;font-size:clamp(2.5rem,5.3vw,5.5rem);line-height:.94;letter-spacing:-.058em}.s44-section-head p{max-width:54rem;margin:1rem 0 0;color:#929ba5;line-height:1.7}.s44-route-grid{display:grid;grid-template-columns:repeat(12,1fr);gap:.65rem}.s44-route{grid-column:span 4;min-height:16rem;display:flex;flex-direction:column;padding:1.3rem;border:1px solid rgba(255,255,255,.1);border-radius:1.2rem;background:linear-gradient(145deg,#11151b,#0c1015);text-decoration:none;transition:transform .2s ease,border-color .2s ease,background .2s ease}.s44-route--wide{grid-column:span 8}.s44-route--accent{background:radial-gradient(circle at 100% 0,rgba(201,255,74,.10),transparent 17rem),linear-gradient(145deg,#12171b,#0c1014)}.s44-route:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.2)}.s44-route>span{color:#78828d;font:800 .61rem/1 ui-monospace,monospace;letter-spacing:.08em}.s44-route h3{margin:auto 0 .7rem;max-width:15ch;font-size:clamp(1.55rem,2.7vw,2.6rem);line-height:1;letter-spacing:-.045em}.s44-route p{margin:0;max-width:38rem;color:#8e98a3;font-size:.84rem}.s44-route b{margin-top:1rem;color:#c8cdd2;font-size:.72rem}.s44-case-grid{display:grid;grid-template-columns:repeat(12,1fr);gap:.7rem}.s44-case{border:1px solid rgba(255,255,255,.1);border-radius:1.25rem;background:#0d1116;text-decoration:none;overflow:hidden}.s44-case--visual{grid-column:span 5;display:grid;grid-template-columns:minmax(0,.44fr) minmax(0,.56fr);min-height:26rem}.s44-case__image{min-height:100%;overflow:hidden;background:#080a0e}.s44-case__image img{width:100%;height:100%;display:block;object-fit:cover}.s44-case__body{padding:1.25rem;display:flex;flex-direction:column}.s44-case__body>span,.s44-case-stack span{color:#78828d;font:800 .58rem/1.2 ui-monospace,monospace;letter-spacing:.06em}.s44-case__body h3,.s44-case-stack h3{margin:auto 0 .6rem;font-size:clamp(1.45rem,2.5vw,2.5rem);line-height:1;letter-spacing:-.045em}.s44-case__body p,.s44-case-stack p{margin:0;color:#8f98a3;font-size:.8rem;line-height:1.55}.s44-case__body b,.s44-case-stack b{margin-top:.9rem;font-size:.7rem}.s44-case-stack{grid-column:span 2;display:grid;gap:.7rem}.s44-case-stack a{display:flex;flex-direction:column;min-height:8rem;padding:1rem;border:1px solid rgba(255,255,255,.1);border-radius:1rem;background:#0d1116;text-decoration:none}.s44-case-stack h3{margin:auto 0 .4rem;font-size:1.05rem}.s44-case-stack p{font-size:.7rem}.s44-case-stack b{margin-top:.5rem}.s44-case:hover,.s44-case-stack a:hover{border-color:rgba(255,255,255,.2)}.s44-inline-actions{display:flex;gap:1rem;margin-top:1rem}.s44-inline-actions a{color:#aab1b8;font-size:.76rem}.s44-value-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.65rem}.s44-value-grid article{min-height:15rem;padding:1.2rem;border:1px solid rgba(255,255,255,.1);border-radius:1.1rem;background:#0d1116}.s44-value-grid article>span{color:#737d88;font:800 .6rem/1 ui-monospace,monospace}.s44-value-grid h3{margin:4.2rem 0 .65rem;font-size:1.15rem;letter-spacing:-.025em}.s44-value-grid p{margin:0;color:#8f98a3;font-size:.78rem;line-height:1.58}.s44-trust-card,.s44-service-decision{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2rem;align-items:end;margin-top:.7rem;padding:clamp(1.35rem,3vw,2rem);border:1px solid rgba(201,255,74,.17);border-radius:1.25rem;background:radial-gradient(circle at 100% 0,rgba(201,255,74,.075),transparent 24rem),#0d1116}.s44-trust-card h3{margin:.65rem 0 0;font-size:clamp(1.8rem,3.2vw,3rem);letter-spacing:-.04em}.s44-trust-card p,.s44-service-decision p{max-width:58rem;color:#929ba5}.s44-trust-actions{display:flex;gap:.55rem;flex-wrap:wrap;justify-content:flex-end}.s44-price-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.65rem}.s44-price-grid article{min-height:20rem;display:flex;flex-direction:column;padding:1.25rem;border:1px solid rgba(255,255,255,.105);border-radius:1.15rem;background:linear-gradient(145deg,#11151b,#0c1015)}.s44-price-grid article>span{color:#76808a;font:800 .59rem/1 ui-monospace,monospace;letter-spacing:.08em}.s44-price-grid strong{display:block;margin:.8rem 0 0;font-size:clamp(1.8rem,3.2vw,3rem);letter-spacing:-.055em}.s44-price-grid h3{margin:auto 0 .55rem;font-size:1.08rem}.s44-price-grid p{margin:0;color:#8f98a3;font-size:.76rem;line-height:1.5}.s44-price-grid a{margin-top:.9rem;font-size:.7rem}.s44-price--custom{background:radial-gradient(circle at 90% 0,rgba(129,149,255,.12),transparent 17rem),linear-gradient(145deg,#11151b,#0c1015)!important}.s44-process{list-style:none;padding:0;margin:0;border-top:1px solid rgba(255,255,255,.1)}.s44-process li{display:grid;grid-template-columns:minmax(5rem,.2fr) minmax(0,1fr);gap:1rem;padding:1.35rem 0;border-bottom:1px solid rgba(255,255,255,.09)}.s44-process li>span{color:#747e89;font:800 .62rem/1.2 ui-monospace,monospace}.s44-process h3{margin:0;font-size:clamp(1.25rem,2.5vw,2rem);letter-spacing:-.035em}.s44-process p{max-width:55rem;margin:.45rem 0 0;color:#8e98a2}.s44-brief{display:grid;grid-template-columns:1fr 1fr;gap:.75rem;padding:clamp(1.1rem,3vw,1.8rem);border:1px solid rgba(255,255,255,.11);border-radius:1.25rem;background:linear-gradient(145deg,#11151a,#0b0f14)}.s44-brief label{display:grid;gap:.45rem}.s44-brief label>span{color:#818b96;font-size:.68rem;font-weight:800}.s44-brief input,.s44-brief select,.s44-brief textarea{width:100%;border:1px solid rgba(255,255,255,.12);border-radius:.8rem;background:#090c10;color:#eef0ec;padding:.78rem .85rem;font:inherit;outline:none}.s44-brief textarea{resize:vertical;min-height:8rem}.s44-brief input:focus,.s44-brief select:focus,.s44-brief textarea:focus{border-color:rgba(201,255,74,.45);box-shadow:0 0 0 3px rgba(201,255,74,.055)}.s44-brief__wide{grid-column:1/-1}.s44-brief__footer{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;gap:1rem}.s44-brief__footer p{margin:0;color:#747e89;font-size:.68rem}.s44-services-hero{padding:clamp(4rem,8vw,7rem) 0 clamp(3rem,6vw,5rem)}.s44-services-hero h1{margin:.9rem 0 0;max-width:11ch;font-size:clamp(3.5rem,7vw,7rem);line-height:.9;letter-spacing:-.066em}.s44-services-hero>div>p{max-width:52rem;color:#98a1ab;font-size:clamp(1rem,1.5vw,1.16rem);line-height:1.7}.s44-service-map{display:grid;grid-template-columns:repeat(12,1fr);gap:.65rem}.s44-service-map__item{grid-column:span 6;min-height:20rem;display:flex;flex-direction:column;padding:1.3rem;border:1px solid rgba(255,255,255,.1);border-radius:1.2rem;background:linear-gradient(145deg,#11161c,#0c1015);text-decoration:none}.s44-service-map__item--lead{grid-column:span 7;min-height:24rem}.s44-service-map__item--repair{grid-column:span 5;background:radial-gradient(circle at 100% 0,rgba(201,255,74,.09),transparent 20rem),linear-gradient(145deg,#11161c,#0c1015)}.s44-service-map__item>span{color:#76808b;font:800 .6rem/1 ui-monospace,monospace}.s44-service-map__item h2{margin:auto 0 .7rem;max-width:15ch;font-size:clamp(1.8rem,3.6vw,3.4rem);line-height:.98;letter-spacing:-.05em}.s44-service-map__item p{margin:0;max-width:42rem;color:#8e98a2;font-size:.82rem}.s44-service-map__item>div{display:flex;justify-content:space-between;gap:1rem;margin-top:1.1rem;color:#aab2ba;font-size:.7rem}.s44-service-map__item i{font-style:normal}.s44-service-map__item:hover{border-color:rgba(255,255,255,.2);transform:translateY(-3px)}.s44-special-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem}.s44-special-grid a{display:block;padding:1rem;border:1px solid rgba(255,255,255,.09);border-radius:.95rem;background:#0d1116;text-decoration:none}.s44-special-grid strong,.s44-special-grid span{display:block}.s44-special-grid strong{font-size:.84rem}.s44-special-grid span{margin-top:.35rem;color:#7e8893;font-size:.68rem;line-height:1.42}.s44-orientation{padding:clamp(3.8rem,7vw,6rem) 0;border-top:1px solid rgba(255,255,255,.075);border-bottom:1px solid rgba(255,255,255,.075)}.s44-orientation__head{display:grid;grid-template-columns:minmax(0,.6fr) minmax(0,1.4fr);gap:2rem;align-items:start}.s44-orientation__head h2{margin:.45rem 0 0;font-size:clamp(2rem,4vw,4rem);line-height:.98;letter-spacing:-.05em;max-width:15ch}.s44-orientation__head p{margin:.8rem 0 0;max-width:53rem;color:#9099a3;line-height:1.65}.s44-orientation__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.65rem;margin-top:1.4rem}.s44-orientation__grid article{padding:1rem;border:1px solid rgba(255,255,255,.09);border-radius:.95rem;background:#0d1116}.s44-orientation__grid h3{margin:0;font-size:.95rem}.s44-orientation__grid p{margin:.45rem 0 0;color:#838d98;font-size:.75rem;line-height:1.5}
/* refine commercial blocks introduced by earlier stages */
.market-proof[data-stage42-market="true"]{padding:0 0 clamp(3rem,6vw,5rem)}.market-proof__grid{gap:.6rem}.market-proof__item{border-radius:1rem!important;background:linear-gradient(145deg,#10151b,#0b0f14)!important}.market-proof__item strong{letter-spacing:-.035em}.market-packages[data-stage42-packages="true"] .market-package{border-radius:1.05rem;background:linear-gradient(145deg,#10151b,#0b0f14)}
@media(max-width:1100px){.s44-hero__grid{grid-template-columns:1fr}.s44-hero__visual{min-height:34rem;max-width:43rem}.s44-shot--main{height:30rem}.s44-shot--side{height:24rem}.s44-case--visual{grid-column:span 6}.s44-case-stack{grid-column:span 12;grid-template-columns:repeat(3,1fr)}.s44-value-grid,.s44-price-grid,.s44-special-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:820px){.s44-section-head,.s44-orientation__head{grid-template-columns:1fr;gap:.65rem}.s44-route,.s44-route--wide{grid-column:span 6}.s44-service-map__item,.s44-service-map__item--lead,.s44-service-map__item--repair{grid-column:span 12;min-height:17rem}.s44-trust-card,.s44-service-decision{grid-template-columns:1fr;align-items:start}.s44-trust-actions{justify-content:flex-start}.s44-proofline{grid-template-columns:repeat(2,1fr)}.s44-orientation__grid{grid-template-columns:1fr}}
@media(max-width:620px){.s44-hero{padding-top:3rem}.s44-hero h1,.s44-services-hero h1{font-size:clamp(3rem,15vw,4.8rem)}.s44-hero__visual{min-height:26rem}.s44-shot--main{width:68%;height:23rem;top:.5rem}.s44-shot--side{width:55%;height:18rem;top:5rem}.s44-visual-note{bottom:0;width:80%}.s44-actions,.s44-trust-actions{display:grid}.s44-actions .button,.s44-trust-actions .button{width:100%}.s44-route,.s44-route--wide{grid-column:span 12;min-height:14rem}.s44-case--visual{grid-column:span 12;min-height:22rem}.s44-case-stack{grid-template-columns:1fr}.s44-value-grid,.s44-price-grid,.s44-special-grid{grid-template-columns:1fr}.s44-value-grid article{min-height:12rem}.s44-value-grid h3{margin-top:2.8rem}.s44-price-grid article{min-height:16rem}.s44-process li{grid-template-columns:3rem 1fr}.s44-brief{grid-template-columns:1fr}.s44-brief__wide,.s44-brief__footer{grid-column:auto}.s44-brief__footer{align-items:stretch;flex-direction:column}.s44-brief__footer .button{width:100%}.s44-service-map__item>div{align-items:flex-start;flex-direction:column}.s44-proofline{grid-template-columns:1fr 1fr}.s44-inline-actions{flex-direction:column}}
'''
    css.write_text(css_text, encoding="utf-8")

js = root / "assets" / "site-enhancements.js"
if not js.is_file():
    raise SystemExit("stage44: site-enhancements.js missing")
js_text = js.read_text(encoding="utf-8")
if "// Stage 44: compact brief to Telegram." not in js_text:
    js_text += r'''

// Stage 44: compact brief to Telegram.
(() => {
  const form = document.getElementById('s44-brief-form');
  if (!form) return;
  form.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(form);
    const type = String(data.get('type') || '').trim();
    const task = String(data.get('task') || '').trim();
    const current = String(data.get('current') || '').trim();
    const limits = String(data.get('limits') || '').trim();
    if (!task) {
      const field = form.querySelector('[name="task"]');
      if (field) field.focus();
      return;
    }
    const lines = [
      'Приветствую. Пишу с сайта Alexuys.',
      '',
      `Тип задачи: ${type}`,
      `Что нужно: ${task}`,
      current ? `Что уже есть: ${current}` : '',
      limits ? `Срок / бюджет: ${limits}` : '',
    ].filter(Boolean);
    const url = 'https://t.me/Alexuys?text=' + encodeURIComponent(lines.join('\n'));
    if (typeof window.ym === 'function') {
      try { window.ym(112290993, 'reachGoal', 'brief_to_telegram', { type }); } catch (_) {}
    }
    window.open(url, '_blank', 'noopener,noreferrer');
  });
})();
'''
    js.write_text(js_text, encoding="utf-8")

print("stage44 experience rebuild: homepage + services + 4 service orientation blocks")
