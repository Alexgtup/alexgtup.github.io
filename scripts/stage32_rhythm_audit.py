#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict
from html.parser import HTMLParser
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
    # Source audit only. Effective shared overrides live in layout-system.css.
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


class HeadingParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = None
        self.buf = []
        self.headings = []
        self.ignore = 0
    def handle_starttag(self, tag, attrs):
        tag=tag.lower()
        if tag in ("script","style","template","noscript"):
            self.ignore += 1
            return
        if not self.ignore and tag in ("h1","h2"):
            self.active=tag; self.buf=[]
    def handle_data(self, data):
        if self.active and not self.ignore:
            self.buf.append(data)
    def handle_endtag(self, tag):
        tag=tag.lower()
        if tag in ("script","style","template","noscript"):
            if self.ignore: self.ignore -= 1
            return
        if self.active == tag:
            text=re.sub(r'\s+',' ',' '.join(self.buf)).strip()
            if text: self.headings.append((tag,text))
            self.active=None; self.buf=[]


families=defaultdict(list)
typography=[]
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

    hp=HeadingParser(); hp.feed(html)
    for tag,text in hp.headings:
        tokens=re.findall(r'\S+', text)
        longest=max(tokens,key=len) if tokens else ""
        typography.append((len(text),len(longest),rt,tag,text,longest))

print("stage32 vertical rhythm source audit")
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

print("stage32 mobile typography review")
long_h1=sorted((x for x in typography if x[3]=="h1"), reverse=True)[:15]
long_h2=sorted((x for x in typography if x[3]=="h2"), reverse=True)[:15]
long_tokens=sorted(typography,key=lambda x:x[1],reverse=True)[:15]
print("  longest H1:")
for chars,toklen,rt,tag,text,token in long_h1:
    print(f"    {chars} chars :: {rt} :: {text[:125]}")
print("  longest H2:")
for chars,toklen,rt,tag,text,token in long_h2:
    print(f"    {chars} chars :: {rt} :: {text[:125]}")
print("  longest heading tokens:")
for chars,toklen,rt,tag,text,token in long_tokens:
    if toklen < 18: break
    print(f"    {toklen} chars :: {rt} :: {tag} :: {token[:80]}")

risks=[]
for chars,toklen,rt,tag,text,token in typography:
    if (tag=="h1" and chars>95) or (tag=="h2" and chars>120) or toklen>32:
        risks.append((rt,tag,chars,toklen,text))
print(f"  review-threshold risks: {len(risks)}")
for rt,tag,chars,toklen,text in risks[:30]:
    print(f"    {rt} :: {tag} :: {chars} chars / token {toklen} :: {text[:130]}")
