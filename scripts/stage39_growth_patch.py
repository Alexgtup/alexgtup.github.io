#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def read(route):
    p = root / ("index.html" if route == "/" else route.strip("/") + "/index.html")
    if not p.is_file():
        raise SystemExit(f"stage39: missing {route}: {p}")
    return p, p.read_text(encoding="utf-8")


def write(p, text):
    p.write_text(text, encoding="utf-8")


def replace_once(text, old, new, label):
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise SystemExit(f"stage39: marker not found: {label}")


# 1) Homepage: narrow the commercial promise to the three directions most likely
# to convert for a solo developer, while keeping the broader service catalogue below.
p, html = read("/")
html = replace_once(
    html,
    '<h1 id="hero-title">Telegram-боты, автоматизация <span class="soft">и веб-сервисы под задачу.</span></h1>',
    '<h1 id="hero-title">Telegram-боты, автоматизация <span class="soft">и доработка проектов.</span></h1>',
    "homepage H1",
)
html = replace_once(
    html,
    '<p class="hero-copy">Собираю Telegram-боты, автоматизацию, CRM, интеграции и веб-продукты под конкретный процесс — от первой логики до запуска и дальнейшей доработки.</p>',
    '<p class="hero-copy">Разрабатываю и дорабатываю Telegram-ботов, автоматизацию и интеграции. Если проект уже существует, можно начать с конкретной ошибки, сломанного сценария или функции — без обязательного большого ТЗ.</p>',
    "homepage hero copy",
)
html = replace_once(
    html,
    '<div aria-label="Направления работы" class="hero-tags" data-nosnippet=""><span>TELEGRAM</span><span>AI AUTOMATION</span><span>WEB</span><span>INTEGRATIONS</span></div>',
    '<div aria-label="Направления работы" class="hero-tags" data-nosnippet=""><span>TELEGRAM</span><span>AUTOMATION</span><span>PROJECT REPAIR</span><span>INTEGRATIONS</span></div>',
    "homepage hero tags",
)

work_marker = '<section aria-labelledby="work-title" class="section container" id="work">'
quick_start = '''<section aria-labelledby="quick-start-title" class="section container" id="quick-start">
<div class="section-head">
<div class="section-index" data-nosnippet="">01 / Быстрый старт</div>
<div><h2 class="section-title" id="quick-start-title">Понятный первый шаг. <span class="soft">Без оценки вслепую.</span></h2><p class="section-lead">Ориентиры нужны, чтобы сразу понимать порядок бюджета. Точная стоимость зависит от текущего состояния и интеграций. <a class="inline-more" href="https://freelance.ru/gglalex" rel="noopener noreferrer" target="_blank">20+ отзывов и 20+ выполненных заданий на Freelance.ru ↗</a></p></div>
</div>
<div class="route-grid">
<a class="route-card" href="/project-repair/"><span class="route-no">ОТ 5 000 ₽</span><strong>Доработка существующего проекта</strong><p>Ошибка на сайте, сломанный бот, чужой код, интеграция или незавершённый релиз. Сначала локализую проблему.</p><span class="route-link">Доработка проекта ↗</span></a>
<a class="route-card" href="/telegram-bots/"><span class="route-no">ОТ 15 000 ₽</span><strong>Telegram-бот</strong><p>Первый рабочий сценарий: заявки, анкета, уведомления, данные или простая интеграция.</p><span class="route-link">Разработка Telegram-бота ↗</span></a>
<a class="route-card" href="/n8n-automation/"><span class="route-no">ОТ 15 000 ₽</span><strong>Автоматизация n8n / Make</strong><p>Webhook, API, CRM, Telegram или таблицы в одном воспроизводимом процессе с обработкой ошибок.</p><span class="route-link">Автоматизация ↗</span></a>
</div>
</section>
'''
if 'id="quick-start"' not in html:
    if work_marker not in html:
        raise SystemExit("stage39: homepage work marker not found")
    html = html.replace(work_marker, quick_start + work_marker, 1)

