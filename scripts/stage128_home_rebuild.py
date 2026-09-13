#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
path = ROOT / 'index.html'
if not path.is_file():
    raise SystemExit('stage128: home missing')
html = path.read_text(encoding='utf-8')

main = r'''<main id="main-content" class="p128-home" data-stage128-home="true">
<section class="p128-hero" aria-labelledby="p128-title">
  <div class="p128-shell">
    <div class="p128-hero__copy">
      <p class="p128-eyebrow">ALEXUYS / DIGITAL PRODUCT DEVELOPMENT</p>
      <h1 id="p128-title">Разработка, которая <span>доходит до запуска.</span></h1>
      <p class="p128-lead">Сайты, Telegram-сервисы, автоматизация и приложения. Беру задачу целиком или подключаюсь к уже работающему проекту - без лишнего слоя менеджеров и терминов.</p>
      <div class="p128-actions">
        <a class="p128-btn p128-btn--primary" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить задачу <span>↗</span></a>
        <a class="p128-link" href="#selected-work">Смотреть проекты <span>↓</span></a>
      </div>
    </div>
    <div class="p128-hero__visual" aria-label="Примеры реальных проектов">
      <a class="p128-shot p128-shot--one" href="/cases/fin-planner/"><img src="/assets/cases/fin-planner/fin-planner-card-01-720w.webp" width="720" height="900" alt="Интерфейс Fin Planner" decoding="async" fetchpriority="high"><span>Fin Planner</span></a>
      <a class="p128-shot p128-shot--two" href="/cases/swift-calendar/"><img src="/assets/cases/swift-calendar/calendar-card-01-720w.webp" width="720" height="900" alt="Интерфейс Swift Calendar" loading="lazy" decoding="async"><span>Swift Calendar</span></a>
      <a class="p128-shot p128-shot--three" href="/cases/sheetpilot-ai/"><img src="/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp" width="720" height="540" alt="Интерфейс SheetPilot AI" loading="lazy" decoding="async"><span>SheetPilot AI</span></a>
      <div class="p128-orbit" aria-hidden="true"></div>
    </div>
    <div class="p128-proofbar" aria-label="Проверяемые факты">
      <a href="https://freelance.ru/gglalex" target="_blank" rel="me noopener noreferrer"><strong>20</strong><span>публичных отзывов</span></a>
      <a href="/cases/"><strong>9</strong><span>подробных кейсов</span></a>
      <a href="/demos/"><strong>4</strong><span>публичных демо</span></a>
      <span><strong>6 лет</strong><span>в публичном профиле</span></span>
    </div>
  </div>
</section>

<section class="p128-work" id="selected-work" aria-labelledby="p128-work-title">
  <div class="p128-shell">
    <div class="p128-section-intro"><p>SELECTED WORK</p><h2 id="p128-work-title">Сначала работа. <span>Потом слова.</span></h2><a href="/cases/">Все кейсы ↗</a></div>
    <article class="p128-feature">
      <a class="p128-feature__media" href="/cases/fin-planner/"><img src="/assets/cases/fin-planner/fin-planner-original-800w.webp" width="800" height="605" loading="lazy" decoding="async" alt="Fin Planner - Telegram-сервис для учета финансов"></a>
      <div class="p128-feature__copy"><span>01 / TELEGRAM PRODUCT</span><h3>Fin Planner</h3><p>Бот для ежедневного учета денег: расходы, доходы, регулярные операции и отчёты внутри привычного Telegram.</p><a href="/cases/fin-planner/">Разобрать кейс ↗</a></div>
    </article>
    <article class="p128-feature p128-feature--reverse">
      <a class="p128-feature__media" href="/cases/swift-calendar/"><img src="/assets/cases/swift-calendar/calendar-original-800w.webp" width="800" height="551" loading="lazy" decoding="async" alt="Swift Calendar - интерфейс iOS приложения"></a>
      <div class="p128-feature__copy"><span>02 / iOS PRODUCT</span><h3>Swift Calendar</h3><p>Нативное приложение с календарными сценариями, событиями и продуктовой логикой - без ощущения веб-страницы внутри телефона.</p><a href="/cases/swift-calendar/">Разобрать кейс ↗</a></div>
    </article>
    <article class="p128-feature">
      <a class="p128-feature__media" href="/cases/sheetpilot-ai/"><img src="/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp" width="720" height="540" loading="lazy" decoding="async" alt="SheetPilot AI - веб-интерфейс обработки Excel"></a>
      <div class="p128-feature__copy"><span>03 / WEB PRODUCT</span><h3>SheetPilot AI</h3><p>Сервис, где Excel-файл меняется обычной фразой: загрузить, описать действие, проверить результат и скачать новую версию.</p><a href="/cases/sheetpilot-ai/">Открыть кейс и демо ↗</a></div>
    </article>
  </div>
</section>

<section class="p128-capabilities" aria-labelledby="p128-cap-title">
  <div class="p128-shell">
    <div class="p128-cap__lead"><p>WHAT I BUILD</p><h2 id="p128-cap-title">С нуля или поверх того, <span>что уже есть.</span></h2><p>Не нужно знать стек заранее. Достаточно понимать, какой результат должен появиться у пользователя или внутри бизнеса.</p></div>
    <div class="p128-cap__list">
      <a href="/web-development/"><span>01</span><strong>Сайты и веб-сервисы</strong><em>Лендинг, кабинет, каталог, SaaS, внутренний сервис</em><b>↗</b></a>
      <a href="/telegram-bots/"><span>02</span><strong>Telegram-продукты</strong><em>Боты, Mini Apps, оплаты, заявки, личные сценарии</em><b>↗</b></a>
      <a href="/n8n-automation/"><span>03</span><strong>Автоматизация</strong><em>Убрать ручные действия и связать рабочие сервисы</em><b>↗</b></a>
      <a href="/project-repair/"><span>04</span><strong>Доработка проектов</strong><em>Ошибки, чужой код, незавершённый релиз, адаптив</em><b>↗</b></a>
    </div>
  </div>
</section>

<section class="p128-proof" id="reviews" aria-labelledby="p128-proof-title">
  <div class="p128-shell p128-proof__grid">
    <div class="p128-proof__statement"><p>PUBLIC PROOF</p><h2 id="p128-proof-title">Не нужно верить сайту <span>на слово.</span></h2><blockquote>«Задачу понял сразу, задал нужные вопросы, всё сдал быстро. Рекомендую.»</blockquote><p class="p128-proof__author"><strong>Иван</strong><span>публичный отзыв на Freelance.ru</span></p><a class="p128-link" href="https://freelance.ru/reviews/gglalex/" target="_blank" rel="noopener noreferrer">Посмотреть все отзывы ↗</a></div>
    <div class="p128-proof__numbers"><div><strong>20</strong><span>отзывов в открытом профиле</span></div><div><strong>9/10</strong><span>профессионализм</span></div><div><strong>9/10</strong><span>коммуникация</span></div><div><strong>6 лет</strong><span>опыта в публичном профиле</span></div></div>
  </div>
</section>

<section class="p128-start" id="brief" aria-labelledby="p128-start-title">
  <div class="p128-shell p128-start__grid">
    <div class="p128-start__copy"><p>START</p><h2 id="p128-start-title">Покажите задачу. <span>Разберём первый рабочий шаг.</span></h2><p>Достаточно пары предложений. Если есть ссылка, код или макет - отлично. Если есть только идея, тоже нормально.</p><div class="p128-start__meta"><span>Ответ напрямую</span><span>Без созвона на старте</span><span>Можно с чужим кодом</span></div></div>
    <form class="s44-brief p128-form" id="s44-brief-form">
      <label><span>Что нужно сделать</span><select name="type"><option>Небольшая правка / разовая задача</option><option>Продолжить прошлый проект</option><option>Сайт / веб-сервис</option><option>Telegram-бот или мини-приложение</option><option>Мобильное приложение</option><option>Автоматизировать повторяющиеся действия</option><option>Связать несколько сервисов</option><option>Доработка существующего проекта</option><option>Другое / пока не знаю</option></select></label>
      <label class="s44-brief__wide"><span>Задача своими словами</span><textarea maxlength="3000" name="task" placeholder="Что должно работать в итоге?" required rows="5"></textarea></label>
      <details class="ux-brief-more"><summary>Есть ссылка, срок или бюджет?<span>необязательно</span></summary><div class="ux-brief-more__grid"><label><span>Что уже есть</span><input maxlength="500" name="current" placeholder="Сайт, код, Figma, ТЗ или только идея" type="text"></label><label><span>Срок / бюджет, если есть</span><input maxlength="200" name="limits" placeholder="Например: до 2 недель / ориентир 30-50 тыс." type="text"></label></div></details>
      <div class="s44-brief__footer"><p>Откроется Telegram с готовым черновиком.</p><button class="button primary" disabled type="submit">Перейти в Telegram ↗</button><button class="button" data-brief-preview disabled type="button">Другой способ</button></div>
      <p aria-live="polite" class="s44-brief__wide" data-brief-status role="status"></p>
      <div class="s44-brief__wide" data-brief-result hidden><label><span>Ваше сообщение</span><textarea aria-label="Ваше сообщение" data-brief-draft readonly rows="7"></textarea></label><div class="s44-actions"><a class="button primary" data-brief-email href="mailto:alexgtup@gmail.com">Открыть письмо ↗</a><button class="button" data-brief-copy type="button">Скопировать текст</button><a class="button" data-brief-telegram href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Открыть Telegram ещё раз ↗</a></div></div>
    </form>
  </div>
</section>
</main>'''

html, count = re.subn(r'<main\b[^>]*id="main-content"[^>]*>.*?</main>', main, html, count=1, flags=re.S | re.I)
if count != 1:
    raise SystemExit('stage128: main replacement failed')
path.write_text(html, encoding='utf-8')

check = path.read_text(encoding='utf-8')
for token in ('data-stage128-home="true"', 'id="p128-title"', 'id="selected-work"', 'id="s44-brief-form"', '/cases/fin-planner/', '/web-development/'):
    if token not in check:
        raise SystemExit(f'stage128: missing {token}')
if len(re.findall(r'<h1\b', check, flags=re.I)) != 1:
    raise SystemExit('stage128: home must keep one H1')
print('stage128 home rebuild: old homepage DOM replaced by five-screen project-led composition')
