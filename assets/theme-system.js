(() => {
  'use strict';

  const KEY = 'alexuys:theme:v1';
  const root = document.documentElement;
  const isEnglish = (root.lang || '').toLowerCase().startsWith('en');

  const readTheme = () => {
    try {
      const saved = localStorage.getItem(KEY);
      return saved === 'light' || saved === 'dark' ? saved : 'dark';
    } catch (_) {
      return 'dark';
    }
  };

  const updateBrowserChrome = (theme) => {
    root.style.colorScheme = theme;
    const scheme = document.querySelector('meta[name="color-scheme"]');
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (scheme) scheme.setAttribute('content', theme);
    if (themeColor) themeColor.setAttribute('content', theme === 'light' ? '#f5f6f8' : '#090b0e');
  };

  const buttonCopy = (theme, mobile) => {
    const next = theme === 'light' ? 'dark' : 'light';
    if (isEnglish) {
      return {
        label: next === 'light' ? 'Switch to light theme' : 'Switch to dark theme',
        visible: mobile ? (next === 'light' ? 'Light theme' : 'Dark theme') : ''
      };
    }
    return {
      label: next === 'light' ? 'Включить светлую тему' : 'Включить тёмную тему',
      visible: mobile ? (next === 'light' ? 'Светлая тема' : 'Тёмная тема') : ''
    };
  };

  const syncButtons = (theme) => {
    document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
      const mobile = button.classList.contains('theme-toggle--mobile');
      const copy = buttonCopy(theme, mobile);
      button.setAttribute('aria-label', copy.label);
      button.setAttribute('title', copy.label);
      button.setAttribute('aria-pressed', String(theme === 'light'));
      button.dataset.themeCurrent = theme;
      const text = button.querySelector('.theme-toggle__label');
      if (text) text.textContent = copy.visible;
    });
  };

  const applyTheme = (theme, persist = false) => {
    const safeTheme = theme === 'light' ? 'light' : 'dark';
    root.dataset.theme = safeTheme;
    updateBrowserChrome(safeTheme);
    syncButtons(safeTheme);
    if (persist) {
      try { localStorage.setItem(KEY, safeTheme); } catch (_) {}
      try { window.alexuysAnalytics?.goal?.('theme_toggle', { theme: safeTheme }); } catch (_) {}
    }
    window.dispatchEvent(new CustomEvent('alexuys:themechange', { detail: { theme: safeTheme } }));
  };

  // Run before body rendering finishes so a saved light theme does not flash dark first.
  applyTheme(readTheme(), false);

  const makeButton = (mobile = false) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = mobile ? 'theme-toggle theme-toggle--mobile' : 'theme-toggle';
    button.dataset.themeToggle = 'true';
    button.innerHTML = '<span class="theme-toggle__track" aria-hidden="true"><span class="theme-toggle__sun">☀</span><span class="theme-toggle__moon">☾</span><span class="theme-toggle__thumb"></span></span><span class="theme-toggle__label"></span>';
    button.addEventListener('click', () => {
      const next = root.dataset.theme === 'light' ? 'dark' : 'light';
      applyTheme(next, true);
    });
    return button;
  };

  const mount = () => {
    if (document.querySelector('[data-theme-toggle]')) {
      syncButtons(root.dataset.theme || 'dark');
      return;
    }

    const desktopNav = document.querySelector('.stage98-nav');
    if (desktopNav) {
      const button = makeButton(false);
      const language = desktopNav.querySelector('.stage98-lang');
      const cta = desktopNav.querySelector('.stage98-cta');
      desktopNav.insertBefore(button, language || cta || null);
    }

    const mobileNav = document.querySelector('.stage98-mobile-menu > nav');
    if (mobileNav) {
      const button = makeButton(true);
      const language = mobileNav.querySelector('.stage98-lang');
      const cta = mobileNav.querySelector('.stage98-mobile-cta');
      mobileNav.insertBefore(button, language || cta || null);
    }

    syncButtons(root.dataset.theme || 'dark');
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();

  window.addEventListener('storage', (event) => {
    if (event.key !== KEY) return;
    const theme = event.newValue === 'light' ? 'light' : 'dark';
    applyTheme(theme, false);
  });
})();
