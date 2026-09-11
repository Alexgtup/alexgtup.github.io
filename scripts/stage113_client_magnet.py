#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
HOME = ROOT / 'index.html'
BUNDLE = ROOT / 'assets' / 'stage105-final-ui.css'
MARK = '/* stage113-client-magnet */'
PROFILE_URL = 'https://freelance.ru/gglalex'
REVIEWS_URL = 'https://freelance.ru/reviews/gglalex/'

# Public Freelance.ru profile snapshot checked 2026-09-11.
PROFILE_REVIEWS = 20
PROFILE_EXPERIENCE_YEARS = 6
PROFILE_PROFESSIONALISM = 9
PROFILE_COMMUNICATION = 9

CSS = r'''
/* stage113-client-magnet */
/* Conversion layer: make verified proof visible before a visitor has to trust claims. */
.s44-hero__copy{position:relative;z-index:2}
.s44-hero__copy .s44-kicker{letter-spacing:.095em}
.s44-hero__copy h1{max-width:14.5ch!important}
.s44-hero__copy h1 em{color:var(--ds-accent,#c9ff4a)!important;font-style:normal!important}
.s44-hero__copy .s44-lead{max-width:43rem!important}
.s44-proofline>a{min-width:0}
.s44-proofline>a strong{font-size:clamp(1.05rem,1.6vw,1.35rem)!important;letter-spacing:-.035em}
.s44-proofline>a span{line-height:1.35}
.s44-hero__visual{position:relative!important;isolation:isolate}
.s44-hero__visual::before{
  content:"ПУБЛИЧНЫЕ ОТЗЫВЫ · FREELANCE.RU";
  position:absolute;z-index:8;top:.1rem;right:.1rem;
  padding:.58rem .78rem;border-radius:999px;
  background:var(--ds-accent,#c9ff4a);color:#0b0c0e;
  box-shadow:0 12px 30px rgba(0,0,0,.16);
  font:800 .63rem/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  letter-spacing:.055em;
}
.s44-shot{box-shadow:0 28px 72px rgba(0,0,0,.23)!important}
.s44-shot span{backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}

.s113-reviews{
  position:relative;
  padding:clamp(4.5rem,8vw,7.8rem) 0;
  border-top:1px solid var(--ds-line,rgba(255,255,255,.1));
  border-bottom:1px solid var(--ds-line,rgba(255,255,255,.1));
  overflow:hidden;
}
.s113-reviews::before{
  content:"";position:absolute;pointer-events:none;
  width:34rem;height:34rem;right:-11rem;top:-15rem;border-radius:50%;
  background:radial-gradient(circle,var(--ds-accent-soft,rgba(201,255,74,.08)),transparent 68%);
}
.s113-review-head{
  display:grid;grid-template-columns:minmax(0,1.15fr) minmax(18rem,.7fr);
  gap:clamp(2rem,6vw,6rem);align-items:end;margin-bottom:2rem;
}
.s113-kicker{
  display:block;margin-bottom:.8rem;color:var(--ds-muted,#9ca2aa);
  font:750 .68rem/1.2 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  letter-spacing:.09em;text-transform:uppercase;
}
.s113-review-head h2{margin:0;max-width:16ch;font-size:clamp(2.2rem,4.5vw,4.7rem);line-height:.98;letter-spacing:-.055em}
.s113-review-head h2 em{font-style:normal;color:var(--ds-accent,#c9ff4a)}
.s113-review-head p{margin:0;color:var(--ds-muted,#9ca2aa);font-size:1rem;line-height:1.7;max-width:35rem}
.s113-review-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem}
.s113-review-card{
  display:flex;flex-direction:column;min-height:14rem;padding:1.35rem;
  border:1px solid var(--ds-line,rgba(255,255,255,.1));border-radius:1.35rem;
  background:var(--ds-surface,#111318);box-shadow:0 16px 42px rgba(0,0,0,.07)
}
.s113-review-card::before{content:"“";color:var(--ds-accent,#c9ff4a);font:800 2.4rem/1 Georgia,serif}
.s113-review-card blockquote{margin:.55rem 0 1.4rem;font-size:clamp(1.05rem,1.7vw,1.28rem);line-height:1.45;letter-spacing:-.02em}
.s113-review-card footer{margin-top:auto;padding:0;border:0;background:none!important}
.s113-review-card cite{display:block;font-style:normal;font-weight:800}
.s113-review-card time{display:block;margin-top:.28rem;color:var(--ds-muted,#9ca2aa);font-size:.78rem}
.s113-review-proof{
  margin-top:.9rem;display:grid;grid-template-columns:auto 1fr auto;gap:1rem;align-items:center;
  padding:1rem 1.15rem;border:1px solid var(--ds-line,rgba(255,255,255,.1));border-radius:1.15rem;
  background:var(--ds-surface-2,var(--ds-surface,#111318));
}
.s113-review-proof strong{font-size:1rem;letter-spacing:-.02em}
.s113-review-proof span{color:var(--ds-muted,#9ca2aa);font-size:.84rem;line-height:1.45}
.s113-review-proof a{white-space:nowrap;text-decoration:none;font-weight:800;color:var(--ds-text,#f3f5f7)}
.s113-review-proof a:hover{color:var(--ds-accent,#c9ff4a)}

/* Turn the independent-profile block into a visible trust checkpoint, not footer-like fine print. */
.s44-trust-card{position:relative;overflow:hidden}
.s44-trust-card::after{
  content:"ПРОВЕРЯЕМО";position:absolute;right:1.1rem;top:1.1rem;
  color:var(--ds-accent,#c9ff4a);font:800 .61rem/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  letter-spacing:.08em
}

/* Reviews are relevant from every Russian landing page, so expose one stable trust anchor globally. */
.stage98-nav>a[href="/#reviews"]{color:var(--ds-text,#f3f5f7)}
.stage98-mobile-menu a[href="/#reviews"]{font-weight:760}

@media(max-width:980px){
  .s113-review-head{grid-template-columns:1fr;gap:1rem}
  .s113-review-head h2{max-width:18ch}
  .s113-review-grid{grid-template-columns:1fr}
  .s113-review-card{min-height:0}
  .s113-review-proof{grid-template-columns:1fr;gap:.35rem}
  .s113-review-proof a{margin-top:.35rem;width:max-content}
}

@media(max-width:820px){
  .s44-hero__visual::before{top:.15rem;right:.15rem;font-size:.56rem;padding:.52rem .64rem}
  .s44-proofline>a strong{font-size:1.04rem!important}
  .s113-reviews{padding:4.2rem 0}
}

@media(max-width:520px){
  .s44-hero__visual::before{content:"20 ОТЗЫВОВ · FREELANCE.RU"}
  .s113-review-head h2{font-size:clamp(2.05rem,10vw,3.15rem)}
  .s113-review-card{padding:1.15rem;border-radius:1.05rem}
}
'''


