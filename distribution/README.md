# Alexuys distribution pipeline

Цель этого каталога - не писать материалы «для SEO внутри сайта», а готовить внешние публикации, которые приводят новую аудиторию на конкретные кейсы и услуги.

## Правило публикации

Каждый материал должен:

1. закрывать один понятный вопрос или проблему;
2. содержать реальный технический или продуктовый разбор;
3. вести на один основной кейс;
4. иметь вторую ссылку на соответствующую услугу;
5. не превращаться в рекламный текст.

## Первая волна

### 1. Habr - Fin Planner architecture

Файл: `habr-fin-planner-architecture.md`

Интент: Telegram-бот для учёта расходов, архитектура финансового бота.

Основной переход:
https://alexgtup.github.io/cases/fin-planner/

Коммерческий переход:
https://alexgtup.github.io/telegram-bots/

### 2. vc.ru - Fin Planner case

Файл: `vc-fin-planner-case.md`

Интент: продуктовый разбор Telegram-бота, автоматизация личных финансов.

Основной переход:
https://alexgtup.github.io/cases/fin-planner/

Коммерческий переход:
https://alexgtup.github.io/telegram-bots/

## Следующие материалы

### Habr

- Как спроектировать Telegram-бота с CRM, webhook и API так, чтобы его можно было дорабатывать
  -> `/telegram-bots/`, `/api-integrations/`

- Когда чужой проект лучше ремонтировать, а не переписывать
  -> `/project-repair/`

- n8n в production: retries, idempotency, webhooks и контроль ошибок
  -> `/n8n-automation/`

- Как устроить поиск и фильтрацию в B2B-каталоге
  -> `/cases/factory-catalog/`, `/web-development/`

### vc.ru

- Из чего реально складывается стоимость Telegram-бота
  -> `/guides/telegram-bot-cost/`, `/telegram-bots/`

- Почему CRM для небольшой команды иногда выгоднее собрать под процесс
  -> `/crm-development/`, `/cases/auto-crm/`

- 7 признаков, что существующий веб-проект не нужно переписывать с нуля
  -> `/project-repair/`

## GitHub distribution

Публичные репозитории должны содержать нормальный README и глубокие ссылки на соответствующий кейс/услугу. Не добавлять ссылки в нерелевантные репозитории ради количества.

Уже используется:

- `Alexgtup/bot` -> Telegram/Python + Fin Planner + service pages
- `Alexgtup/alexgtup.github.io` -> portfolio, cases, services, guides

## KPI

Смотрим не количество опубликованных текстов, а:

- новые referring pages/domains;
- переходы на кейсы и service pages;
- новые запросы в GSC;
- заявки/Telegram переходы;
- заказы, где клиент видел внешний материал до портфолио.

Если материал не даёт внешнего обнаружения, доверия или переходов, он не считается частью acquisition engine.
