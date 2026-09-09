(() => {
  const path = location.pathname.endsWith('/') ? location.pathname : location.pathname + '/';

  const hubFor = () => {
    if (path === '/' || path === '/en/') return null;
    if (path.startsWith('/en/cases/')) return '/en/cases/';
    if (path.startsWith('/en/guides/')) return '/en/guides/';
    if (path.startsWith('/en/') && !['/en/about/','/en/privacy/'].includes(path)) return '/en/services/';
    if (path.startsWith('/cases/')) return '/cases/';
    if (path.startsWith('/guides/')) return '/guides/';
    if (path === '/about/') return '/about/';
    const serviceRoutes = new Set(['/services/','/development/','/telegram-bots/','/telegram-mini-apps/','/n8n-automation/','/crm-development/','/web-development/','/backend-development/','/api-integrations/','/project-repair/','/telegram-bot-repair/','/mvp-development/','/ios-development/','/python-development/','/ai-automation/','/app-development/']);
    if (serviceRoutes.has(path)) return '/services/';
    return null;
  };

  const markCurrentNavigation = () => {
    const hub = hubFor();
    document.querySelectorAll('nav.nav a[href], nav.intl-nav a[href], nav.dt-navlinks a[href]').forEach(link => {
      let href = link.getAttribute('href') || '';
      if (!href.startsWith('/')) return;
      href = href.split('#')[0].split('?')[0];
      if (!href.endsWith('/')) href += '/';
      const current = href === path || (hub && href === hub);
      link.classList.toggle('is-current', !!current);
      if (current) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  };

  const improveSearchEscape = () => {
    document.querySelectorAll('input[type="search"]').forEach(input => {
      input.addEventListener('keydown', event => {
        if (event.key !== 'Escape' || !input.value) return;
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.focus();
      });
    });
  };

  const keyboardFilterRows = () => {
    const selectors = '[data-project-filter],[data-case-filter],[data-ux-filter]';
    document.querySelectorAll(selectors).forEach(button => {
      button.addEventListener('keydown', event => {
        if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
        const row = [...button.parentElement.querySelectorAll(selectors)].filter(el => !el.disabled && el.offsetParent !== null);
        if (!row.length) return;
        const index = row.indexOf(button);
        let next = index;
        if (event.key === 'ArrowLeft') next = (index - 1 + row.length) % row.length;
        if (event.key === 'ArrowRight') next = (index + 1) % row.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = row.length - 1;
        event.preventDefault();
        row[next].focus();
      });
    });
  };

  markCurrentNavigation();
  improveSearchEscape();
  keyboardFilterRows();
  document.documentElement.dataset.stage94Ux = 'ready';
})();