def rotate_bundle_cache() -> str:
    bundle_text = BUNDLE.read_text(encoding='utf-8')
    digest = hashlib.sha256(bundle_text.encode('utf-8')).hexdigest()[:12]
    href_re = re.compile(r'(/assets/stage105-final-ui\.css)\?v=[^"\']+', re.I)
    refs = 0
    for path in sorted(ROOT.rglob('*.html')):
        html = path.read_text(encoding='utf-8', errors='ignore')
        new, count = href_re.subn(rf'\1?v={digest}', html)
        refs += count
        if new != html:
            path.write_text(new, encoding='utf-8')
    if refs < 70:
        raise SystemExit(f'stage113: only {refs} final UI refs rotated')
    return digest


def section_end(text: str, class_token: str) -> int:
    start = text.find(class_token)
    if start < 0:
        raise SystemExit(f'stage113: section token missing: {class_token}')
    open_start = text.rfind('<section', 0, start)
    if open_start < 0:
        raise SystemExit(f'stage113: section open missing for {class_token}')
    end = text.find('</section>', start)
    if end < 0:
        raise SystemExit(f'stage113: section close missing for {class_token}')
    return end + len('</section>')


if not HOME.is_file() or not BUNDLE.is_file():
    raise SystemExit('stage113: final homepage or UI bundle missing')

