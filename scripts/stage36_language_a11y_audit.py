#!/usr/bin/env python3
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter, defaultdict
from urllib.parse import urlsplit
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
CYR = re.compile(r"[А-Яа-яЁё]")
SPACE = re.compile(r"\s+")
SUSPICIOUS = re.compile(
    r"\b(?:todo|tbd|placeholder|lorem ipsum|coming soon)\b|"
    r"(?:демо готовится|готовится к публикации|добавлю сюда|добавим сюда|скоро добавим|в разработке)",
    re.I,
)
HIDDEN_STYLE = re.compile(r"(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden)\b", re.I)


def route(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def clean(text: str) -> str:
    return SPACE.sub(" ", text).strip()


def is_ru_switch(attrs: dict[str, str]) -> bool:
    lang = (attrs.get("lang") or "").lower()
    hreflang = (attrs.get("hreflang") or "").lower()
    href = attrs.get("href") or ""
    return lang.startswith("ru") or hreflang == "ru" or (href.startswith("/") and not href.startswith("/en/"))


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.stack: list[dict] = []
        self.ids: list[str] = []
        self.href_fragments: list[str] = []
        self.en_cyrillic: list[str] = []
        self.en_cyrillic_attrs: list[str] = []
        self.buttons: list[dict] = []
        self.links: list[dict] = []
        self.images: list[dict] = []
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self.iframes_without_title = 0
        self.inputs_without_name = 0
        self.main_count = 0
        self.header_count = 0
        self.footer_count = 0
        self.h1_count = 0
        self.title_count = 0
        self.canonical: list[str] = []
        self.meta_names: list[str] = []
        self.meta_props: list[str] = []
        self.skip_links: list[str] = []
        self.visible_chunks: list[str] = []
        self._ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower(); a = {k.lower(): (v or "") for k,v in attrs}
        if tag == "html": self.html_lang = a.get("lang", "")
        if a.get("id"): self.ids.append(a["id"])
        if tag == "main": self.main_count += 1
        if tag == "header": self.header_count += 1
        if tag == "footer": self.footer_count += 1
        if tag == "h1": self.h1_count += 1
        if tag == "title": self.title_count += 1
        if tag == "link":
            rel = set((a.get("rel") or "").lower().split())
            href = a.get("href", "")
            if "canonical" in rel and href: self.canonical.append(href)
            if "stylesheet" in rel and href: self.stylesheets.append(href)
        if tag == "script" and a.get("src"): self.scripts.append(a["src"])
        if tag == "meta":
            if a.get("name"): self.meta_names.append(a["name"].lower())
            if a.get("property"): self.meta_props.append(a["property"].lower())
        if tag == "img": self.images.append(a)
        if tag == "iframe" and not clean(a.get("title", "")):
            self.iframes_without_title += 1
        if tag in ("input", "select", "textarea"):
            typ = (a.get("type") or "").lower()
            if typ not in ("hidden", "submit", "button", "reset") and not any(clean(a.get(k,"")) for k in ("aria-label","aria-labelledby","title","placeholder","name")):
                self.inputs_without_name += 1
        if tag == "a":
            href = a.get("href", "")
            if href.startswith("#") and len(href) > 1: self.href_fragments.append(href[1:])
            classes = set((a.get("class") or "").split())
            if "skip-link" in classes and href.startswith("#"): self.skip_links.append(href[1:])

        ignored = tag in ("script","style","template","noscript") or self._ignore_depth > 0
        if tag in ("script","style","template","noscript"): self._ignore_depth += 1
        parent_hidden = any(n.get("hidden", False) for n in self.stack)
        own_hidden = (
            "hidden" in a or
            a.get("aria-hidden", "").lower() == "true" or
            bool(HIDDEN_STYLE.search(a.get("style", "")))
        )
        node = {
            "tag":tag,
            "attrs":a,
            "text":[],
            "ignored":ignored,
            "ru_switch":is_ru_switch(a),
            "hidden":parent_hidden or own_hidden or ignored,
            "in_header":tag == "header" or any(n.get("in_header", False) for n in self.stack),
            "in_footer":tag == "footer" or any(n.get("in_footer", False) for n in self.stack),
        }
        self.stack.append(node)

        if self.html_lang.lower().startswith("en") and not ignored and not node["ru_switch"]:
            for attr_name in ("aria-label","title","placeholder","alt"):
                value = clean(a.get(attr_name,""))
                if value and CYR.search(value):
                    self.en_cyrillic_attrs.append(f"{tag}[{attr_name}]={value[:100]}")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if not self.stack or self._ignore_depth: return
        text = clean(data)
        if not text: return
        self.visible_chunks.append(text)
        for node in self.stack:
            node["text"].append(text)
        if self.html_lang.lower().startswith("en"):
            intentional = any(n["ru_switch"] for n in self.stack)
            if not intentional and CYR.search(text):
                self.en_cyrillic.append(text[:140])

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("script","style","template","noscript") and self._ignore_depth:
            self._ignore_depth -= 1
        idx = None
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]["tag"] == tag:
                idx = i; break
        if idx is None: return
        node = self.stack[idx]
        text = clean(" ".join(node["text"]))
        a = node["attrs"]
        if tag == "button":
            self.buttons.append({"text":text,"aria":clean(a.get("aria-label","")),"title":clean(a.get("title","")),"type":a.get("type","")})
        elif tag == "a":
            self.links.append({
                "text":text,
                "aria":clean(a.get("aria-label","")),
                "title":clean(a.get("title","")),
                "href":a.get("href",""),
                "target":a.get("target",""),
                "rel":a.get("rel",""),
                "hidden":bool(node.get("hidden")),
                "in_header":bool(node.get("in_header")),
                "in_footer":bool(node.get("in_footer")),
            })
        del self.stack[idx:]


