#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def body_page(html: str) -> str:
    m = re.search(r'<body\b[^>]*\bdata-page=["\']([^"\']+)', html, re.I)
    return m.group(1) if m else ""


def css_blocks(html: str) -> str:
    return "\n".join(re.findall(r'<style\b[^>]*>(.*?)</style>', html, re.I|re.S))


def rule_values(css: str, selector_token: str):
    # Collect simple CSS rules containing a class token, intentionally ignoring
    # media-query context; this is a source audit, not a computed-style engine.
    out=[]
    pat = re.compile(r'([^{}]+)\{([^{}]*)\}', re.S)
    for m in pat.finditer(css):
        selectors=m.group(1).strip()
        body=m.group(2)
        if selector_token not in selectors:
            continue
        vals={}
        for prop in ("padding","padding-top","padding-bottom","margin","margin-top","margin-bottom","min-height"):
            pm=re.search(rf'(?<![-\w]){re.escape(prop)}\s*:\s*([^;}}]+)', body, re.I)
            if pm: vals[prop]=pm.group(1).strip()
        if vals:
            out.append((selectors, vals))
    return out

families=defaultdict(list)
for path in sorted(root.rglob("*.html")):
    html=path.read_text(encoding="utf-8", errors="ignore")
    if "</head>" not in html or path.name.startswith(("google","yandex_")):
        continue
    rt=route(path)
    if rt in ("/404.html","/privacy/","/en/privacy/"):
        continue
    page=body_page(html)
    if rt == "/": family="home"
    elif rt.startswith("/guides/") or rt.startswith("/en/guides/"): family="guide"
    elif rt.startswith("/cases/") or rt.startswith("/en/cases/"): family="case"
    elif rt.startswith("/en/"): family="en-service"
    else: family="ru-service"
    css=css_blocks(html)
    families[family].append((rt,page,rule_values(css,".hero"),rule_values(css,".section"),rule_values(css,".contact"),rule_values(css,".cta-box")))

print("stage32 vertical rhythm audit")
for family in ("home","ru-service","guide","case","en-service"):
    rows=families.get(family,[])
    print(f"[{family}] {len(rows)} pages")
    hero=Counter(); section=Counter(); contact=Counter(); cta=Counter()
    examples=defaultdict(list)
    for rt,page,hrs,srs,crs,ctrs in rows:
        for _, vals in hrs:
            sig=tuple(sorted(vals.items())); hero[sig]+=1
            if len(examples[("hero",sig)])<3: examples[("hero",sig)].append(rt)
        for _, vals in srs:
            sig=tuple(sorted(vals.items())); section[sig]+=1
            if len(examples[("section",sig)])<3: examples[("section",sig)].append(rt)
        for _, vals in crs:
            sig=tuple(sorted(vals.items())); contact[sig]+=1
            if len(examples[("contact",sig)])<3: examples[("contact",sig)].append(rt)
        for _, vals in ctrs:
            sig=tuple(sorted(vals.items())); cta[sig]+=1
            if len(examples[("cta",sig)])<3: examples[("cta",sig)].append(rt)
    for name,counter in (("hero",hero),("section",section),("contact",contact),("cta-box",cta)):
        print(f"  {name}: {len(counter)} signatures")
        for sig,count in counter.most_common(10):
            readable=", ".join(f"{k}={v}" for k,v in sig)
            ex=", ".join(examples[("cta" if name=="cta-box" else name,sig)])
            print(f"    {count}x {readable} :: {ex}")
