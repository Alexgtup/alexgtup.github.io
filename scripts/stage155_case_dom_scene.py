#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage155-case-dom-scene"

STYLE = r'''<style id="stage155-case-dom-scene">
@media (min-width:981px){
  body[data-x135-family="cinematic"] .p155-cover{
    position:relative!important;
    min-height:calc(88vh - 64px)!important;
    padding:clamp(54px,5vw,82px) 0!important;
    overflow:hidden!important;
    background:#070a0c!important;
  }
  body[data-x135-family="cinematic"] .p155-cover::before,
  body[data-x135-family="cinematic"] .p155-cover::after{
    display:none!important;
    content:none!important;
  }
  body[data-x135-family="cinematic"] .p155-band{
    position:absolute!important;
    left:0!important;
    top:18%!important;
    bottom:10%!important;
    width:min(64vw,980px)!important;
    border-radius:0 34px 34px 0!important;
    display:flex!important;
    align-items:center!important;
    background:
      radial-gradient(48rem 28rem at 12% 30%,rgba(72,126,86,.19),transparent 70%),
      radial-gradient(34rem 22rem at 88% 86%,rgba(190,216,91,.065),transparent 72%),
      linear-gradient(110deg,rgba(18,34,27,.97),rgba(15,23,22,.93) 58%,rgba(14,18,20,.87))!important;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.035),0 28px 90px rgba(0,0,0,.24)!important;
    overflow:hidden!important;
  }
  body[data-x135-family="cinematic"] .p155-band::after{
    content:""!important;
    position:absolute!important;
    inset:0!important;
    background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.014) 1px,transparent 1px)!important;
    background-size:36px 36px!important;
    -webkit-mask-image:linear-gradient(90deg,#000 0%,rgba(0,0,0,.9) 68%,transparent 100%)!important;
    mask-image:linear-gradient(90deg,#000 0%,rgba(0,0,0,.9) 68%,transparent 100%)!important;
    pointer-events:none!important;
  }
  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy{
    position:relative!important;
    z-index:2!important;
    left:auto!important;
    right:auto!important;
    top:auto!important;
    bottom:auto!important;
    transform:none!important;
    translate:none!important;
    width:min(760px,calc(100% - 92px))!important;
    max-width:760px!important;
    min-width:0!important;
    min-height:0!important;
    margin-left:max(36px,calc((100vw - 1380px)/2 + 36px))!important;
    margin-right:0!important;
    padding:0!important;
    display:block!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
    -webkit-backdrop-filter:none!important;
    overflow:visible!important;
  }
  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy::before,
  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy::after{
    display:none!important;
    content:none!important;
  }
  body[data-x135-family="cinematic"] .p155-band .p132-cover h1,
  body[data-x135-family="cinematic"] .p155-band h1{
    width:100%!important;
    max-width:12.8ch!important;
    margin:.8rem 0 1.05rem!important;
    font-size:clamp(52px,4.4vw,82px)!important;
    line-height:.92!important;
    letter-spacing:-.055em!important;
    color:#f5f7f4!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }
  body[data-x135-family="cinematic"] .p155-band h1 :is(em,span){color:#a8e7a8!important;}
  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy>p:not(.p132-eyebrow){
    max-width:48ch!important;
    margin:0!important;
    color:rgba(236,241,238,.84)!important;
    font-size:clamp(16px,1.05vw,18px)!important;
    line-height:1.66!important;
    text-wrap:pretty!important;
  }
  body[data-x135-family="cinematic"] .p155-band .p132-cover-actions{margin-top:1.55rem!important;}
  body[data-x135-family="cinematic"] .p155-preview{
    position:absolute!important;
    z-index:3!important;
    right:max(36px,calc((100vw - 1380px)/2 + 36px))!important;
    top:50%!important;
    transform:translateY(-50%)!important;
    width:min(340px,25vw)!important;
  }
  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:none!important;
    min-width:0!important;
    min-height:0!important;
    height:auto!important;
    aspect-ratio:4/3!important;
    margin:0!important;
    border-radius:26px!important;
    overflow:hidden!important;
    box-shadow:0 26px 78px rgba(0,0,0,.34)!important;
  }
  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual img{
    width:100%!important;height:100%!important;min-height:0!important;object-fit:cover!important;object-position:center!important;
  }

  body[data-x135-family="cinematic"] .p155-service-hero{
    position:relative!important;
    min-height:calc(88vh - 64px)!important;
    padding:clamp(54px,5vw,82px) 0!important;
    overflow:hidden!important;
  }
  body[data-x135-family="cinematic"] .p155-service-band{
    position:absolute!important;
    left:0!important;top:18%!important;bottom:10%!important;width:min(64vw,980px)!important;
    border-radius:0 34px 34px 0!important;display:flex!important;align-items:center!important;
    background:linear-gradient(110deg,rgba(42,24,25,.96),rgba(30,22,23,.92) 58%,rgba(18,18,20,.87))!important;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.035),0 28px 90px rgba(0,0,0,.24)!important;
  }
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy{
    position:relative!important;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;transform:none!important;translate:none!important;
    width:min(780px,calc(100% - 92px))!important;max-width:780px!important;margin-left:max(36px,calc((100vw - 1380px)/2 + 36px))!important;margin-right:0!important;padding:0!important;
    border:0!important;background:transparent!important;box-shadow:none!important;
  }
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{max-width:12.8ch!important;font-size:clamp(52px,4.4vw,82px)!important;line-height:.92!important;text-wrap:balance!important;}
  body[data-x135-family="cinematic"] .p155-service-band .p129-lead{max-width:48ch!important;font-size:clamp(16px,1.05vw,18px)!important;line-height:1.66!important;}
  body[data-x135-family="cinematic"] .p155-service-preview{
    position:absolute!important;right:max(36px,calc((100vw - 1380px)/2 + 36px))!important;top:50%!important;transform:translateY(-50%)!important;width:min(340px,25vw)!important;
  }
  body[data-x135-family="cinematic"] .p155-service-preview .p129-svc-board{
    position:relative!important;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;transform:none!important;translate:none!important;width:100%!important;max-width:none!important;margin:0!important;
  }
}

@media(max-width:980px){
  body[data-x135-family="cinematic"] .p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{min-height:0!important;padding:38px 0 56px!important;display:grid!important;gap:22px!important;}
  body[data-x135-family="cinematic"] .p155-band,
  body[data-x135-family="cinematic"] .p155-service-band{
    position:relative!important;left:auto!important;top:auto!important;bottom:auto!important;width:calc(100% - 24px)!important;margin:0!important;border-radius:0 26px 26px 0!important;min-height:0!important;padding:34px 0!important;
  }
  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy{
    width:calc(100% - 40px)!important;max-width:none!important;margin:0 20px!important;padding:0!important;
  }
  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{max-width:100%!important;font-size:clamp(46px,10vw,74px)!important;}
  body[data-x135-family="cinematic"] .p155-preview,
  body[data-x135-family="cinematic"] .p155-service-preview{
    position:relative!important;right:auto!important;top:auto!important;transform:none!important;width:calc(100% - 32px)!important;max-width:520px!important;margin:0 16px!important;
  }
}
</style>'''

