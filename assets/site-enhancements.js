(() => {
  const isEnglish = (document.documentElement.lang || '').toLowerCase().startsWith('en');
  const ui = isEnglish ? {
    imageFallback: 'project image',
    openImage: 'Open image',
    dialog: 'Image viewer',
    close: 'Close',
    previous: 'Previous image',
    next: 'Next image',
    captionFallback: 'Project image'
  } : {
    imageFallback: 'изображение проекта',
    openImage: 'Открыть изображение',
    dialog: 'Просмотр изображения',
    close: 'Закрыть',
    previous: 'Предыдущее изображение',
    next: 'Следующее изображение',
    captionFallback: 'Изображение проекта'
  };

  const eligible = [...document.querySelectorAll('main img:not([data-no-lightbox])')].filter(img => {
    const src = img.currentSrc || img.getAttribute('src') || '';
    return src && !src.startsWith('data:') && !img.closest('a,button');
  });
  if (!eligible.length) return;

  eligible.forEach((img, i) => {
    img.dataset.lightboxReady = 'true';
    img.dataset.lightboxIndex = String(i);
    img.tabIndex = img.tabIndex >= 0 ? img.tabIndex : 0;
    img.setAttribute('role', 'button');
    if (!img.getAttribute('aria-label')) {
      const alt = img.getAttribute('alt') || ui.imageFallback;
      img.setAttribute('aria-label', `${ui.openImage}: ${alt}`);
    }
  });

  const root = document.createElement('div');
  root.className = 'media-lightbox';
  root.setAttribute('role', 'dialog');
  root.setAttribute('aria-modal', 'true');
  root.setAttribute('aria-label', ui.dialog);
  root.setAttribute('aria-hidden', 'true');
  root.innerHTML = `
    <div class="media-lightbox__backdrop" data-lightbox-close></div>
    <div class="media-lightbox__dialog">
      <div class="media-lightbox__stage">
        <button class="media-lightbox__close" type="button" aria-label="${ui.close}">×</button>
        <button class="media-lightbox__prev" type="button" aria-label="${ui.previous}">←</button>
        <img class="media-lightbox__image" alt="">
        <button class="media-lightbox__next" type="button" aria-label="${ui.next}">→</button>
      </div>
      <div class="media-lightbox__bar">
        <div class="media-lightbox__caption"></div>
        <div class="media-lightbox__count"></div>
      </div>
    </div>`;
  document.body.appendChild(root);

  const viewer = root.querySelector('.media-lightbox__image');
  const caption = root.querySelector('.media-lightbox__caption');
  const count = root.querySelector('.media-lightbox__count');
  const closeBtn = root.querySelector('.media-lightbox__close');
  const prevBtn = root.querySelector('.media-lightbox__prev');
  const nextBtn = root.querySelector('.media-lightbox__next');
  let current = 0;
  let lastFocus = null;
  let touchStartX = null;
  let touchStartY = null;

  function show(index) {
    current = (index + eligible.length) % eligible.length;
    const source = eligible[current];
    viewer.src = source.currentSrc || source.src;
    viewer.alt = source.alt || '';
    caption.textContent = source.dataset.caption || source.alt || ui.captionFallback;
    count.textContent = eligible.length > 1 ? `${current + 1} / ${eligible.length}` : '';
    prevBtn.hidden = eligible.length < 2;
    nextBtn.hidden = eligible.length < 2;
    if (eligible.length > 1) {
      [current - 1, current + 1].forEach(i => {
        const source = eligible[(i + eligible.length) % eligible.length];
        const pre = new Image();
        pre.src = source.currentSrc || source.src;
      });
    }
  }

  function open(index, trigger) {
    lastFocus = trigger || document.activeElement;
    show(index);
    document.body.classList.add('media-lightbox-open');
    root.classList.add('is-open');
    root.setAttribute('aria-hidden', 'false');
    requestAnimationFrame(() => closeBtn.focus({ preventScroll: true }));
  }

  function close() {
    root.classList.remove('is-open');
    root.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('media-lightbox-open');
    viewer.removeAttribute('src');
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus({ preventScroll: true });
  }

  eligible.forEach(img => {
    img.addEventListener('click', event => {
      event.preventDefault();
      event.stopPropagation();
      open(Number(img.dataset.lightboxIndex || 0), img);
    });
    img.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        event.stopPropagation();
        open(Number(img.dataset.lightboxIndex || 0), img);
      }
    });
  });

  closeBtn.addEventListener('click', close);
  root.querySelector('[data-lightbox-close]').addEventListener('click', close);
  prevBtn.addEventListener('click', () => show(current - 1));
  nextBtn.addEventListener('click', () => show(current + 1));
  root.addEventListener('touchstart', event => {
    if (!root.classList.contains('is-open') || !event.touches[0]) return;
    touchStartX = event.touches[0].clientX;
    touchStartY = event.touches[0].clientY;
  }, { passive: true });
  root.addEventListener('touchend', event => {
    if (touchStartX === null || !event.changedTouches[0]) return;
    const dx = event.changedTouches[0].clientX - touchStartX;
    const dy = event.changedTouches[0].clientY - touchStartY;
    touchStartX = touchStartY = null;
    if (eligible.length > 1 && Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.25) show(current + (dx < 0 ? 1 : -1));
  }, { passive: true });
  document.addEventListener('keydown', event => {
    if (!root.classList.contains('is-open')) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      close();
      return;
    }
    if (event.key === 'ArrowLeft' && eligible.length > 1) show(current - 1);
    if (event.key === 'ArrowRight' && eligible.length > 1) show(current + 1);
    if (event.key === 'Tab') {
      const focusable = [closeBtn, prevBtn, nextBtn].filter(el => !el.hidden && !el.disabled);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });
})();


