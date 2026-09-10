(() => {
  'use strict';

  const root = document.documentElement;
  const path = location.pathname.endsWith('/') ? location.pathname : location.pathname + '/';
  const isEn = (root.lang || '').toLowerCase().startsWith('en');

  const SERVICE_COPY = {
    '/telegram-bots/': 'разработку Telegram-бота',
    '/telegram-mini-apps/': 'разработку Telegram Mini App',
    '/n8n-automation/': 'автоматизацию n8n / Make',
    '/crm-development/': 'разработку CRM',
    '/web-development/': 'разработку сайта или веб-сервиса',
    '/api-integrations/': 'API / CRM-интеграцию',
    '/project-repair/': 'доработку существующего проекта',
    '/telegram-bot-repair/': 'доработку Telegram-бота',
    '/backend-development/': 'backend-разработку',
    '/python-development/': 'Python-разработку',
    '/mvp-development/': 'разработку MVP',
    '/app-development/': 'разработку приложения',
    '/ios-development/': 'iOS / Swift-разработку',
    '/ai-automation/': 'AI-автоматизацию',
    '/development/': 'разработку цифрового продукта'
  };

  const h1 = () => (document.querySelector('h1')?.textContent || '')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/[.?!]+$/, '')
    .slice(0, 110);

  const draftForPage = () => {
    if (isEn) {
      if (path.startsWith('/en/cases/')) return `Hello. I viewed the case "${h1()}".\n\nMy project: `;
      if (path.startsWith('/en/guides/')) return `Hello. I read "${h1()}".\n\nMy project: `;
      if (path === '/en/' || path === '/en') return 'Hello. I viewed the Alexuys portfolio.\n\nMy project: ';
      return `Hello. I am writing from the page "${h1()}".\n\nMy project: `;
    }
    if (SERVICE_COPY[path]) return `Здравствуйте. Пишу со страницы про ${SERVICE_COPY[path]}.\n\nЗадача: `;
    if (path.startsWith('/cases/') && path !== '/cases/') return `Здравствуйте. Посмотрел кейс «${h1()}».\n\nМоя задача: `;
    if (path.startsWith('/guides/') && path !== '/guides/') return `Здравствуйте. Прочитал разбор «${h1()}».\n\nМоя задача: `;
    if (path === '/') return 'Здравствуйте. Посмотрел портфолио Alexuys.\n\nЗадача: ';
    if (path === '/cases/') return 'Здравствуйте. Посмотрел кейсы Alexuys.\n\nЗадача: ';
    if (path === '/guides/') return 'Здравствуйте. Посмотрел разборы Alexuys.\n\nЗадача: ';
    return `Здравствуйте. Пишу со страницы «${h1()}».\n\nЗадача: `;
  };

  const placementFor = (link) => {
    if (link.closest('header,.stage98-header,.site-header,.intl-header')) return 'header';
    if (link.closest('#brief,#s44-brief-form')) return 'brief';
    if (link.closest('#contact,.s48-contact,.contact,.contact-card,.dt-contact,.s51-contact')) return 'contact';
    if (link.closest('footer,.footer,.foot,.site-footer')) return 'footer';
    if (link.closest('[class*="hero"]')) return 'hero';
    if (link.closest('.s101-related')) return 'related';
    return 'content';
  };

  const isBareTelegram = (url) =>
    url.hostname === 't.me' &&
    url.pathname.replace(/\/+$/, '').toLowerCase() === '/alexuys' &&
    !url.searchParams.has('text');

  const decorateTelegram = () => {
    const draft = draftForPage();
    document.querySelectorAll('a[href]').forEach((link) => {
      let url;
      try { url = new URL(link.href, location.href); } catch (_) { return; }
      if (url.hostname !== 't.me') return;
      const placement = placementFor(link);
      if (!link.dataset.cta) link.dataset.cta = placement;
      if (isBareTelegram(url)) {
        url.searchParams.set('text', draft);
        link.href = url.toString();
      }
    });
  };

  const goal = (name, params = {}) => {
    try { window.alexuysAnalytics?.goal?.(name, params); } catch (_) {}
  };

  const classifyInternal = (url) => {
    if (url.origin !== location.origin) return null;
    const target = url.pathname.endsWith('/') ? url.pathname : url.pathname + '/';
    if (target.startsWith('/cases/') && target !== '/cases/') return 'case_open';
    if (target.startsWith('/guides/') && target !== '/guides/') return 'guide_open';
    if (SERVICE_COPY[target]) return 'service_open';
    return null;
  };

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    let url;
    try { url = new URL(link.href, location.href); } catch (_) { return; }
    const eventName = classifyInternal(url);
    if (eventName) goal(eventName, {
      target: url.pathname,
      placement: placementFor(link),
      source: path
    });
  });

  const setupBriefFunnel = () => {
    const form = document.getElementById('s44-brief-form');
    if (!form) return;
    let started = false;
    const start = () => {
      if (started) return;
      started = true;
      goal('brief_start', { source: path });
    };
    form.addEventListener('focusin', start, { passive: true });
    form.addEventListener('input', start, { passive: true });
    form.addEventListener('submit', () => goal('brief_submit', { source: path }));
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      decorateTelegram();
      setupBriefFunnel();
    }, { once: true });
  } else {
    decorateTelegram();
    setupBriefFunnel();
  }
})();
