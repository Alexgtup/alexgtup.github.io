(() => {
  const HOME_OR_READING = () => {
    const page = document.body?.dataset?.page || '';
    return page === 'home' || page.startsWith('guides--');
  };

  const cookieIsVisible = () => {
    const banner = document.querySelector('.growth-cookie, .cookie-consent');
    if (!banner || banner.hidden) return false;
    const style = getComputedStyle(banner);
    return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity || 1) !== 0;
  };

  const syncFloatingCta = () => {
    const cta = document.querySelector('.mobile-project-cta');
    if (!cta) return;

    if (HOME_OR_READING()) {
      cta.remove();
      return;
    }

    if (cookieIsVisible()) {
      cta.dataset.stage84Suppressed = 'true';
      cta.style.setProperty('display', 'none', 'important');
      cta.setAttribute('aria-hidden', 'true');
      cta.tabIndex = -1;
      return;
    }

    if (cta.dataset.stage84Suppressed === 'true') {
      delete cta.dataset.stage84Suppressed;
      cta.style.removeProperty('display');
      cta.removeAttribute('aria-hidden');
      cta.removeAttribute('tabindex');
    }
  };

  const normalizeCookieSettings = () => {
    document.querySelectorAll('.growth-cookie-settings, .cookie-settings').forEach(button => {
      if (innerWidth > 900) return;
      button.style.setProperty('position', 'static', 'important');
      button.style.setProperty('inset', 'auto', 'important');
      button.style.setProperty('transform', 'none', 'important');
      button.style.setProperty('float', 'none', 'important');
      button.style.setProperty('max-width', 'calc(100% - 2rem)', 'important');
      button.style.setProperty('margin', '1.25rem auto 2rem', 'important');
    });
  };

  let queued = false;
  const schedule = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      syncFloatingCta();
      normalizeCookieSettings();
    });
  };

  const start = () => {
    schedule();

    const observer = new MutationObserver(schedule);
    observer.observe(document.body, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ['class', 'style', 'hidden']
    });

    addEventListener('resize', schedule, { passive: true });
    addEventListener('pageshow', schedule, { passive: true });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
})();
