(() => {
  const CASE_KEY = 'alexuys:case-return:v1';
  const HOME_KEY = 'alexuys:home-project-filter:v1';
  const MAX_AGE = 30 * 60 * 1000;
  const path = location.pathname.endsWith('/') ? location.pathname : location.pathname + '/';
  const isEnglish = (document.documentElement.lang || '').toLowerCase().startsWith('en') || path.startsWith('/en/');

  const read = (key) => {
    try {
      const value = JSON.parse(sessionStorage.getItem(key) || 'null');
      if (!value || typeof value !== 'object') return null;
      if (value.at && Date.now() - value.at > MAX_AGE) {
        sessionStorage.removeItem(key);
        return null;
      }
      return value;
    } catch (_) {
      return null;
    }
  };

  const write = (key, value) => {
    try { sessionStorage.setItem(key, JSON.stringify({ ...value, at: Date.now() })); } catch (_) {}
  };

  const sameOriginReferrerPath = () => {
    try {
      if (!document.referrer) return '';
      const ref = new URL(document.referrer);
      return ref.origin === location.origin ? ref.pathname : '';
    } catch (_) {
      return '';
    }
  };

  const setupHomeContinuity = () => {
    const root = document.querySelector('[data-project-showcase]');
    if (!root) return;
    const buttons = [...root.querySelectorAll('[data-project-filter]')];
    const caseLinks = [...root.querySelectorAll('a[href^="/cases/"]')].filter(link => {
      try { return new URL(link.href, location.href).pathname === '/cases/'; } catch (_) { return false; }
    });
    const supported = new Set(buttons.map(button => button.dataset.projectFilter || 'all'));

    const syncLinks = (filter) => {
      caseLinks.forEach(link => {
        link.href = filter && filter !== 'all' ? `/cases/?type=${encodeURIComponent(filter)}` : '/cases/';
      });
    };

    buttons.forEach(button => button.addEventListener('click', () => {
      const filter = button.dataset.projectFilter || 'all';
      write(HOME_KEY, { filter });
      syncLinks(filter);
    }));

    window.addEventListener('DOMContentLoaded', () => {
      const saved = read(HOME_KEY);
      const cameBack = sameOriginReferrerPath().startsWith('/cases/');
      const filter = cameBack && saved && supported.has(saved.filter) ? saved.filter : 'all';
      const button = buttons.find(item => (item.dataset.projectFilter || 'all') === filter);
      if (button && filter !== 'all') button.click();
      else syncLinks('all');
    }, { once: true });
  };

  const setupCaseHubContinuity = () => {
    if (path !== '/cases/') return;
    const root = document.querySelector('[data-case-library]');
    if (!root) return;
    const cards = [...root.querySelectorAll('[data-case-card][href]')];

    cards.forEach(card => card.addEventListener('click', () => {
      write(CASE_KEY, {
        url: location.pathname + location.search + location.hash,
        scrollY: Math.max(0, Math.round(window.scrollY)),
        restore: false
      });
    }));

    window.addEventListener('DOMContentLoaded', () => {
      const saved = read(CASE_KEY);
      if (!saved || !saved.restore || saved.url !== location.pathname + location.search + location.hash) return;
      requestAnimationFrame(() => requestAnimationFrame(() => {
        window.scrollTo({ top: Number(saved.scrollY) || 0, behavior: 'auto' });
        write(CASE_KEY, { ...saved, restore: false });
      }));
    }, { once: true });
  };

  const setupCaseDetailContinuity = () => {
    if (!path.startsWith('/cases/') || path === '/cases/') return;
    const saved = read(CASE_KEY);
    if (!saved || typeof saved.url !== 'string' || !saved.url.startsWith('/cases/')) return;
    if (sameOriginReferrerPath() !== '/cases/') return;

    document.querySelectorAll('main a[href="/cases/"]').forEach(link => {
      link.href = saved.url;
      link.addEventListener('click', () => write(CASE_KEY, { ...saved, restore: true }));
    });
  };

  const contactPlacement = (link) => {
    if (link.closest('header,.header,.site-header,.intl-header,nav')) return 'navigation';
    if (link.closest('.hero,.s44-hero,.s48-hero,.growth-hero,.intl-hero')) return 'hero';
    if (link.closest('#brief,.s44-brief,.contact,.cta-box,.intl-contact,.intl-cta')) return 'contact';
    if (link.closest('footer')) return 'footer';
    return 'content';
  };

  const pageMessage = () => {
    const heading = (document.querySelector('main h1')?.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120);
    const isCase = path.startsWith('/cases/') || path.startsWith('/en/cases/');
    const isGuide = path.startsWith('/guides/') || path.startsWith('/en/guides/');
    const isHome = path === '/' || path === '/en/';
    if (isEnglish) {
      if (isCase && heading) return `Hello. I viewed the case “${heading}”.\n\nProject: `;
      if (isGuide && heading) return `Hello. I read the guide “${heading}”.\n\nProject: `;
      if (!isHome && heading) return `Hello. I viewed the page “${heading}”.\n\nProject: `;
      return 'Hello. I viewed your portfolio.\n\nProject: ';
    }
    if (isCase && heading) return `Здравствуйте. Посмотрел кейс «${heading}».\n\nЗадача: `;
    if (isGuide && heading) return `Здравствуйте. Прочитал разбор «${heading}».\n\nЗадача: `;
    if (!isHome && heading) return `Здравствуйте. Посмотрел страницу «${heading}».\n\nЗадача: `;
    return 'Здравствуйте. Посмотрел портфолио.\n\nЗадача: ';
  };

  const enhanceContactContinuity = () => {
    const draft = pageMessage();
    document.querySelectorAll('a[href]').forEach(link => {
      let url;
      try { url = new URL(link.href, location.href); } catch (_) { return; }
      if (url.hostname !== 't.me' || url.pathname.replace(/\/+$/, '').toLowerCase() !== '/alexuys') return;
      link.dataset.cta ||= contactPlacement(link);
      if (!url.searchParams.has('text')) {
        url.searchParams.set('text', draft);
        link.href = url.toString();
      }
    });
  };

  setupHomeContinuity();
  setupCaseHubContinuity();
  setupCaseDetailContinuity();
  enhanceContactContinuity();
})();