// Stage 5: low-friction brief + mobile contact CTA.
(() => {
  const isEnglish = (document.documentElement.lang || '').toLowerCase().startsWith('en');
  const briefButton = document.querySelector('[data-copy-brief]');
  if (briefButton) {
    const status = document.querySelector('.brief-status');
    const template = isEnglish
      ? `What is needed:\n\nWhat already exists:\n\nWhat needs to be connected:\n\nWhat the finished result should look like:`
      : `Что нужно:\n\nЧто уже есть:\n\nЧто должно связаться:\n\nКак выглядит готовый результат:`;
    briefButton.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(template);
        briefButton.textContent = isEnglish ? 'Template copied ✓' : 'Шаблон скопирован ✓';
        if (status) status.textContent = isEnglish
          ? 'Paste it into Telegram and add a few details.'
          : 'Можно вставить текст в Telegram и дописать несколько строк.';
        setTimeout(() => { briefButton.textContent = isEnglish ? 'Copy template' : 'Скопировать шаблон'; }, 2600);
      } catch (_) {
        if (status) status.textContent = isEnglish
          ? 'Automatic copy failed — copy the four prompts manually.'
          : 'Не удалось скопировать автоматически — выделите четыре пункта слева.';
      }
    });
  }

  const floatingCtaExcluded = new Set(['/privacy/', '/en/privacy/']);
  if (!document.querySelector('.mobile-project-cta') && !floatingCtaExcluded.has(location.pathname)) {
    const cta = document.createElement('a');
    cta.className = 'mobile-project-cta';
    cta.href = 'https://t.me/Alexuys';
    cta.target = '_blank';
    cta.rel = 'noopener noreferrer';
    cta.dataset.cta = 'mobile_floating';
    cta.textContent = isEnglish ? 'Describe your project in Telegram ↗' : 'Описать задачу в Telegram ↗';
    cta.setAttribute('aria-label', isEnglish ? 'Describe your project in Telegram' : 'Описать задачу в Telegram');
    document.body.appendChild(cta);

    const contact = document.querySelector('#contact, .cta-box, .contact, .intl-cta, .intl-contact');
    const cookie = document.querySelector('.cookie-consent');
    let contactVisible = false;
    const sync = () => {
      const scrolled = window.scrollY > Math.min(520, window.innerHeight * .7);
      cta.classList.toggle('is-visible', scrolled && !contactVisible);
      if (cookie) {
        const cs = getComputedStyle(cookie);
        const shown = !cookie.hidden && cs.display !== 'none' && cs.visibility !== 'hidden' && Number(cs.opacity || 1) !== 0;
        cta.classList.toggle('with-cookie', shown);
      }
    };
    if (contact && 'IntersectionObserver' in window) {
      new IntersectionObserver(entries => { contactVisible = entries.some(e => e.isIntersecting); sync(); }, { threshold: .12 }).observe(contact);
    }
    if (cookie && 'MutationObserver' in window) new MutationObserver(sync).observe(cookie,{attributes:true,attributeFilter:['class','style','hidden']});
    let syncQueued = false;
    const scheduleSync = () => {
      if (syncQueued) return;
      syncQueued = true;
      requestAnimationFrame(() => { syncQueued = false; sync(); });
    };
    addEventListener('scroll', scheduleSync, { passive:true });
    addEventListener('resize', scheduleSync, { passive:true });
    sync();
  }
})();