case_count = len(list((ROOT / 'cases').glob('*/index.html')))
demos_html = (ROOT / 'demos' / 'index.html').read_text(encoding='utf-8')
demo_count = len(re.findall(r'<article\b[^>]*class=["\'][^"\']*\bgrowth-card\b', demos_html, re.I))
if case_count < 8 or demo_count < 3:
    raise SystemExit(f'stage113: unexpected proof inventory cases={case_count} demos={demo_count}')

html = HOME.read_text(encoding='utf-8')

# Stronger outcome-led hero while keeping all commercial terms visible in the lead.
html, n1 = re.subn(
    r'(<div class="s44-kicker"[^>]*>).*?(</div>)',
    r'\1ALEXUYS · FULLSTACK · АВТОМАТИЗАЦИЯ\2',
    html,
    count=1,
    flags=re.S,
)
html, n2 = re.subn(
    r'<h1 id="s44-hero-title">.*?</h1>',
    '<h1 id="s44-hero-title">Разработка, которая <em>доходит до рабочего запуска.</em></h1>',
    html,
    count=1,
    flags=re.S,
)
html, n3 = re.subn(
    r'<p class="s44-lead">.*?</p>',
    '<p class="s44-lead">Сайты и веб-сервисы, Telegram-боты, CRM, API-интеграции и автоматизация. Можно прийти с идеей, чужим кодом или сломанной интеграцией - сначала определяем, что должно заработать, затем собираю рабочий результат без цепочки менеджеров.</p>',
    html,
    count=1,
    flags=re.S,
)
html, n4 = re.subn(
    r'(<div class="s44-actions">\s*<a class="button primary"[^>]*>).*?(</a>)',
    r'\1Обсудить задачу ↗\2',
    html,
    count=1,
    flags=re.S,
)

proof = f'''<div aria-label="Проверяемые факты" class="s44-proofline">
<a href="{PROFILE_URL}" rel="me noopener noreferrer" target="_blank"><strong>{PROFILE_REVIEWS} отзывов</strong><span>в публичном профиле Freelance.ru</span></a>
<a href="/cases/"><strong>{case_count} кейсов</strong><span>задача, логика и реализация</span></a>
<a href="/demos/"><strong>{demo_count} демо</strong><span>можно открыть и проверить</span></a>
<a href="/about/"><strong>{PROFILE_EXPERIENCE_YEARS} лет опыта</strong><span>разработка и доработка проектов</span></a>
</div>'''
html, n5 = re.subn(
    r"<div\b(?=[^>]*\bclass=['\"][^'\"]*\bs44-proofline\b[^'\"]*['\"])[^>]*>.*?</div>",
    proof,
    html,
    count=1,
    flags=re.S,
)
html = html.replace(
    '<div class="s44-visual-note"><i></i><span>Интерфейсы из опубликованных кейсов.</span></div>',
    '<div class="s44-visual-note"><i></i><span>Откройте карточки - это реальные опубликованные кейсы.</span></div>',
    1,
)

# Make the existing trust card concrete and independently verifiable.
html = html.replace(
    '<h3>Отзывы и история работы — в публичном профиле.</h3><p>Публичный профиль Freelance.ru можно открыть до обращения. В профиле доступны отзывы заказчиков, оценки и история выполненных работ на независимой площадке.</p>',
    f'<h3>Репутацию можно проверить вне этого сайта.</h3><p>На 11 сентября 2026 в профиле Freelance.ru - {PROFILE_REVIEWS} отзывов, {PROFILE_PROFESSIONALISM}/10 за профессионализм, {PROFILE_COMMUNICATION}/10 за коммуникацию и {PROFILE_EXPERIENCE_YEARS} лет опыта. Профиль, даты и история сотрудничества открываются на независимой площадке.</p>',
    1,
)

