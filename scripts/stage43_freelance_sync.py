#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

# Public Freelance.ru profile facts verified 2026-09-06:
# 20 reviews, 9/10 professionalism, 9/10 communication, 6 years experience,
# on platform since 2023, self-employed status. Keep final site claims tied to
# those directly verifiable facts rather than stale catalogue snapshots.
replacements = {
    "20+ отзывов и 20+ выполненных заданий": "20 отзывов · 9/10 по профессионализму и коммуникации",
    "20+ отзывов и более 20 выполненных заданий": "20 отзывов · 9/10 по профессионализму и коммуникации",
    "более 20 отзывов и более 20 выполненных заданий": "20 отзывов, оценки 9/10 и 6 лет опыта",
    "20+ отзывов в публичном профиле": "20 отзывов в публичном профиле",
    "20+ выполненных заданий на площадке": "6 лет опыта в публичном профиле",
    "20+ отзывов на Freelance.ru": "20 отзывов на Freelance.ru",
    "19 выполненных заданий, оценки 9/9": "20 отзывов, оценки 9/10, 6 лет опыта",
    "19 выполненных заданий": "20 отзывов",
    "9 / 9": "9 / 10",
}

changed = 0
for page in root.rglob("*.html"):
    text = page.read_text(encoding="utf-8", errors="ignore")
    original = text
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Dedicated freelance landing: make the first proof tile match the direct
    # profile rather than a stale catalogue snapshot.
    text = text.replace(
        '<strong>19</strong><span>выполненных заданий</span>',
        '<strong>20</strong><span>публичных отзывов</span>',
    )
    text = text.replace(
        '<strong>9 / 10</strong><span>профессионализм и коммуникация</span>',
        '<strong>9 / 10</strong><span>профессионализм и коммуникация</span>',
    )
    if text != original:
        page.write_text(text, encoding="utf-8")
        changed += 1

css = root / "assets" / "site-enhancements.css"
if not css.is_file():
    raise SystemExit("stage43: site-enhancements.css missing")
css_text = css.read_text(encoding="utf-8")
if "/* stage43 freelance referral */" not in css_text:
    css_text += r'''

/* stage43 freelance referral */
.freelance-ref-banner{border-bottom:1px solid rgba(255,255,255,.09);background:linear-gradient(90deg,rgba(201,255,74,.08),rgba(129,149,255,.055));position:relative;z-index:18}.freelance-ref-banner__inner{width:min(100%,86rem);margin:auto;padding:.8rem clamp(1.1rem,4vw,4.4rem);display:flex;align-items:center;justify-content:space-between;gap:1rem}.freelance-ref-banner__copy{display:flex;align-items:center;gap:.75rem;min-width:0}.freelance-ref-banner__badge{flex:0 0 auto;border:1px solid rgba(201,255,74,.28);border-radius:999px;padding:.3rem .48rem;color:#c9ff4a;font:800 .61rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.06em}.freelance-ref-banner__copy p{margin:0;color:#a6aeb7;font-size:.76rem;line-height:1.45}.freelance-ref-banner__copy strong{color:#f4f5f2}.freelance-ref-banner__actions{display:flex;gap:.45rem;flex:0 0 auto}.freelance-ref-banner__actions a{display:inline-flex;align-items:center;min-height:2.35rem;padding:.48rem .7rem;border:1px solid rgba(255,255,255,.11);border-radius:.7rem;text-decoration:none;font-size:.7rem;font-weight:800}.freelance-ref-banner__actions a:last-child{background:#c9ff4a;border-color:#c9ff4a;color:#090a0b}@media(max-width:760px){.freelance-ref-banner__inner{align-items:flex-start;flex-direction:column}.freelance-ref-banner__actions{width:100%}.freelance-ref-banner__actions a{flex:1;justify-content:center}}@media(max-width:430px){.freelance-ref-banner__copy{align-items:flex-start}.freelance-ref-banner__actions{display:grid;grid-template-columns:1fr}.freelance-ref-banner__actions a{width:100%}}
'''
    css.write_text(css_text, encoding="utf-8")

js = root / "assets" / "site-enhancements.js"
if not js.is_file():
    raise SystemExit("stage43: site-enhancements.js missing")
js_text = js.read_text(encoding="utf-8")
if "// Stage 43: Freelance.ru referral funnel." not in js_text:
    js_text += r'''

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
    if (typeof window.ym !== 'function') return;
    try { window.ym(112290993, 'reachGoal', goal, params); } catch (_) {}
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
      reach('telegram_click', { page: location.pathname, freelance_referral: fromFreelance ? 'yes' : 'no' });
      if (fromFreelance) reach('freelance_to_telegram', { page: location.pathname });
    }
  }, { passive: true });
})();
'''
    js.write_text(js_text, encoding="utf-8")

print(f"stage43 freelance sync: {changed} HTML pages normalized; referral funnel installed")