pages: dict[str, tuple[Path, AuditParser, str]] = {}
for page in sorted(root.rglob("*.html")):
    html = page.read_text(encoding="utf-8", errors="ignore")
    if "</head>" not in html or page.name.startswith(("google","yandex_")): continue
    rt = route(page)
    p = AuditParser(); p.feed(html)
    pages[rt] = (page, p, html)

routes = set(pages)
routes.add("/404.html")

hard = defaultdict(list)
quality = defaultdict(list)


def add(bucket, kind, rt, detail):
    bucket[kind].append((rt, str(detail)[:180]))


def canonical_expected(rt: str) -> str:
    if rt == "/": return "https://alexgtup.github.io/"
    return "https://alexgtup.github.io" + rt


def local_target_exists(href: str) -> bool:
    if not href or href.startswith(("#","mailto:","tel:","javascript:","data:")): return True
    u = urlsplit(href)
    if u.scheme or u.netloc: return True
    path = u.path or "/"
    if path.startswith("/assets/") or path.startswith("/favicon") or path in ("/site.webmanifest","/feed.xml","/sitemap.xml","/robots.txt"): return True
    if path.endswith(('.png','.jpg','.jpeg','.webp','.svg','.ico','.pdf','.xml','.txt','.json','.js','.css')): return True
    if not path.startswith("/"): return True
    norm = path if path.endswith("/") or path.endswith(".html") else path + "/"
    return norm in routes or path in routes