// Stage 8: useful interaction goals on every page where consented Metrika is already active.
(() => {
  const servicePaths = new Set(['/telegram-bots/','/ai-automation/','/n8n-automation/','/crm-development/','/web-development/','/api-integrations/','/project-repair/','/ios-development/','/services/', '/en/services/','/en/telegram-bot-development/','/en/telegram-mini-app-development/','/en/ai-automation/','/en/n8n-automation/','/en/custom-crm-development/','/en/web-app-development/','/en/api-integrations/','/en/python-development/','/en/backend-development/','/en/mvp-development/','/en/ios-development/','/en/project-repair/']);
  const goal = (name, params={}) => {
    const analytics = window.alexuysAnalytics;
    if (!analytics || typeof analytics.goal !== 'function') return;
    analytics.goal(name, params);
  };
  document.addEventListener('click', event => {
    const el = event.target instanceof Element ? event.target : null;
    if (!el) return;
    const copy = el.closest('[data-copy-brief]');
    if (copy) goal('brief_copy');
    const a = el.closest('a');
    if (!a) return;
    let url;
    try { url = new URL(a.href, location.href); } catch (_) { return; }
    if (url.origin !== location.origin) return;
    if ((url.pathname.startsWith('/cases/') && url.pathname !== '/cases/') || (url.pathname.startsWith('/en/cases/') && url.pathname !== '/en/cases/')) goal('case_open', { target: url.pathname });
    else if (servicePaths.has(url.pathname)) goal('service_open', { target: url.pathname });
    else if (url.pathname.startsWith('/guides/') || url.pathname.startsWith('/en/guides/')) goal('guide_open', { target: url.pathname });
    else if (url.pathname === '/about/' || url.pathname === '/en/about/') goal('about_open');
  }, { capture: true });
})();


// Stage 10: consistent mobile navigation on standalone pages.
(() => {
  if (document.body?.dataset.page === 'home' || document.querySelector('.stage98-mobile-menu') || document.querySelector('.mobile-site-toggle')) return;
  const head = document.querySelector('.header .head, .site-header .head, .header .container, .site-header .container');
  if (!head) return;
  const button = document.createElement('button');
  button.className = 'mobile-site-toggle';
  button.type = 'button';
  button.setAttribute('aria-label','Открыть меню');
  button.setAttribute('aria-expanded','false');
  button.textContent = '☰';
  const drawer = document.createElement('nav');
  drawer.className = 'mobile-site-drawer';
  drawer.setAttribute('aria-label','Мобильная навигация');
  const englishMap = {
    '/about/':'/en/about/', '/services/':'/en/services/', '/telegram-bots/':'/en/telegram-bot-development/',
    '/telegram-mini-apps/':'/en/telegram-mini-app-development/', '/ai-automation/':'/en/ai-automation/',
    '/n8n-automation/':'/en/n8n-automation/', '/crm-development/':'/en/custom-crm-development/',
    '/web-development/':'/en/web-app-development/', '/api-integrations/':'/en/api-integrations/',
    '/python-development/':'/en/python-development/', '/backend-development/':'/en/backend-development/',
    '/mvp-development/':'/en/mvp-development/', '/ios-development/':'/en/ios-development/',
    '/cases/':'/en/cases/', '/cases/auto-crm/':'/en/cases/auto-crm/', '/cases/taxi-app/':'/en/cases/taxi-app/',
    '/cases/factory-catalog/':'/en/cases/factory-catalog/', '/cases/fin-planner/':'/en/cases/fin-planner/', '/cases/swift-calendar/':'/en/cases/swift-calendar/',
    '/guides/':'/en/guides/', '/guides/development-cost/':'/en/guides/development-cost/', '/guides/bot-vs-mini-app-vs-web/':'/en/guides/bot-vs-mini-app-vs-web/',
    '/guides/telegram-bot-cost/':'/en/guides/telegram-bot-cost/', '/guides/n8n-vs-make/':'/en/guides/n8n-vs-make/', '/project-repair/':'/en/project-repair/', '/privacy/':'/en/privacy/'
  };
  const enLink = englishMap[location.pathname] ? `<a href="${englishMap[location.pathname]}" hreflang="en" lang="en">English version — EN</a>` : '';
  drawer.innerHTML = '<a href="/cases/">Кейсы</a><a href="/services/">Услуги</a><a href="/guides/">Разборы</a><a href="/about/">Обо мне</a>' + enLink + '<a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить задачу ↗</a>';
  head.appendChild(button);
  document.body.appendChild(drawer);
  const close=()=>{drawer.classList.remove('is-open');button.setAttribute('aria-expanded','false');button.textContent='☰'};
  button.addEventListener('click',()=>{const open=!drawer.classList.contains('is-open');drawer.classList.toggle('is-open',open);button.setAttribute('aria-expanded',String(open));button.textContent=open?'×':'☰'});
  drawer.addEventListener('click',e=>{if(e.target.closest('a')) close()});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
  document.addEventListener('click',e=>{if(drawer.classList.contains('is-open')&&!drawer.contains(e.target)&&!button.contains(e.target))close()});
})();


