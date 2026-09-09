(() => {
  const path = location.pathname.endsWith('/') ? location.pathname : location.pathname + '/';
  const isEn = path.startsWith('/en/');

  const serviceRoutes = new Set([
    '/services/','/development/','/telegram-bots/','/telegram-mini-apps/','/n8n-automation/',
    '/crm-development/','/web-development/','/backend-development/','/api-integrations/',
    '/project-repair/','/telegram-bot-repair/','/mvp-development/','/ios-development/',
    '/python-development/','/ai-automation/','/app-development/'
  ]);

  const familyFor = () => {
    if (path === '/' || path === '/en/') return 'home';
    if (path.startsWith('/en/')) {
      if (path.startsWith('/en/cases/') && path !== '/en/cases/') return 'case';
      if (path.startsWith('/en/guides/') && path !== '/en/guides/') return 'guide';
      if (['/en/services/','/en/cases/','/en/guides/','/en/about/'].includes(path)) return 'hub';
      if (path === '/en/privacy/') return 'legal';
      return 'service';
    }
    if (path.startsWith('/cases/') && path !== '/cases/') return 'case';
    if (path.startsWith('/guides/') && path !== '/guides/') return 'guide';
    if (path.startsWith('/tools/') && path !== '/tools/') return 'tool';
    if (['/cases/','/guides/','/tools/','/services/','/demos/','/about/','/freelance-developer/'].includes(path)) return 'hub';
    if (path === '/freelance-os/') return 'product';
    if (serviceRoutes.has(path)) return 'service';
    if (path === '/privacy/') return 'legal';
    return 'page';
  };

  const ensureLandmarks = () => {
    document.body.dataset.uxFamily ||= familyFor();
    const main = document.querySelector('main');
    if (main && !main.id) main.id = 'main-content';
    if (!document.querySelector('a[href="#main-content"]') && main) {
      const skip = document.createElement('a');
      skip.className = 'stage94-skip-link';
      skip.href = '#main-content';
      skip.textContent = isEn ? 'Skip to content' : 'К содержанию';
      document.body.prepend(skip);
    }
  };

  const hubFor = () => {
    if (path === '/' || path === '/en/') return null;
    if (path.startsWith('/en/cases/')) return '/en/cases/';
    if (path.startsWith('/en/guides/')) return '/en/guides/';
    if (path.startsWith('/en/') && !['/en/about/','/en/privacy/'].includes(path)) return '/en/services/';
    if (path.startsWith('/cases/')) return '/cases/';
    if (path.startsWith('/guides/')) return '/guides/';
    if (path === '/about/') return '/about/';
    if (serviceRoutes.has(path)) return '/services/';
    return null;
  };

  const markCurrentNavigation = () => {
    const hub = hubFor();
    document.querySelectorAll('nav.nav a[href], nav.intl-nav a[href], nav.dt-navlinks a[href], .fos-nav nav a[href]').forEach(link => {
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

  const firstSectionAfter = hero => {
    let node = hero?.nextElementSibling || null;
    while (node && node.tagName !== 'SECTION') node = node.nextElementSibling;
    return node;
  };

  const ensureTarget = (hero, id) => {
    let target = document.getElementById(id);
    if (target) return target;
    target = firstSectionAfter(hero);
    if (target && !target.id) target.id = id;
    return target;
  };

  const addActionRow = (section, anchor, primary, secondary = null) => {
    if (!section || !anchor || section.querySelector('.stage94-hero-actions')) return;
    const row = document.createElement('div');
    row.className = 'stage94-hero-actions';
    const a = document.createElement('a');
    a.className = 'stage94-action-primary';
    a.href = primary.href;
    a.textContent = primary.label;
    row.append(a);
    if (secondary) {
      const b = document.createElement('a');
      b.className = 'stage94-action-secondary';
      b.href = secondary.href;
      b.textContent = secondary.label;
      row.append(b);
    }
    anchor.insertAdjacentElement('afterend', row);
  };

  const addEntryActions = () => {
    const caseTargets = new Map([
      ['/cases/seo-control-center/', 'case-interface'],
      ['/cases/siteaudit-studio/', 'case-overview'],
      ['/cases/freelance-os/', 'case-overview']
    ]);
    if (caseTargets.has(path)) {
      const hero = document.querySelector('section.hero');
      const targetId = caseTargets.get(path);
      if (ensureTarget(hero, targetId)) {
        addActionRow(hero, hero?.querySelector('.lead'),
          { href: `#${targetId}`, label: 'Смотреть интерфейс ↓' },
          { href: '/cases/', label: 'Все кейсы' });
      }
    }

    if (path === '/tools/' || (path.startsWith('/tools/') && path !== '/tools/')) {
      const hero = document.querySelector('section.dt-hero');
      const targetId = path === '/tools/' ? 'tool-list' : 'tool-workspace';
      if (ensureTarget(hero, targetId)) {
        addActionRow(hero, hero?.querySelector('.dt-privacy') || hero?.querySelector('.dt-lead'),
          { href: `#${targetId}`, label: path === '/tools/' ? 'Открыть инструменты ↓' : 'К инструменту ↓' },
          { href: path === '/tools/' ? '/cases/' : '/tools/', label: path === '/tools/' ? 'Кейсы' : 'Все инструменты' });
      }
    }

    if (path === '/demos/') {
      const hero = document.querySelector('section.growth-hero');
      addActionRow(hero, hero?.querySelector('p'),
        { href: '#demo-products', label: 'Смотреть демо ↓' },
        { href: '/cases/', label: 'Все кейсы' });
    }

    if (['/en/services/','/en/cases/','/en/guides/'].includes(path)) {
      const hero = document.querySelector('section.intl-hero');
      if (ensureTarget(hero, 'browse')) {
        const labels = {
          '/en/services/': 'Browse services ↓',
          '/en/cases/': 'Browse cases ↓',
          '/en/guides/': 'Browse guides ↓'
        };
        addActionRow(hero, hero?.querySelector('.intl-lead'), { href: '#browse', label: labels[path] });
      }
    }

    if (path === '/en/project-repair/') {
      const sections = [...document.querySelectorAll('main > section.intl-section')];
      const last = sections.at(-1);
      const links = last?.querySelector('.intl-links');
      addActionRow(last, links || last?.querySelector('.intl-section-head'),
        { href: 'https://t.me/Alexuys', label: 'Discuss the repair ↗' },
        { href: '/en/services/', label: 'All services' });
    }
  };

  const normalizeEndingOrder = () => {
    if (path !== '/freelance-developer/') return;
    const main = document.querySelector('main');
    const contact = document.getElementById('hub-contact');
    const extra = main?.querySelector('.s68-entry');
    if (main && contact && extra && extra.compareDocumentPosition(contact) & Node.DOCUMENT_POSITION_PRECEDING) {
      main.insertBefore(extra, contact);
    }
  };

  const improveLiveFeedback = () => {
    document.querySelectorAll('.dt-status').forEach(status => {
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      status.setAttribute('aria-atomic', 'true');
    });
    document.querySelectorAll('.project-radar__filters,.case-filter__list,.ux-filterbar').forEach(row => {
      row.setAttribute('role', 'toolbar');
      if (!row.getAttribute('aria-label')) row.setAttribute('aria-label', isEn ? 'Content filters' : 'Фильтры');
    });
    document.querySelectorAll('[data-case-count]').forEach(counter => {
      const container = counter.closest('.case-library__toolbar,.case-filter__top');
      if (container) {
        container.setAttribute('aria-live', 'polite');
        container.setAttribute('aria-atomic', 'true');
      }
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
        const row = [...button.parentElement.querySelectorAll(selectors)]
          .filter(el => !el.disabled && el.offsetParent !== null);
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

  ensureLandmarks();
  markCurrentNavigation();
  addEntryActions();
  normalizeEndingOrder();
  improveLiveFeedback();
  improveSearchEscape();
  keyboardFilterRows();
  document.documentElement.dataset.stage94Ux = 'ready';
})();
