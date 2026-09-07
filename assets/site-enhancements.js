(() => {
  if (location.pathname === '/cases/sheetpilot-ai/' || location.pathname === '/cases/sheetpilot-ai/index.html') {
    const card = document.querySelector('.status-card');
    if (card) {
      const heading = card.querySelector('h2');
      const copy = card.querySelector('p');
      const actions = card.querySelector('.actions');
      if (heading) heading.innerHTML = 'Публичное демо — <em>уже работает.</em>';
      if (copy) copy.textContent = 'SheetPilot AI уже развёрнут как публичный сервис. Можно открыть демо, загрузить Excel-файл, описать изменение обычным языком, проверить предпросмотр и скачать новый файл.';
      if (actions && !actions.querySelector('[data-sheetpilot-live-demo]')) {
        const oldStatus = actions.querySelector('.btn.status');
        const demo = document.createElement('a');
        demo.className = 'btn primary';
        demo.href = 'https://sheetpilot-ai-6omr.onrender.com';
        demo.target = '_blank';
        demo.rel = 'noopener noreferrer';
        demo.dataset.sheetpilotLiveDemo = 'true';
        demo.textContent = 'Открыть демо ↗';
        if (oldStatus) oldStatus.replaceWith(demo); else actions.prepend(demo);
        const telegram = [...actions.querySelectorAll('a')].find(a => a.href.includes('t.me/Alexuys'));
        if (telegram) telegram.classList.remove('primary');
      }
    }
    document.querySelectorAll('.section-copy').forEach(node => {
      node.textContent = node.textContent.replace('Публичную демо-версию добавлю после отдельного развёртывания сервиса.', 'Публичная демо-версия уже развёрнута и доступна для тестирования.');
    });
  }

  const base = document.createElement('script');
  base.src = '/assets/site-enhancements-base.js';
  document.head.appendChild(base);
})();