# Replace copy-paste-only brief with a real low-friction form. Telegram officially
# supports t.me/<username>?text=<draft_text>, so no backend/API key is required.
old_brief = '''<div class="brief-action">
<span class="eyebrow" data-nosnippet="">Можно начать за 2 минуты</span>
<h3>Скопируйте шаблон и заполните своими словами.</h3>
<p>Не нужно придумывать архитектуру или технические термины — это уже часть моей работы.</p>
<div class="brief-buttons"><button class="button" data-copy-brief="" type="button">Скопировать шаблон</button><a class="button primary" href="https://t.me/Alexuys" rel="noreferrer noopener" target="_blank">Открыть Telegram ↗</a></div>
<div aria-live="polite" class="brief-status"></div>
</div>'''
new_brief = '''<div class="brief-action">
<span class="eyebrow" data-nosnippet="">Можно начать за 2 минуты</span>
<h3>Коротко опишите задачу — текст сразу откроется в Telegram.</h3>
<p>Без регистрации и без отправки данных на сайт. Форма только собирает сообщение и открывает чат @Alexuys с готовым черновиком.</p>
<form class="lead-brief" data-lead-brief>
<label><span>Что нужно сделать</span><textarea name="task" rows="4" required placeholder="Например: бот принимает заявки, но перестала работать передача в CRM"></textarea></label>
<label><span>Тип задачи</span><select name="kind"><option value="Доработка существующего проекта">Доработка существующего проекта</option><option value="Telegram-бот">Telegram-бот</option><option value="n8n / Make автоматизация">n8n / Make автоматизация</option><option value="Интеграция API / CRM">Интеграция API / CRM</option><option value="Другая задача">Другая задача</option></select></label>
<label><span>Ориентир по бюджету</span><select name="budget"><option value="Не определён">Пока не определён</option><option value="до 10 000 ₽">до 10 000 ₽</option><option value="10 000–30 000 ₽">10 000–30 000 ₽</option><option value="30 000–70 000 ₽">30 000–70 000 ₽</option><option value="от 70 000 ₽">от 70 000 ₽</option></select></label>
<div class="brief-buttons"><button class="button primary" type="submit">Открыть Telegram с текстом ↗</button><button class="button" data-copy-brief="" type="button">Скопировать шаблон</button></div>
<div aria-live="polite" class="brief-status"></div>
</form>
</div>'''
html = replace_once(html, old_brief, new_brief, "homepage lead form")
write(p, html)

# Form styling is appended to the built shared stylesheet so source templates stay small.
css = root / "assets" / "site-enhancements.css"
if not css.is_file():
    raise SystemExit("stage39: site-enhancements.css not found")
css_text = css.read_text(encoding="utf-8")
css_marker = "/* stage39 lead brief */"
if css_marker not in css_text:
    css_text += '''\n\n/* stage39 lead brief */
.lead-brief{display:grid;gap:.75rem;margin-top:1.15rem}.lead-brief label{display:grid;gap:.4rem}.lead-brief label>span{color:#929aa4;font-size:.72rem;font-weight:700}.lead-brief textarea,.lead-brief select{width:100%;min-height:2.85rem;border:1px solid rgba(255,255,255,.11);border-radius:.8rem;background:#0b0e12;color:#f4f5f2;padding:.72rem .8rem;font:inherit;font-size:.82rem;outline:none}.lead-brief textarea{resize:vertical;min-height:7rem;line-height:1.55}.lead-brief textarea:focus,.lead-brief select:focus{border-color:rgba(201,255,74,.55);box-shadow:0 0 0 3px rgba(201,255,74,.07)}.lead-brief textarea::placeholder{color:#68717b}.lead-brief .brief-buttons{margin-top:.15rem}.lead-brief .brief-status{min-height:1.25rem;color:#8f98a2;font-size:.72rem;line-height:1.45}@media(max-width:560px){.lead-brief .brief-buttons{display:grid}.lead-brief .button{width:100%}}\n'''
    css.write_text(css_text, encoding="utf-8")

