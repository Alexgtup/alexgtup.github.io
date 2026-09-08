const form = document.querySelector('#audit-form');
const input = document.querySelector('#url');
const statusEl = document.querySelector('#status');
const resultEl = document.querySelector('#result');
const scoreEl = document.querySelector('#score');
const resultUrl = document.querySelector('#result-url');
const metricsEl = document.querySelector('#metrics');
const issuesEl = document.querySelector('#issues');
const detailsEl = document.querySelector('#details');
const issueCountEl = document.querySelector('#issue-count');
const copyBtn = document.querySelector('#copy-report');

const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (m) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));

function metric(label, value, good = null) {
  const state = good === true ? ' good' : good === false ? ' bad' : '';
  return `<article class="metric${state}"><span>${esc(label)}</span><strong>${esc(value)}</strong></article>`;
}

function render(data) {
  resultEl.hidden = false;
  scoreEl.textContent = data.score;
  resultUrl.textContent = data.finalUrl;
  document.title = `Аудит ${new URL(data.finalUrl).hostname} - ${data.score}/100 | SiteAudit Studio`;

  metricsEl.innerHTML = [
    metric('HTTP', data.summary.status, data.summary.status < 400),
    metric('Индексируемость', data.summary.indexable ? 'Да' : 'Нет', data.summary.indexable),
    metric('robots.txt', data.summary.robots ? 'Есть' : 'Нет', data.summary.robots),
    metric('sitemap.xml', data.summary.sitemap ? (data.summary.sitemapUrls ? `${data.summary.sitemapUrls} URL` : 'Есть') : 'Нет', data.summary.sitemap),
    metric('Внутренние ссылки', data.summary.internalLinks),
    metric('Битые ссылки', data.summary.brokenLinks, data.summary.brokenLinks === 0),
    metric('H1', data.summary.h1Count, data.summary.h1Count === 1),
    metric('Изображения без alt', `${data.summary.imagesWithoutAlt}/${data.summary.images}`, data.summary.imagesWithoutAlt === 0)
  ].join('');

  issueCountEl.textContent = `${data.issues.length} найдено`;
  if (!data.issues.length) {
    issuesEl.innerHTML = '<div class="empty">Критичных базовых проблем не найдено.</div>';
  } else {
    issuesEl.innerHTML = data.issues.map((x) => `
      <article class="issue ${esc(x.severity)}">
        <div class="severity">${esc(x.severity)}</div>
        <div><h3>${esc(x.title)}</h3><p>${esc(x.detail)}</p></div>
      </article>`).join('');
  }

  const broken = data.broken?.length
    ? `<div><span>Проблемные ссылки</span><strong>${data.broken.map((x) => `${esc(x.status)} · ${esc(x.url)}`).join('<br>')}</strong></div>`
    : '';

  detailsEl.innerHTML = `
    <div><span>Title</span><strong>${esc(data.summary.title || 'не найден')}</strong></div>
    <div><span>Description</span><strong>${esc(data.summary.description || 'не найден')}</strong></div>
    <div><span>Canonical</span><strong>${esc(data.summary.canonical || 'не найден')}</strong></div>
    <div><span>Время аудита</span><strong>${esc(data.durationMs)} мс</strong></div>
    <div><span>HSTS</span><strong>${data.headers.hsts ? 'есть' : 'нет'}</strong></div>
    <div><span>CSP</span><strong>${data.headers.csp ? 'есть' : 'нет'}</strong></div>
    ${broken}`;

  resultEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function runAudit(raw) {
  statusEl.textContent = 'Проверяю сайт и внутренние ссылки...';
  resultEl.hidden = true;
  const query = new URLSearchParams({ url: raw });
  const res = await fetch(`/api/audit?${query}`);
  const data = await res.json();
  if (!res.ok || !data.ok) throw new Error(data.error || 'Ошибка аудита');
  history.replaceState(null, '', `/report?url=${encodeURIComponent(data.finalUrl)}`);
  render(data);
  statusEl.textContent = `Готово за ${data.durationMs} мс`;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const raw = input.value.trim();
  if (!raw) return;
  form.querySelector('button').disabled = true;
  try {
    await runAudit(raw);
  } catch (error) {
    statusEl.textContent = error.message || 'Не удалось выполнить аудит';
  } finally {
    form.querySelector('button').disabled = false;
  }
});

copyBtn.addEventListener('click', async () => {
  await navigator.clipboard.writeText(location.href);
  const old = copyBtn.textContent;
  copyBtn.textContent = 'Ссылка скопирована';
  setTimeout(() => copyBtn.textContent = old, 1800);
});

const initial = new URLSearchParams(location.search).get('url');
if (initial) {
  input.value = initial;
  runAudit(initial).catch((error) => statusEl.textContent = error.message || 'Не удалось открыть отчёт');
}
