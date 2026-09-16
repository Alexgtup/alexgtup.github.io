#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage167-final-design-system"

STYLE = r'''<style id="stage167-final-design-system">
/* One final visual contract for the Russian portfolio. This file intentionally
   runs after legacy art-direction stages and owns contrast, spacing and cards. */

:root{
  --s167-bg:#07090b;
  --s167-bg-2:#0a0d10;
  --s167-surface:#0d1115;
  --s167-surface-2:#11161b;
  --s167-text:#f3f6f4;
  --s167-muted:rgba(226,233,230,.70);
  --s167-soft:rgba(226,233,230,.50);
  --s167-line:rgba(255,255,255,.095);
  --s167-line-strong:rgba(255,255,255,.14);
  --s167-lime:#c9ff4a;
  --s167-coral:#ff765e;
}

body[data-ux-family="hub"],
body[data-ux-family="service"],
body[data-ux-family="case"],
body[data-ux-family="guide"]{
  color-scheme:dark;
  background:var(--s167-bg)!important;
  color:var(--s167-text)!important;
}
body[data-ux-family="hub"] main,
body[data-ux-family="service"] main,
body[data-ux-family="case"] main,
body[data-ux-family="guide"] main,
body[data-ux-family="guide"] .ux-guide-main{
  background:var(--s167-bg)!important;
  color:var(--s167-text)!important;
}
body[data-ux-family="hub"] main :is(h1,h2,h3,h4),
body[data-ux-family="service"] main :is(h1,h2,h3,h4),
body[data-ux-family="case"] main :is(h1,h2,h3,h4),
body[data-ux-family="guide"] main :is(h1,h2,h3,h4){
  color:var(--s167-text)!important;
}
body[data-ux-family="hub"] main :is(p,li),
body[data-ux-family="service"] main :is(p,li),
body[data-ux-family="case"] main :is(p,li),
body[data-ux-family="guide"] main :is(p,li){
  color:var(--s167-muted);
}
body[data-ux-family="hub"] main :is(.p130-kicker,.p129-kicker,.kicker,.eyebrow),
body[data-ux-family="service"] main :is(.p130-kicker,.p129-kicker,.kicker,.eyebrow),
body[data-ux-family="case"] main :is(.p130-kicker,.p129-kicker,.kicker,.eyebrow),
body[data-ux-family="guide"] main :is(.p130-kicker,.p129-kicker,.kicker,.eyebrow){
  color:var(--s167-soft)!important;
}

/* Search-depth sections are useful SEO content, but must look like editorial UI. */
.x146-depth{
  position:relative!important;
  margin:0!important;
  padding:0!important;
  overflow:hidden!important;
  background:
    radial-gradient(44rem 26rem at 88% 0%,rgba(108,132,255,.075),transparent 72%),
    radial-gradient(36rem 26rem at 4% 100%,rgba(201,255,74,.035),transparent 72%),
    var(--s167-bg-2)!important;
  color:var(--s167-text)!important;
  border-top:1px solid var(--s167-line)!important;
  border-bottom:1px solid var(--s167-line)!important;
}
.x146-depth__inner{
  width:min(1320px,calc(100% - 64px))!important;
  max-width:1320px!important;
  margin:0 auto!important;
  padding:clamp(72px,7vw,112px) 0!important;
}
.x146-depth__head{
  display:grid!important;
  grid-template-columns:minmax(120px,.30fr) minmax(0,1.25fr)!important;
  gap:clamp(28px,5vw,78px)!important;
  align-items:start!important;
  margin:0 0 clamp(38px,4.5vw,64px)!important;
  padding:0!important;
}
.x146-depth__eyebrow{
  margin:7px 0 0!important;
  color:var(--s167-soft)!important;
  font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace!important;
  letter-spacing:.17em!important;
  text-transform:uppercase!important;
}
.x146-depth__head h2{
  max-width:18ch!important;
  margin:0!important;
  color:var(--s167-text)!important;
  font-size:clamp(40px,4.5vw,70px)!important;
  line-height:.98!important;
  letter-spacing:-.052em!important;
  text-wrap:balance!important;
}
.x146-depth__intro{
  max-width:78ch!important;
  margin:22px 0 0!important;
  color:var(--s167-muted)!important;
  font-size:clamp(16px,1.15vw,19px)!important;
  line-height:1.72!important;
}
.x146-depth__grid{
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  gap:16px!important;
  margin:0!important;
}
.x146-depth__card{
  min-width:0!important;
  min-height:0!important;
  margin:0!important;
  padding:clamp(24px,2.5vw,34px)!important;
  border:1px solid var(--s167-line)!important;
  border-radius:24px!important;
  background:linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.012)),var(--s167-surface)!important;
  color:var(--s167-text)!important;
  box-shadow:0 18px 54px rgba(0,0,0,.18)!important;
}
.x146-depth__card h3{
  margin:0!important;
  color:var(--s167-text)!important;
  font-size:clamp(20px,1.65vw,26px)!important;
  line-height:1.12!important;
  letter-spacing:-.025em!important;
}
.x146-depth__card p{
  margin:14px 0 0!important;
  color:var(--s167-muted)!important;
  font-size:clamp(15px,1vw,17px)!important;
  line-height:1.68!important;
}
.x146-depth__links{
  display:flex!important;
  flex-wrap:wrap!important;
  gap:9px!important;
  margin:clamp(28px,3vw,42px) 0 0!important;
  padding:0!important;
}
.x146-depth__links a{
  display:inline-flex!important;
  align-items:center!important;
  min-height:40px!important;
  padding:9px 13px!important;
  border:1px solid var(--s167-line)!important;
  border-radius:999px!important;
  background:rgba(255,255,255,.025)!important;
  color:rgba(238,243,240,.82)!important;
  font-size:13px!important;
  line-height:1.25!important;
  text-decoration:none!important;
}
.x146-depth__links a:hover{border-color:rgba(201,255,74,.44)!important;color:var(--s167-text)!important;}

/* Secondary search-demand sections use the same editorial language. */
.secondary-demand{
  margin:0!important;
  padding:0!important;
  background:var(--s167-bg)!important;
  color:var(--s167-text)!important;
  border-top:1px solid var(--s167-line)!important;
}
.secondary-demand__inner{
  width:min(1320px,calc(100% - 64px))!important;
  max-width:1320px!important;
  margin:0 auto!important;
  padding:clamp(68px,6.5vw,104px) 0!important;
}
.secondary-demand__head{margin:0 0 34px!important;}
.secondary-demand__head h2{
  max-width:18ch!important;
  margin:0!important;
  color:var(--s167-text)!important;
  font-size:clamp(36px,4vw,62px)!important;
  line-height:1!important;
  letter-spacing:-.045em!important;
}
.secondary-demand__intro{
  max-width:76ch!important;
  margin:18px 0 0!important;
  color:var(--s167-muted)!important;
  font-size:clamp(16px,1.1vw,18px)!important;
  line-height:1.7!important;
}
.secondary-demand__grid{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:14px!important;
}
.secondary-demand__card{
  min-height:0!important;
  padding:24px!important;
  border:1px solid var(--s167-line)!important;
  border-radius:22px!important;
  background:var(--s167-surface)!important;
  color:var(--s167-text)!important;
}
.secondary-demand__card h3{margin:0!important;color:var(--s167-text)!important;font-size:20px!important;line-height:1.15!important;}
.secondary-demand__card p{margin:12px 0 0!important;color:var(--s167-muted)!important;font-size:15px!important;line-height:1.62!important;}
.secondary-demand__links{display:flex!important;flex-wrap:wrap!important;gap:9px!important;margin:26px 0 0!important;}
.secondary-demand__links a{
  padding:9px 12px!important;border:1px solid var(--s167-line)!important;border-radius:999px!important;
  color:rgba(238,243,240,.82)!important;text-decoration:none!important;font-size:13px!important;
}

/* Service-page conversion block: explicit contrast, no black-on-black inheritance. */
body[data-ux-family="service"] .p129-contact{
  padding:clamp(70px,7vw,108px) 0!important;
  background:var(--s167-bg)!important;
  color:var(--s167-text)!important;
}
body[data-ux-family="service"] .p129-contact>.p129-shell{
  width:min(1240px,calc(100% - 64px))!important;
  max-width:1240px!important;
  margin:0 auto!important;
}
body[data-ux-family="service"] .p129-contact-card{
  display:grid!important;
  grid-template-columns:minmax(0,1fr) auto!important;
  gap:clamp(30px,5vw,74px)!important;
  align-items:end!important;
  margin:0!important;
  padding:clamp(34px,4vw,58px)!important;
  border:1px solid var(--s167-line-strong)!important;
  border-radius:28px!important;
  background:
    radial-gradient(32rem 20rem at 86% 0%,rgba(108,132,255,.10),transparent 72%),
    linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.012)),var(--s167-surface)!important;
  color:var(--s167-text)!important;
  box-shadow:0 28px 80px rgba(0,0,0,.24)!important;
}
body[data-ux-family="service"] .p129-contact-card .p129-kicker{color:rgba(201,255,74,.68)!important;}
body[data-ux-family="service"] .p129-contact-card h2{
  max-width:13ch!important;margin:10px 0 16px!important;color:var(--s167-text)!important;
  font-size:clamp(36px,4vw,60px)!important;line-height:.98!important;letter-spacing:-.05em!important;
}
body[data-ux-family="service"] .p129-contact-card p{
  max-width:65ch!important;margin:0!important;color:var(--s167-muted)!important;font-size:16px!important;line-height:1.68!important;
}
body[data-ux-family="service"] .p129-contact-card .p129-btn{
  display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:46px!important;
  padding:12px 17px!important;border:1px solid rgba(201,255,74,.38)!important;border-radius:13px!important;
  background:var(--s167-lime)!important;color:#071008!important;font-weight:800!important;text-decoration:none!important;
}

/* Case endcaps: premium dark panel with readable demo/result CTA. */
body[data-ux-family="case"] .contact.stage108-endcap,
body[data-ux-family="case"] .p132-end{
  width:min(1320px,calc(100% - 64px))!important;
  max-width:1320px!important;
  margin:clamp(70px,7vw,112px) auto!important;
  padding:clamp(18px,2vw,28px)!important;
  border:1px solid var(--s167-line)!important;
  border-radius:30px!important;
  background:
    radial-gradient(38rem 24rem at 12% 0%,rgba(91,126,255,.22),transparent 70%),
    radial-gradient(32rem 22rem at 90% 100%,rgba(67,214,255,.14),transparent 70%),
    #0b1015!important;
  color:var(--s167-text)!important;
  box-shadow:0 28px 90px rgba(0,0,0,.26)!important;
}
body[data-ux-family="case"] .contact.stage108-endcap>.container,
body[data-ux-family="case"] .p132-end>.container{
  width:100%!important;max-width:none!important;margin:0!important;padding:0!important;
}
body[data-ux-family="case"] .status-card{
  display:grid!important;
  grid-template-columns:minmax(0,1fr) auto!important;
  gap:clamp(28px,4vw,60px)!important;
  align-items:end!important;
  margin:0!important;
  padding:clamp(30px,3.6vw,48px)!important;
  border:1px solid rgba(255,255,255,.10)!important;
  border-radius:24px!important;
  background:rgba(5,9,12,.78)!important;
  color:var(--s167-text)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04)!important;
}
body[data-ux-family="case"] .status-card h2{
  max-width:14ch!important;margin:0!important;color:var(--s167-text)!important;
  font-size:clamp(36px,4.3vw,66px)!important;line-height:.96!important;letter-spacing:-.055em!important;
}
body[data-ux-family="case"] .status-card h2 em{color:var(--s167-lime)!important;font-weight:inherit!important;}
body[data-ux-family="case"] .status-card p{
  max-width:64ch!important;margin:18px 0 0!important;color:var(--s167-muted)!important;
  font-size:clamp(15px,1.1vw,18px)!important;line-height:1.68!important;
}
body[data-ux-family="case"] .status-card .actions{display:flex!important;flex-wrap:wrap!important;justify-content:flex-end!important;gap:10px!important;}
body[data-ux-family="case"] .status-card .btn.primary{
  display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:44px!important;
  padding:11px 15px!important;border:1px solid rgba(201,255,74,.42)!important;border-radius:12px!important;
  background:var(--s167-lime)!important;color:#071008!important;font-weight:800!important;text-decoration:none!important;
}

/* Search-to-conversion bridges: readable on every page regardless of parent theme. */
.s165-bridge{
  color:var(--s167-text)!important;
  border-top-color:var(--s167-line)!important;
}
.s165-bridge h2{color:var(--s167-text)!important;}
.s165-bridge__eyebrow{color:var(--s167-soft)!important;opacity:1!important;}
.s165-bridge__copy{color:var(--s167-muted)!important;opacity:1!important;}
.s165-bridge__links{border-top-color:var(--s167-line)!important;}
.s165-bridge__link{color:var(--s167-text)!important;border-bottom-color:var(--s167-line)!important;}
.s165-bridge__link:nth-child(even){border-left-color:var(--s167-line)!important;}
.s165-bridge__link strong{color:var(--s167-text)!important;}
.s165-bridge__link span{color:var(--s167-soft)!important;opacity:1!important;}
.s165-bridge__contact{color:var(--s167-muted)!important;opacity:1!important;}
.s165-bridge__contact a{color:var(--s167-text)!important;}

/* Related-navigation fragments should look intentional, not like stray underlined text. */
.s101-more.s107-related{
  width:min(1320px,calc(100% - 64px))!important;
  max-width:1320px!important;
  margin:28px auto 0!important;
  padding:0!important;
  background:transparent!important;
  border:0!important;
}
.s101-more.s107-related a{
  display:inline-flex!important;align-items:center!important;min-height:40px!important;padding:9px 13px!important;
  border:1px solid var(--s167-line)!important;border-radius:999px!important;background:rgba(255,255,255,.025)!important;
  color:rgba(238,243,240,.78)!important;text-decoration:none!important;font-size:13px!important;
}

/* Hub CTAs and cards stay in the same dark material system. */
body[data-ux-family="hub"] .p130-footer-cta{
  background:var(--s167-bg)!important;color:var(--s167-text)!important;border-top:1px solid var(--s167-line)!important;
}
body[data-ux-family="hub"] .p130-footer-cta h2{color:var(--s167-text)!important;}
body[data-ux-family="hub"] .p130-footer-cta p{color:var(--s167-muted)!important;}
body[data-ux-family="hub"] .p130-footer-cta .p129-btn{
  border-color:rgba(201,255,74,.36)!important;background:var(--s167-lime)!important;color:#071008!important;font-weight:800!important;
}

/* Keep reveal content deterministic after old motion layers have been retired. */
body[data-ux-family="hub"] .wow-reveal,
body[data-ux-family="service"] .wow-reveal,
body[data-ux-family="case"] .wow-reveal,
body[data-ux-family="guide"] .wow-reveal{
  opacity:1!important;visibility:visible!important;transform:none!important;translate:none!important;filter:none!important;
}

@media(max-width:980px){
  .x146-depth__inner,.secondary-demand__inner,
  body[data-ux-family="service"] .p129-contact>.p129-shell,
  body[data-ux-family="case"] .contact.stage108-endcap,
  body[data-ux-family="case"] .p132-end,
  .s101-more.s107-related{
    width:min(100% - 28px,860px)!important;
  }
  .x146-depth__head{grid-template-columns:1fr!important;gap:16px!important;}
  .x146-depth__eyebrow{margin:0!important;}
  .x146-depth__grid{grid-template-columns:1fr!important;}
  .secondary-demand__grid{grid-template-columns:1fr!important;}
  body[data-ux-family="service"] .p129-contact-card,
  body[data-ux-family="case"] .status-card{grid-template-columns:1fr!important;align-items:start!important;}
  body[data-ux-family="case"] .status-card .actions{justify-content:flex-start!important;}
}
@media(max-width:600px){
  .x146-depth__inner,.secondary-demand__inner,
  body[data-ux-family="service"] .p129-contact>.p129-shell,
  body[data-ux-family="case"] .contact.stage108-endcap,
  body[data-ux-family="case"] .p132-end,
  .s101-more.s107-related{
    width:calc(100% - 24px)!important;
  }
  .x146-depth__inner{padding:58px 0!important;}
  .x146-depth__head h2{font-size:clamp(34px,10vw,48px)!important;}
  .x146-depth__card{padding:22px!important;border-radius:20px!important;}
  body[data-ux-family="service"] .p129-contact-card,
  body[data-ux-family="case"] .status-card{padding:24px!important;border-radius:22px!important;}
  body[data-ux-family="case"] .contact.stage108-endcap,
  body[data-ux-family="case"] .p132-end{padding:10px!important;border-radius:24px!important;}
  .s165-bridge__link:nth-child(even){border-left:0!important;}
}
</style>'''

changed = []
for path in sorted(ROOT.rglob("index.html")):
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        continue
    text = path.read_text(encoding="utf-8")
    if "</head>" not in text:
        continue
    text = re.sub(
        r'<style\s+id=["\']stage167-final-design-system["\']>.*?</style>',
        '',
        text,
        flags=re.I | re.S,
    )
    text = text.replace("</head>", STYLE + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(rel)

required = [
    "cases/index.html",
    "cases/sheetpilot-ai/index.html",
    "python-development/index.html",
    "api-integrations/index.html",
    "services/index.html",
    "guides/index.html",
]
for rel in required:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"stage167: missing required page {rel}")
    text = path.read_text(encoding="utf-8")
    if text.count(MARKER) != 1:
        raise SystemExit(f"stage167: marker count invalid for {rel}")

print(f"stage167 final design system: {len(changed)} pages normalized")