# Telegram public username links support a pre-filled draft via ?text=.
js = root / "assets" / "site-enhancements.js"
if not js.is_file():
    raise SystemExit("stage39: site-enhancements.js not found")
js_text = js.read_text(encoding="utf-8")
js_marker = "// Stage 39: pre-filled Telegram lead form."
if js_marker not in js_text:
    js_text += r'''

// Stage 39: pre-filled Telegram lead form.
(() => {
  const form = document.querySelector('[data-lead-brief]');
  if (!form) return;
  const status = form.querySelector('.brief-status');
  form.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(form);
    const task = String(data.get('task') || '').trim();
    if (!task) {
      if (status) status.textContent = 'Опишите задачу хотя бы одной строкой.';
      form.querySelector('[name="task"]')?.focus();
      return;
    }
    const kind = String(data.get('kind') || 'Другая задача');
    const budget = String(data.get('budget') || 'Не определён');
    const draft = `Приветствую. Пишу с сайта Alexuys.\n\nТип задачи: ${kind}\nБюджет: ${budget}\n\nЧто нужно:\n${task}`;
    const url = `https://t.me/Alexuys?text=${encodeURIComponent(draft)}`;
    if (status) status.textContent = 'Открываю Telegram с готовым сообщением…';
    if (typeof window.ym === 'function') {
      try { window.ym(112290993, 'reachGoal', 'lead_brief_submit', { page: location.pathname, kind, budget }); } catch (_) {}
    }
    window.open(url, '_blank', 'noopener,noreferrer');
  });
})();
'''
    js.write_text(js_text, encoding="utf-8")

# 2) Project repair becomes the primary landing for small/medium existing-project work.
p, html = read("/project-repair/")
html = replace_once(
    html,
    '<title>Доработка сайта и чужого проекта — исправление ошибок | Alexuys</title>',
    '<title>Доработка сайтов и Telegram-ботов — исправление ошибок | Alexuys</title>',
    "repair title",
)
html = replace_once(
    html,
    'Доработка сайта, Telegram-бота или веб-сервиса: аудит кода, исправление ошибок, интеграций и логики, завершение проекта и подготовка к релизу.',
    'Доработка сайтов, Telegram-ботов и существующих проектов: исправление ошибок, API и интеграций, чужой код, адаптив, завершение и подготовка к релизу.',
    "repair description first occurrence",
)
html = html.replace('Доработка сайта и чужого проекта — исправление ошибок | Alexuys', 'Доработка сайтов и Telegram-ботов — исправление ошибок | Alexuys')
html = replace_once(
    html,
    '<h1>Доработка сайта <em>и существующего проекта</em></h1>',
    '<h1>Доработка сайта, Telegram-бота <em>и существующего проекта</em></h1>',
    "repair H1",
)
html = replace_once(
    html,
    '<p class="lead">Подключаюсь к проекту, который уже существует: ищу реальную причину ошибки, отделяю критичное от косметики и довожу согласованный участок до проверяемого результата. Подходит для сайтов, ботов и веб-сервисов.</p>',
    '<p class="lead">Если сайт, Telegram-бот или веб-сервис уже существует, не обязательно начинать заново. Сначала воспроизвожу проблему, нахожу её источник и оцениваю минимальный объём, который вернёт рабочий сценарий.</p>',
    "repair lead",
)

repair_marker = '<section class="section container"><div class="section-head"><div class="kicker" data-nosnippet="">Что делаю</div>'
repair_pricing = '''<section class="section container"><div class="section-head"><div class="kicker" data-nosnippet="">Стоимость · ориентир</div><h2>Можно начать <em>с небольшой задачи</em></h2></div><div class="cards"><article class="card"><span class="num" data-nosnippet="">ОТ 5 000 ₽</span><h3>Небольшое исправление</h3><p>Локальный баг, адаптив, форма, настройка или понятная правка в существующем проекте после просмотра реализации.</p></article><article class="card"><span class="num" data-nosnippet="">ОТ 10 000 ₽</span><h3>Логика или интеграция</h3><p>API, webhook, авторизация, Telegram, CRM или сценарий, где нужно найти причину сбоя и проверить соседние состояния.</p></article><article class="card"><span class="num" data-nosnippet="">ПОСЛЕ АУДИТА</span><h3>Продолжить чужой проект</h3><p>Сначала отделяю уже рабочую часть от незавершённой и называю объём до следующего проверяемого результата.</p></article></div><p class="micro">Это ориентиры, а не фиксированный прайс: точную оценку даю после ссылки, скрина, исходников или короткого описания проблемы.</p></section>'''
if 'Стоимость · ориентир' not in html:
    if repair_marker not in html:
        raise SystemExit("stage39: repair insertion marker not found")
    html = html.replace(repair_marker, repair_pricing + repair_marker, 1)