// Stage 18: English mobile navigation for international pages.
(() => {
  const head = document.querySelector('.intl-header .intl-head');
  const button = document.querySelector('.intl-mobile-toggle');
  if (!head || !button || document.querySelector('.intl-mobile-drawer')) return;
  const ru = document.querySelector('.intl-lang')?.getAttribute('href') || '/';
  const drawer = document.createElement('nav');
  drawer.className = 'intl-mobile-drawer';
  drawer.setAttribute('aria-label','Mobile navigation');
  drawer.innerHTML = '<a href="/en/services/">Services</a><a href="/en/cases/">Cases</a><a href="/en/guides/">Guides</a><a href="/en/about/">About</a><a href="'+ru+'" hreflang="ru" lang="ru">Русская версия — RU</a><a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Discuss a project ↗</a>';
  document.body.appendChild(drawer);
  const close=()=>{drawer.classList.remove('is-open');button.setAttribute('aria-expanded','false');button.textContent='☰'};
  button.addEventListener('click',()=>{const open=!drawer.classList.contains('is-open');drawer.classList.toggle('is-open',open);button.setAttribute('aria-expanded',String(open));button.textContent=open?'×':'☰'});
  drawer.addEventListener('click',e=>{if(e.target.closest('a'))close()});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
  document.addEventListener('click',e=>{if(drawer.classList.contains('is-open')&&!drawer.contains(e.target)&&!button.contains(e.target))close()});
})();


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
    window.alexuysAnalytics?.goal('lead_brief_submit', { kind, budget });
    window.alexuysAnalytics?.lead?.('brief', { kind, budget });
    window.open(url, '_blank', 'noopener,noreferrer');
  });
})();


// Stage 43: Freelance.ru referral funnel.
(() => {
  const params = new URLSearchParams(location.search);
  const source = String(params.get('utm_source') || '').toLowerCase();
  const medium = String(params.get('utm_medium') || '').toLowerCase();
  const directReferral = source.includes('freelance') || document.referrer.includes('freelance.ru');
  if (directReferral) {
    try { sessionStorage.setItem('alexuys_freelance_referral', '1'); } catch (_) {}
  }
  let fromFreelance = directReferral;
  try { fromFreelance = fromFreelance || sessionStorage.getItem('alexuys_freelance_referral') === '1'; } catch (_) {}

  const reach = (goal, params = {}) => {
    window.alexuysAnalytics?.goal(goal, params);
  };

  if (directReferral) {
    let sent = false;
    try { sent = sessionStorage.getItem('alexuys_freelance_visit_goal') === '1'; } catch (_) {}
    if (!sent) {
      reach('freelance_referral_visit', { page: location.pathname, source: source || 'referrer', medium });
      try { sessionStorage.setItem('alexuys_freelance_visit_goal', '1'); } catch (_) {}
    }
  }

  if (fromFreelance && !document.querySelector('.freelance-ref-banner')) {
    const banner = document.createElement('aside');
    banner.className = 'freelance-ref-banner';
    banner.setAttribute('aria-label', 'Информация для посетителей с Freelance.ru');
    banner.innerHTML = '<div class="freelance-ref-banner__inner"><div class="freelance-ref-banner__copy"><span class="freelance-ref-banner__badge">FREELANCE.RU</span><p><strong>Пришли из моего профиля?</strong> Здесь собраны подробные кейсы, ориентиры стоимости и условия работы. Публичные отзывы остаются на Freelance.ru.</p></div><div class="freelance-ref-banner__actions"><a href="/cases/">Кейсы</a><a href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Написать в Telegram ↗</a></div></div>';
    const header = document.querySelector('header');
    if (header) header.insertAdjacentElement('afterend', banner);
    else document.body.prepend(banner);
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    const href = link.getAttribute('href') || '';
    if (href.includes('freelance.ru/gglalex') || href.includes('freelance.ru/reviews/gglalex')) {
      reach('freelance_profile_click', { page: location.pathname });
    }
    if (href.includes('t.me/Alexuys')) {
      if (fromFreelance) reach('freelance_to_telegram', { source: 'freelance' });
    }
  }, { passive: true });
})();


