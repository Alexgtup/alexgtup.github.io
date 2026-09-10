(() => {
  const CASE_KEY = 'alexuys:case-return:v1';
  const HOME_KEY = 'alexuys:home-project-filter:v1';
  const MAX_AGE = 30 * 60 * 1000;
  const path = location.pathname.endsWith('/') ? location.pathname : location.pathname + '/';

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

  setupHomeContinuity();
  setupCaseHubContinuity();
  setupCaseDetailContinuity();
})();