# Insert concise public social proof directly after the portfolio, before process/pricing.
reviews = f'''
<section class="s113-reviews" id="reviews" aria-labelledby="s113-reviews-title">
  <div class="container">
    <div class="s113-review-head">
      <div><span class="s113-kicker">02 / ПУБЛИЧНАЯ РЕПУТАЦИЯ</span><h2 id="s113-reviews-title">Не нужно верить сайту на слово. <em>Есть отзывы заказчиков.</em></h2></div>
      <p>Короткие фрагменты из публичного профиля. Полная версия, авторы, даты и история работ доступны на Freelance.ru.</p>
    </div>
    <div class="s113-review-grid">
      <article class="s113-review-card"><blockquote>Отличный специалист, вник в суть, оперативно помог.</blockquote><footer><cite>Ева Григорова</cite><time datetime="2026-09-04">04.09.2026</time></footer></article>
      <article class="s113-review-card"><blockquote>Получил хороший результат!</blockquote><footer><cite>Александр Займатов</cite><time datetime="2026-07-16">16.07.2026</time></footer></article>
      <article class="s113-review-card"><blockquote>Задачу понял сразу, задал нужные вопросы, всё сдал быстро. Рекомендую.</blockquote><footer><cite>Иван</cite><time datetime="2026-05-15">15.05.2026</time></footer></article>
    </div>
    <div class="s113-review-proof"><strong>{PROFILE_REVIEWS} отзывов в профиле</strong><span>Профессионализм {PROFILE_PROFESSIONALISM}/10 · коммуникация {PROFILE_COMMUNICATION}/10 · опыт {PROFILE_EXPERIENCE_YEARS} лет</span><a href="{REVIEWS_URL}" rel="noopener noreferrer" target="_blank">Открыть все отзывы ↗</a></div>
  </div>
</section>'''
if 'class="s113-reviews"' not in html:
    end = section_end(html, 'class="portfolio-showcase"')
    html = html[:end] + reviews + html[end:]

# The old section numbering had a gap after earlier content pruning.
html = html.replace('>06 / СТАРТ</span>', '>05 / СТАРТ</span>', 1)

if not all((n1, n2, n3, n4, n5)):
    raise SystemExit(f'stage113: hero patch counts unexpected kicker={n1} h1={n2} lead={n3} cta={n4} proof={n5}')

HOME.write_text(html, encoding='utf-8')

# Add a stable Reviews entry to both desktop and mobile navigation on Russian pages.
nav_pages = 0
about_link = re.compile(r'(<a\b[^>]*href=["\']/about/["\'][^>]*>Обо мне</a>)', re.I)
for path in sorted(ROOT.rglob('*.html')):
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith('en/'):
        continue
    page = path.read_text(encoding='utf-8', errors='ignore')
    if 'stage98-header' not in page:
        continue
    if 'href="/#reviews"' in page:
        continue
    new, count = about_link.subn(r'<a href="/#reviews">Отзывы</a>\1', page)
    if count:
        path.write_text(new, encoding='utf-8')
        nav_pages += 1
if nav_pages < 40:
    raise SystemExit(f'stage113: Reviews nav patched on only {nav_pages} RU pages')

bundle_text = BUNDLE.read_text(encoding='utf-8')
if MARK not in bundle_text:
    BUNDLE.write_text(bundle_text.rstrip() + '\n\n' + CSS.strip() + '\n', encoding='utf-8')

digest = rotate_bundle_cache()

# Final guards.
final_home = HOME.read_text(encoding='utf-8')
checks = {
    'outcome hero': 'доходит до рабочего запуска' in final_home,
    'reviews section': 'id="reviews"' in final_home and final_home.count('s113-review-card') == 3,
    'verified review link': REVIEWS_URL in final_home,
    'proof counts': f'>{case_count} кейсов<' in final_home and f'>{demo_count} демо<' in final_home,
    'brief numbering': '>05 / СТАРТ</span>' in final_home,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit('stage113 guards failed: ' + ', '.join(failed))

print(
    f'stage113 client magnet: hero upgraded; cases={case_count}; demos={demo_count}; '
    f'public_reviews={PROFILE_REVIEWS}; review_cards=3; nav_pages={nav_pages}; bundle={digest}; guards OK'
)