// Stage 44: compact brief to Telegram.
(() => {
  const form = document.getElementById('s44-brief-form');
  if (!form) return;
  const status = form.querySelector('[data-brief-status]');
  const result = form.querySelector('[data-brief-result]');
  const draft = form.querySelector('[data-brief-draft]');
  const email = form.querySelector('[data-brief-email]');
  const telegram = form.querySelector('[data-brief-telegram]');
  const goal = (name, params = {}) => {
    window.alexuysAnalytics?.goal(name, params);
  };
  function prepare() {
    if (!form.reportValidity()) return null;
    const data = new FormData(form);
    const type = String(data.get('type') || '').trim();
    const task = String(data.get('task') || '').trim();
    const current = String(data.get('current') || '').trim();
    const limits = String(data.get('limits') || '').trim();
    if (!task) {
      status.textContent = 'Опишите задачу хотя бы одной строкой.';
      const field = form.querySelector('[name="task"]');
      if (field) field.focus();
      return null;
    }
    const lines = [
      'Приветствую. Пишу с сайта Alexuys.',
      '',
      `Тип задачи: ${type}`,
      `Что нужно: ${task}`,
      current ? `Что уже есть: ${current}` : '',
      limits ? `Срок / бюджет: ${limits}` : '',
    ].filter(Boolean);
    draft.value = lines.join('\n');
    telegram.href = 'https://t.me/Alexuys?text=' + encodeURIComponent(draft.value);
    email.href = 'mailto:alexgtup@gmail.com?subject=' + encodeURIComponent('Задача с сайта Alexuys') + '&body=' + encodeURIComponent(draft.value);
    result.hidden = false;
    return { type, url: telegram.href };
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    const prepared = prepare();
    if (!prepared) return;
    status.textContent = 'Сообщение подготовлено. Нажмите «Отправить» в Telegram. Если переход не сработал, текст и другие способы связи доступны ниже.';
    goal('brief_to_telegram', { type: prepared.type });
    window.alexuysAnalytics?.lead?.('brief', { type: prepared.type });
    window.open(prepared.url, '_blank', 'noopener,noreferrer');
  });
  form.querySelector('[data-brief-preview]').addEventListener('click', () => {
    if (!prepare()) return;
    status.textContent = 'Текст готов. Откройте письмо или скопируйте сообщение. Оно ещё не отправлено.';
    goal('brief_preview');
    email.focus();
  });
  form.querySelector('[data-brief-copy]').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(draft.value);
      status.textContent = 'Текст скопирован. Вставьте его в Telegram или письмо и отправьте.';
      goal('brief_copy');
    } catch (_) {
      draft.focus();
      draft.select();
      status.textContent = 'Выделил текст. Скопируйте его вручную и отправьте в Telegram или по почте.';
    }
  });
  // Editing the brief invalidates the previously prepared message and links.
  form.addEventListener('input', event => {
    if (!event.target.name) return;
    result.hidden = true;
    draft.value = '';
    email.href = 'mailto:alexgtup@gmail.com';
    telegram.href = 'https://t.me/Alexuys';
    status.textContent = '';
  });
  form.querySelectorAll('button[disabled]').forEach(button => { button.disabled = false; });
})();
