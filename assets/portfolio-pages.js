(() => {
  'use strict';
  const en = document.documentElement.lang === 'en';
  const catalog = document.querySelector('.ax-catalog');
  if (catalog) {
    const cards = [...catalog.querySelectorAll('[data-catalog-category]')];
    const search = catalog.querySelector('[data-catalog-search]');
    const filters = [...catalog.querySelectorAll('[data-catalog-filter]')];
    let selected = 'all';
    function apply() {
      const query = search.value.trim().toLocaleLowerCase();
      let count = 0;
      cards.forEach(card => {
        card.hidden = !(selected === 'all' || card.dataset.catalogCategory === selected) || !card.textContent.toLocaleLowerCase().includes(query);
        if (!card.hidden) count++;
      });
      catalog.querySelector('[data-catalog-status]').textContent = (en ? 'Found: ' : 'Найдено: ') + count;
      catalog.querySelector('.ax-catalog-empty').hidden = count !== 0;
    }
    filters.forEach(button => button.addEventListener('click', () => {
      selected = button.dataset.catalogFilter;
      filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      apply();
    }));
    search.addEventListener('input', apply);
  }
  const dialog = document.querySelector('[data-page-lightbox]');
  if (dialog) {
    const preview = dialog.querySelector('img');
    document.querySelectorAll('.ax-content img').forEach(img => {
      if (img.closest('a,button') || !img.getAttribute('src')) return;
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'ax-image-open';
      button.setAttribute('aria-label', (en ? 'Enlarge: ' : 'Увеличить: ') + (img.alt || (en ? 'project image' : 'изображение проекта')));
      img.replaceWith(button);
      button.append(img);
      button.addEventListener('click', () => {
        preview.src = img.currentSrc || img.src;
        preview.alt = img.alt;
        dialog.querySelector('p').textContent = img.alt;
        dialog.showModal();
      });
    });
    dialog.querySelector('[data-page-close]').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  }
})();
