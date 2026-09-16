#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage157-designer-case-hero"

STYLE = r'''<style id="stage157-designer-case-hero">
body[data-ux-family="case"] .p132-cover.p155-cover{
  position:relative!important;display:grid!important;
  grid-template-columns:minmax(0,1.08fr) minmax(520px,.92fr)!important;
  align-items:center!important;gap:clamp(48px,5.5vw,96px)!important;
  width:min(1480px,calc(100% - 64px))!important;max-width:1480px!important;
  min-height:clamp(620px,52vw,820px)!important;
  margin:clamp(56px,6vw,96px) auto clamp(88px,8vw,132px)!important;
  padding:clamp(18px,2vw,32px) 0!important;overflow:visible!important;isolation:isolate!important;
  border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;
  backdrop-filter:none!important;-webkit-backdrop-filter:none!important;
}
body[data-ux-family="case"] .p132-cover.p155-cover::before{
  content:""!important;position:absolute!important;z-index:-1!important;right:-8%!important;top:50%!important;
  width:min(760px,52vw)!important;aspect-ratio:1!important;transform:translateY(-50%)!important;border-radius:50%!important;
  background:radial-gradient(circle,rgba(96,126,255,.12) 0%,rgba(73,119,91,.06) 40%,transparent 72%)!important;
  filter:blur(12px)!important;pointer-events:none!important;
}
body[data-ux-family="case"] .p132-cover.p155-cover::after{
  content:""!important;position:absolute!important;left:0!important;right:0!important;bottom:-40px!important;height:1px!important;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.08) 16%,rgba(255,255,255,.08) 84%,transparent)!important;pointer-events:none!important;
}
body[data-ux-family="case"] .p155-band,
body[data-ux-family="case"] .p155-band .p132-cover-copy{
  position:relative!important;inset:auto!important;transform:none!important;translate:none!important;
  width:100%!important;max-width:none!important;min-width:0!important;min-height:0!important;height:auto!important;
  margin:0!important;padding:0!important;display:block!important;border:0!important;border-radius:0!important;
  background:transparent!important;box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;overflow:visible!important;
}
body[data-ux-family="case"] .p155-band::before,
body[data-ux-family="case"] .p155-band::after,
body[data-ux-family="case"] .p155-band .p132-cover-copy::before,
body[data-ux-family="case"] .p155-band .p132-cover-copy::after{content:none!important;display:none!important;}
body[data-ux-family="case"] .p155-band .p132-eyebrow{
  margin:0 0 22px!important;color:rgba(226,233,228,.56)!important;font-size:12px!important;line-height:1.35!important;
  letter-spacing:.2em!important;text-transform:uppercase!important;
}
body[data-ux-family="case"] .p155-band h1{
  width:100%!important;max-width:none!important;margin:0 0 30px!important;
  font-size:clamp(72px,6.4vw,118px)!important;line-height:.88!important;letter-spacing:-.07em!important;
  color:#f5f7f4!important;text-wrap:pretty!important;overflow-wrap:normal!important;word-break:normal!important;
}
body[data-ux-family="case"] .p155-band h1 :is(em,span){color:#a8e0a4!important;}
body[data-ux-family="case"] .p155-band .p132-cover-copy>p:not(.p132-eyebrow){
  width:100%!important;max-width:68ch!important;margin:0!important;color:rgba(234,239,236,.76)!important;
  font-size:clamp(18px,1.22vw,22px)!important;line-height:1.7!important;text-wrap:pretty!important;
}
body[data-ux-family="case"] .p155-band .p132-cover-actions{
  margin-top:36px!important;display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:14px 22px!important;
}
body[data-ux-family="case"] .p155-preview{
  position:relative!important;inset:auto!important;transform:none!important;translate:none!important;
  width:100%!important;max-width:720px!important;min-width:0!important;margin:0!important;align-self:center!important;justify-self:end!important;
}
body[data-ux-family="case"] .p155-preview::before{
  content:""!important;position:absolute!important;z-index:-1!important;inset:8% 6% -10% 6%!important;border-radius:38px!important;
  background:linear-gradient(135deg,rgba(111,141,255,.16),rgba(78,137,96,.08))!important;filter:blur(54px)!important;opacity:.82!important;pointer-events:none!important;
}
body[data-ux-family="case"] .p155-preview .p132-cover-visual{
  position:relative!important;inset:auto!important;transform:none!important;translate:none!important;
  width:100%!important;max-width:none!important;min-width:0!important;min-height:0!important;height:auto!important;aspect-ratio:16/10!important;margin:0!important;
  border:1px solid rgba(255,255,255,.09)!important;border-radius:28px!important;overflow:hidden!important;background:rgba(255,255,255,.02)!important;
  box-shadow:0 36px 96px rgba(0,0,0,.42),inset 0 1px 0 rgba(255,255,255,.04)!important;
}
body[data-ux-family="case"] .p155-preview .p132-cover-visual img{
  width:100%!important;height:100%!important;min-height:0!important;object-fit:cover!important;object-position:center!important;
}
@media (max-width:1180px) and (min-width:981px){
  body[data-ux-family="case"] .p132-cover.p155-cover{grid-template-columns:minmax(0,1fr) minmax(420px,.9fr)!important;gap:42px!important;width:min(1140px,calc(100% - 48px))!important;}
  body[data-ux-family="case"] .p155-band h1{font-size:clamp(62px,6vw,88px)!important;}
}
@media (max-width:980px){
  body[data-ux-family="case"] .p132-cover.p155-cover{display:grid!important;grid-template-columns:1fr!important;gap:44px!important;width:min(100% - 28px,860px)!important;min-height:0!important;margin:40px auto 72px!important;padding:0!important;}
  body[data-ux-family="case"] .p132-cover.p155-cover::before,
  body[data-ux-family="case"] .p132-cover.p155-cover::after{content:none!important;display:none!important;}
  body[data-ux-family="case"] .p155-band,
  body[data-ux-family="case"] .p155-band .p132-cover-copy{position:relative!important;inset:auto!important;transform:none!important;translate:none!important;width:100%!important;max-width:none!important;min-height:0!important;margin:0!important;padding:0!important;}
  body[data-ux-family="case"] .p155-band h1{max-width:none!important;margin-bottom:24px!important;font-size:clamp(52px,11vw,82px)!important;line-height:.91!important;}
  body[data-ux-family="case"] .p155-band .p132-cover-copy>p:not(.p132-eyebrow){max-width:70ch!important;}
  body[data-ux-family="case"] .p155-preview{width:100%!important;max-width:760px!important;justify-self:start!important;}
}
@media (max-width:600px){
  body[data-ux-family="case"] .p132-cover.p155-cover{width:calc(100% - 24px)!important;gap:30px!important;margin-top:32px!important;}
  body[data-ux-family="case"] .p155-band h1{font-size:clamp(46px,13.5vw,68px)!important;}
  body[data-ux-family="case"] .p155-preview .p132-cover-visual{border-radius:22px!important;}
}
</style>'''