TAG_RE = re.compile(r'<(?P<close>/)?(?P<tag>[a-zA-Z0-9]+)\b[^>]*>')

def extract_balanced(text: str, start: int, tag: str) -> tuple[str, int]:
    depth = 0
    for m in TAG_RE.finditer(text, start):
        if m.group('tag').lower() != tag:
            continue
        if m.group('close'):
            depth -= 1
            if depth == 0:
                return text[start:m.end()], m.end()
        else:
            depth += 1
    raise RuntimeError(f'unbalanced <{tag}> at {start}')

def extract_class_block(text: str, class_name: str, tag: str = 'div') -> str:
    m = re.search(rf'<{tag}\b[^>]*class="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*>', text)
    if not m:
        raise RuntimeError(f'missing {class_name}')
    block, _ = extract_balanced(text, m.start(), tag)
    return block

def replace_section(text: str, marker_class: str, replacement: str) -> str:
    m = re.search(rf'<section\b[^>]*class="[^"]*\b{re.escape(marker_class)}\b[^"]*"[^>]*>', text)
    if not m:
        raise RuntimeError(f'missing section {marker_class}')
    _, end = extract_balanced(text, m.start(), 'section')
    return text[:m.start()] + replacement + text[end:]

case_count = 0
service_count = 0
for path in sorted(ROOT.rglob('index.html')):
    html = path.read_text(encoding='utf-8')
    old = html

    if 'class="p132-cover"' in html and 'p132-cover-copy' in html and 'p132-cover-visual' in html:
        section_match = re.search(r'<section\b[^>]*class="[^"]*\bp132-cover\b[^"]*"[^>]*>', html)
        if section_match:
            section, _ = extract_balanced(html, section_match.start(), 'section')
            copy = extract_class_block(section, 'p132-cover-copy')
            visual = extract_class_block(section, 'p132-cover-visual')
            new_section = '<section class="p132-cover p155-cover" data-stage155-case-scene="true"><div class="p155-band">' + copy + '</div><div class="p155-preview">' + visual + '</div></section>'
            html = replace_section(html, 'p132-cover', new_section)
            case_count += 1

    if 'class="p129-svc-hero"' in html and 'p129-svc-copy' in html and 'p129-svc-board' in html:
        section_match = re.search(r'<section\b[^>]*class="[^"]*\bp129-svc-hero\b[^"]*"[^>]*>', html)
        if section_match:
            section, _ = extract_balanced(html, section_match.start(), 'section')
            copy = extract_class_block(section, 'p129-svc-copy')
            board = extract_class_block(section, 'p129-svc-board', 'aside')
            new_section = '<section class="p129-svc-hero p155-service-hero" data-stage155-service-scene="true"><div class="p155-service-band">' + copy + '</div><div class="p155-service-preview">' + board + '</div></section>'
            html = replace_section(html, 'p129-svc-hero', new_section)
            service_count += 1

    if html != old:
        if MARKER not in html:
            if '</head>' not in html:
                raise RuntimeError(f'head missing: {path}')
            html = html.replace('</head>', STYLE + '</head>', 1)
        path.write_text(html, encoding='utf-8')

if case_count == 0:
    raise SystemExit('stage155: no detail case heroes rebuilt')

for path in sorted((ROOT / 'cases').glob('*/index.html')):
    html = path.read_text(encoding='utf-8')
    if 'p132-cover-copy' in html and 'data-stage155-case-scene="true"' not in html:
        raise SystemExit(f'stage155: case scene guard failed: {path}')

print(f'stage155 case DOM scene: {case_count} cases, {service_count} service heroes')
