#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
home = root / "index.html"
if not home.is_file():
    raise SystemExit("stage59: homepage missing")
home_before = hashlib.sha256(home.read_bytes()).hexdigest()

SLUGS = ("n8n-vs-backend", "site-vs-web-app", "repair-vs-rewrite")

STYLE = r'''<style data-stage59-decision-guide-header>
.s59-header{position:sticky;top:0;z-index:100;background:rgba(8,9,11,.68)!important;backdrop-filter:blur(20px) saturate(135%);-webkit-backdrop-filter:blur(20px) saturate(135%);border-bottom:1px solid rgba(255,255,255,.075)!important}
.s59-shell{width:min(100%,92rem);margin-inline:auto;padding-inline:clamp(1.15rem,4vw,4.5rem)}
.s59-header-inner{min-height:5rem;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:1.5rem}
.s59-brand{display:inline-flex;align-items:center;gap:.8rem;width:max-content;color:#f4f5f2;text-decoration:none}
.s59-mark{width:2.4rem;aspect-ratio:1;border-radius:.78rem;display:grid;place-items:center;border:1px solid rgba(255,255,255,.13);background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.015));box-shadow:inset 0 1px rgba(255,255,255,.05)}
.s59-mark svg{width:1.72rem;height:1.72rem}
.s59-brand-copy{display:grid;gap:.15rem;line-height:1}
.s59-brand-copy strong{font-size:.93rem;letter-spacing:-.025em}
.s59-brand-copy small{font:600 .5rem/1.2 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;letter-spacing:.12em;color:#747b84}
.s59-nav{display:flex;align-items:center;gap:1.8rem}
.s59-nav a{color:#b8bdc4;text-decoration:none;font-size:.88rem;transition:color .18s ease}
.s59-nav a:hover,.s59-nav a[aria-current="page"]{color:#f4f5f2}
.s59-lang{display:grid!important;place-items:center;width:2.35rem;height:2.35rem;border:1px solid rgba(255,255,255,.12);border-radius:.72rem;color:#d9dde1!important;font-size:.72rem!important}
.s59-action{justify-self:end;display:inline-flex;align-items:center;gap:.55rem;color:#f4f5f2;text-decoration:none;font-size:.88rem;font-weight:700;white-space:nowrap}
.s59-action svg{transition:transform .18s ease}.s59-action:hover svg{transform:translate(2px,-2px)}
@media(max-width:980px){.s59-nav{gap:1rem}.s59-nav a{font-size:.8rem}.s59-brand-copy small{display:none}}
@media(max-width:760px){.s59-header{position:relative!important;top:auto!important}.s59-header-inner{grid-template-columns:minmax(0,1fr) auto;min-height:4.4rem}.s59-nav{display:none}.s59-action{font-size:.8rem;padding:.58rem .72rem;border:1px solid rgba(255,255,255,.11);border-radius:.72rem;background:rgba(255,255,255,.03)}.s59-brand-copy small{display:block}}
@media(max-width:430px){.s59-brand-copy small{display:none}.s59-mark{width:2.2rem}.s59-action{font-size:0}.s59-action::before{content:"Telegram";font-size:.78rem}.s59-action svg{width:13px;height:13px}}
</style>'''

HEADER = r'''<header class="header s59-header" data-stage59-header data-nosnippet=""><div class="s59-shell s59-header-inner"><a class="s59-brand" href="/" aria-label="Alexuys — на главную"><span class="s59-mark" aria-hidden="true"><svg fill="none" viewBox="0 0 32 32"><path d="M8.5 9.5 14 15l-5.5 5.5" stroke="#c9ff4a" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2"/><path d="M16 21h7.5" stroke="#8195ff" stroke-linecap="round" stroke-width="2.2"/><circle cx="24" cy="8" r="2.2" fill="#c9ff4a"/></svg></span><span class="s59-brand-copy"><strong>alexuys</strong><small>AI · WEB · AUTOMATION</small></span></a><nav class="s59-nav" aria-label="Основная навигация" data-nosnippet=""><a href="/cases/">Кейсы</a><a href="/services/">Услуги</a><a href="/guides/" aria-current="page">Разборы</a><a href="/#process">Процесс</a><a href="/about/">Обо мне</a><a class="s59-lang" href="/en/" hreflang="en" lang="en" aria-label="English version">EN</a></nav><a class="s59-action" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить проект <svg fill="none" height="15" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="15" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></a></div></header>'''

changed = 0
for slug in SLUGS:
    page = root / "guides" / slug / "index.html"
    if not page.is_file():
        raise SystemExit(f"stage59: missing {page}")

    text = page.read_text(encoding="utf-8", errors="ignore")
    original = text

    # Stage 54 creates a deliberately self-contained article shell. Replace only
    # its header, leaving article/SEO content and the homepage untouched.
    text, n = re.subn(
        r'<header\s+class=["\']header["\'][^>]*>.*?</header>',
        HEADER,
        text,
        count=1,
        flags=re.I | re.S,
    )
    if n != 1:
        raise SystemExit(f"stage59: expected one legacy header on /guides/{slug}/")

    if "data-stage59-decision-guide-header" not in text:
        pos = text.lower().find("</head>")
        if pos < 0:
            raise SystemExit(f"stage59: /guides/{slug}/ missing </head>")
        text = text[:pos] + STYLE + text[pos:]

    if text != original:
        page.write_text(text, encoding="utf-8")
        changed += 1

# Invariants: all three decision guides use one consistent shell and the homepage
# remains byte-for-byte unchanged.
for slug in SLUGS:
    text = (root / "guides" / slug / "index.html").read_text(encoding="utf-8", errors="ignore")
    if text.count("data-stage59-header") != 1:
        raise SystemExit(f"stage59: normalized header missing on /guides/{slug}/")
    if "s59-brand-copy" not in text or "Обсудить проект" not in text:
        raise SystemExit(f"stage59: header content incomplete on /guides/{slug}/")

home_after = hashlib.sha256(home.read_bytes()).hexdigest()
if home_after != home_before:
    raise SystemExit("stage59: homepage changed; forbidden")

print("stage59 decision-guide header:")
print(f"  normalized pages: {changed}")
print(f"  homepage sha256 unchanged: {home_after}")