for rt, (page, p, html) in pages.items():
    if rt != "/404.html":
        if p.main_count != 1: add(hard,"main-count",rt,p.main_count)
        if p.h1_count != 1: add(quality,"h1-count",rt,p.h1_count)
        if p.title_count != 1: add(quality,"title-count",rt,p.title_count)
        if p.header_count != 1: add(quality,"header-count",rt,p.header_count)
        if p.footer_count != 1: add(quality,"footer-count",rt,p.footer_count)

    dup_ids = sorted({x for x,c in Counter(p.ids).items() if c > 1})
    for x in dup_ids[:20]: add(hard,"duplicate-id",rt,x)
    missing_fragments = sorted({f for f in p.href_fragments if f not in set(p.ids)})
    for f in missing_fragments[:20]: add(hard,"broken-fragment",rt,"#"+f)
    for target in p.skip_links:
        if target not in set(p.ids): add(hard,"broken-skip-link",rt,"#"+target)
    for b in p.buttons:
        if not (b["text"] or b["aria"] or b["title"]): add(hard,"unnamed-button",rt,b["type"] or "button")
    for a in p.links:
        href = a["href"]
        if href and not (a["text"] or a["aria"] or a["title"]): add(hard,"unnamed-link",rt,href)
        if href in ("", "#"): add(quality,"empty-link",rt,href or "<empty>")
        if not local_target_exists(href): add(quality,"broken-internal-link",rt,href)
        if a["target"].lower() == "_blank" and "noopener" not in a["rel"].lower(): add(quality,"blank-without-noopener",rt,href)
    if p.iframes_without_title: add(hard,"iframe-without-title",rt,p.iframes_without_title)
    if p.inputs_without_name: add(hard,"form-control-without-name",rt,p.inputs_without_name)

    if p.html_lang.lower().startswith("en"):
        for text in dict.fromkeys(p.en_cyrillic): add(hard,"en-visible-cyrillic",rt,text)
        for text in dict.fromkeys(p.en_cyrillic_attrs): add(hard,"en-attribute-cyrillic",rt,text)

    # A standalone 404 page intentionally has no canonical. Auditing it as a
    # canonical failure hid real metadata regressions in the report.
    if rt != "/404.html":
        if len(p.canonical) != 1:
            add(quality,"canonical-count",rt,len(p.canonical))
        elif p.canonical[0].rstrip('/') != canonical_expected(rt).rstrip('/'):
            add(quality,"canonical-mismatch",rt,p.canonical[0])

    for key, values in (("meta-description", [x for x in p.meta_names if x == "description"]),
                        ("meta-author", [x for x in p.meta_names if x == "author"]),
                        ("og-image", [x for x in p.meta_props if x == "og:image"]),
                        ("og-title", [x for x in p.meta_props if x == "og:title"])):
        if len(values) > 1: add(quality,"duplicate-"+key,rt,len(values))

    for href,c in Counter(p.stylesheets).items():
        if c > 1: add(quality,"duplicate-stylesheet",rt,f"{c}x {href}")
    for src,c in Counter(p.scripts).items():
        if c > 1: add(quality,"duplicate-script",rt,f"{c}x {src}")

    for img in p.images:
        if "alt" not in img: add(quality,"image-without-alt",rt,img.get("src","")[:120])

    text = clean(" ".join(p.visible_chunks))
    for m in SUSPICIOUS.finditer(text): add(quality,"placeholder-copy",rt,m.group(0))

    hrefs = [a["href"] for a in p.links]
    if rt not in ("/privacy/","/en/privacy/","/404.html") and not any(h in ("/privacy/","/en/privacy/") for h in hrefs):
        add(quality,"missing-privacy-link",rt,"no privacy link")

    # Count only visible content CTAs. Responsive desktop/mobile header variants,
    # noscript fallbacks and hidden retry links are not simultaneous conversion noise.
    tg = [
        a for a in p.links
        if "t.me/Alexuys" in a["href"]
        and not a.get("hidden")
        and not a.get("in_header")
        and not a.get("in_footer")
    ]
    if len(tg) >= 5: add(quality,"telegram-overload",rt,len(tg))

print(f"stage36 full final-site audit: {len(pages)} HTML pages")

hard_order = (
    "en-visible-cyrillic","en-attribute-cyrillic","main-count","broken-skip-link",
    "duplicate-id","broken-fragment","unnamed-button","unnamed-link",
    "iframe-without-title","form-control-without-name"
)
quality_order = (
    "h1-count","title-count","header-count","footer-count","canonical-count","canonical-mismatch",
    "duplicate-meta-description","duplicate-meta-author","duplicate-og-image","duplicate-og-title",
    "duplicate-stylesheet","duplicate-script","empty-link","broken-internal-link","blank-without-noopener",
    "image-without-alt","placeholder-copy","missing-privacy-link","telegram-overload"
)

print("HARD INVARIANTS")
for kind in hard_order:
    rows = hard.get(kind, [])
    print(f"  {kind}: {len(rows)}")
    for rt, detail in rows[:60]: print(f"    {rt} :: {detail}")

print("QUALITY LAPSES (report-only for this audit pass)")
quality_total = 0
for kind in quality_order:
    rows = quality.get(kind, [])
    quality_total += len(rows)
    print(f"  {kind}: {len(rows)}")
    for rt, detail in rows[:80]: print(f"    {rt} :: {detail}")
print(f"stage36 quality-lapse total: {quality_total}")

hard_total = sum(len(hard.get(kind, [])) for kind in hard_order)
if hard_total:
    raise SystemExit(f"stage36: {hard_total} language/accessibility regression(s)")
print("stage36 hard invariants OK")