write(p, html)

# 3) Strengthen the weak internal-link graph with contextual links, not footer spam.
p, html = read("/development/")
old = '<a href="/web-development/"><strong>Веб-разработка</strong><span>Сервисы и кабинеты</span></a></div>'
new = '<a href="/web-development/"><strong>Веб-разработка</strong><span>Сервисы и кабинеты</span></a><a href="/app-development/"><strong>Приложения</strong><span>Web, Mini App и iOS по пользовательскому сценарию</span></a></div>'
html = replace_once(html, old, new, "development -> app-development")
write(p, html)

p, html = read("/mvp-development/")
old = '<a href="/cases/"><strong>Кейсы</strong><span>Реальные проекты</span></a></div>'
new = '<a href="/cases/"><strong>Кейсы</strong><span>Реальные проекты</span></a><a href="/app-development/"><strong>Разработка приложений</strong><span>Когда MVP развивается в отдельный продукт</span></a></div>'
html = replace_once(html, old, new, "mvp -> app-development")
write(p, html)

p, html = read("/cases/auto-crm/")
old = '<a href="/n8n-automation/"><strong>n8n / Make</strong><span>Автоматизировать повторяющиеся действия между системами.</span></a></div>'
new = '<a href="/n8n-automation/"><strong>n8n / Make</strong><span>Автоматизировать повторяющиеся действия между системами.</span></a><a href="/guides/custom-crm-or-ready/"><strong>Своя CRM или готовая</strong><span>Разбор, когда кастомная система действительно оправдана.</span></a></div>'
html = replace_once(html, old, new, "auto-crm -> CRM guide")
write(p, html)

p, html = read("/en/services/")
old = '</div></section><section class="intl-container intl-section"><div class="intl-cta-box">'
new = '<a href="/en/guides/development-cost/"><strong>Software development cost guide</strong><span>What actually changes an estimate before the build starts.</span></a></div></section><section class="intl-container intl-section"><div class="intl-cta-box">'
html = replace_once(html, old, new, "en services -> cost guide")
write(p, html)

p, html = read("/en/telegram-bot-development/")
old = '<a href="/en/cases/fin-planner/"><strong>Fin Planner case</strong><span>A real Telegram product in the portfolio</span></a></div>'
new = '<a href="/en/cases/fin-planner/"><strong>Fin Planner case</strong><span>A real Telegram product in the portfolio</span></a><a href="/en/guides/telegram-bot-cost/"><strong>Telegram bot cost guide</strong><span>Estimate scenarios, integrations and production scope.</span></a></div>'
html = replace_once(html, old, new, "en telegram service -> cost guide")
write(p, html)

p, html = read("/en/n8n-automation/")
old = '<a href="/en/backend-development/"><strong>Backend development</strong><span>When the workflow needs a custom service</span></a></div>'
new = '<a href="/en/backend-development/"><strong>Backend development</strong><span>When the workflow needs a custom service</span></a><a href="/en/guides/n8n-vs-make/"><strong>n8n vs Make</strong><span>Choose the automation platform by workflow and maintenance needs.</span></a></div>'
html = replace_once(html, old, new, "en n8n service -> comparison guide")
write(p, html)

print("stage39 growth: homepage focus + pricing + Telegram lead form, project-repair commercialized, weak internal links strengthened")