OLD_STYLE_IDS_RE = re.compile(
    r'<style\b[^>]*id="(?:stage153-case-left-panel|stage154-text-into-existing-band|stage154-case-left-band|stage155-case-dom-scene|stage156-stable-hero-layout(?:-v2)?|stage157-designer-case-hero)"[^>]*>.*?</style>',
    re.I | re.S,
)
RUNTIME_SCRIPT_RE = re.compile(
    r'<script\b[^>]*src="/assets/(?:stage134-experimental-web|stage135-world-system)\.js[^\"]*"[^>]*>\s*</script>',
    re.I | re.S,
)

def clean_case_html(html: str) -> str:
    html = OLD_STYLE_IDS_RE.sub('', html)
    html = RUNTIME_SCRIPT_RE.sub('', html)
    html = re.sub(r'\sdata-x134="[^"]*"', '', html, count=1)
    html = re.sub(r'\sdata-x135="[^"]*"', '', html, count=1)
    html = re.sub(r'\sdata-x135-family="[^"]*"', '', html, count=1)
    return html

case_pages = sorted((ROOT / 'cases').glob('*/index.html')) if (ROOT / 'cases').is_dir() else []
if not case_pages:
    raise SystemExit('stage157: no case pages found')

changed = 0
for path in case_pages:
    html = path.read_text(encoding='utf-8')
    if 'p155-cover' not in html or 'p155-band' not in html or 'p155-preview' not in html:
        raise SystemExit(f'stage157: p155 scene missing: {path}')
    html = clean_case_html(html)
    if '</head>' not in html:
        raise SystemExit(f'stage157: head missing: {path}')
    html = html.replace('</head>', STYLE + '</head>', 1)
    path.write_text(html, encoding='utf-8')
    changed += 1

for path in case_pages:
    html = path.read_text(encoding='utf-8')
    if html.count(f'id="{MARKER}"') != 1:
        raise SystemExit(f'stage157: final style guard failed: {path}')
    if 'stage134-experimental-web.js' in html or 'stage135-world-system.js' in html:
        raise SystemExit(f'stage157: runtime cleanup failed: {path}')
    body = re.search(r'<body\b[^>]*>', html, re.I)
    body_tag = body.group(0) if body else ''
    if 'data-x134=' in body_tag or 'data-x135=' in body_tag or 'data-x135-family=' in body_tag:
        raise SystemExit(f'stage157: body runtime flags remain: {path}')

print(f'stage157 stable editorial case hero: {changed} case pages')
