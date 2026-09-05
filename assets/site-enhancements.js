(() => {
  const eligible = [...document.querySelectorAll('main img:not([data-no-lightbox])')].filter(img => {
    const src = img.currentSrc || img.getAttribute('src') || '';
    return src && !src.startsWith('data:');
  });
  if (!eligible.length) return;

  eligible.forEach((img, i) => {
    img.dataset.lightboxReady = 'true';
    img.dataset.lightboxIndex = String(i);
    img.tabIndex = img.tabIndex >= 0 ? img.tabIndex : 0;
    img.setAttribute('role', 'button');
    if (!img.getAttribute('aria-label')) {
      const alt = img.getAttribute('alt') || 'изображение проекта';
      img.setAttribute('aria-label', `Открыть изображение: ${alt}`);
    }
  });

  const root = document.createElement('div');
  root.className = 'media-lightbox';
  root.setAttribute('role', 'dialog');
  root.setAttribute('aria-modal', 'true');
  root.setAttribute('aria-label', 'Просмотр изображения');
  root.innerHTML = `
    <div class="media-lightbox__backdrop" data-lightbox-close></div>
    <div class="media-lightbox__dialog">
      <div class="media-lightbox__stage">
        <button class="media-lightbox__close" type="button" aria-label="Закрыть">×</button>
        <button class="media-lightbox__prev" type="button" aria-label="Предыдущее изображение">←</button>
        <img class="media-lightbox__image" alt="">
        <button class="media-lightbox__next" type="button" aria-label="Следующее изображение">→</button>
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
    caption.textContent = source.dataset.caption || source.alt || 'Изображение проекта';
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
    requestAnimationFrame(() => closeBtn.focus({ preventScroll: true }));
  }

  function close() {
    root.classList.remove('is-open');
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
    if (event.key === 'Escape') close();
    if (event.key === 'ArrowLeft' && eligible.length > 1) show(current - 1);
    if (event.key === 'ArrowRight' && eligible.length > 1) show(current + 1);
  });
})();
