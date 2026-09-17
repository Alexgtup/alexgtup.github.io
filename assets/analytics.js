/* Shared, consent-based analytics. Loaded once on every public page. */
(() => {
  'use strict';
  if (window.alexuysAnalytics) return;
  const ID = 112290993;
  const KEY = 'alexuys-analytics-consent-v1';
  const OWNER_KEY = 'alexuys-owner-analytics-skip-v1';
  const params = new URLSearchParams(location.search);
  try {
    if (params.get('alexuys_owner') === '1') {
      localStorage.setItem(OWNER_KEY, '1');
      params.delete('alexuys_owner');
      const clean = location.pathname + (params.toString() ? '?' + params.toString() : '') + location.hash;
      history.replaceState(null, '', clean);
    } else if (params.get('alexuys_owner') === '0') {
      localStorage.removeItem(OWNER_KEY);
      params.delete('alexuys_owner');
      const clean = location.pathname + (params.toString() ? '?' + params.toString() : '') + location.hash;
      history.replaceState(null, '', clean);
    }
  } catch (_) {}
  let ownerSkip = false;
  try { ownerSkip = localStorage.getItem(OWNER_KEY) === '1'; } catch (_) {}
  const automated = navigator.webdriver === true || /HeadlessChrome/i.test(navigator.userAgent || '');
  if (ownerSkip || automated) {
    window.alexuysAnalytics = { goal() {}, get consent() { return 'declined'; }, get skipped() { return true; } };
    return;
  }
  let active = false;
  let consent = null;
  const normalize = value => ['accepted', 'yes'].includes(value) ? 'accepted'
    : ['declined', 'no'].includes(value) ? 'declined' : null;
  try { consent = normalize(localStorage.getItem(KEY)); } catch (_) {}
  const box = document.querySelector('[data-analytics-consent]');
  const settings = document.querySelector('[data-analytics-settings]');
  function start() {
    if (active || consent !== 'accepted') return;
    active = true;
    window.ym = window.ym || function () { (window.ym.a = window.ym.a || []).push(arguments); };
    window.ym.l = Date.now();
    if (!document.querySelector('script[data-alexuys-metrika]')) {
      const script = document.createElement('script');
      script.async = true;
      script.dataset.alexuysMetrika = 'true';
      script.src = 'https://mc.yandex.ru/metrika/tag.js?id=' + ID;
      document.head.appendChild(script);
    }
    window.ym(ID, 'init', {
      webvisor: true,
      clickmap: true,
      trackLinks: true,
      accurateTrackBounce: true
    });
  }
  function show(open) {
    if (box) box.hidden = !open;
    if (settings) settings.hidden = open;
  }
  function choose(value, persist = true) {
    consent = normalize(value);
    if (persist) { try { localStorage.setItem(KEY, consent); } catch (_) {} }
    if (consent === 'accepted') start();
    else if (active) {
      window.ym(ID, 'destruct');
      active = false;
    }
    show(!consent);
  }
  function goal(name, params = {}) {
    if (active && consent === 'accepted' && typeof window.ym === 'function') {
      window.ym(ID, 'reachGoal', name, { page: location.pathname, ...params });
    }
  }
  window.alexuysAnalytics = { goal, get consent() { return consent; }, get skipped() { return false; } };
  box?.addEventListener('click', event => {
    const button = event.target.closest('[data-analytics-choice]');
    if (button) { choose(button.dataset.analyticsChoice); settings?.focus(); }
  });
  settings?.addEventListener('click', () => {
    show(true);
    box?.querySelector('button')?.focus();
  });
  window.addEventListener('storage', event => {
    if (event.key === KEY || event.key === null) choose(event.newValue, false);
  });
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    let url;
    try { url = new URL(link.href, location.href); } catch (_) { return; }
    if (url.hostname === 't.me') goal('telegram_click', link.dataset.cta ? { placement: link.dataset.cta } : {});
    else if (url.protocol === 'mailto:') goal('email_click');
    else if (url.hostname === 'freelance.ru') goal('freelance_click');
    if (link.dataset.demo) goal('demo_open', { project: link.dataset.demo });
    if (link.dataset.offer) goal('freelance_offer_open', { offer: link.dataset.offer });
  });
  choose(consent, false);
})();