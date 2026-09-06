#!/usr/bin/env python3
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from collections import defaultdict
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
CYR = re.compile(r"[А-Яа-яЁё]")
SPACE = re.compile(r"\s+")


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
        self.iframes_without_title = 0
        self.inputs_without_name = 0
        self.main_count = 0
        self.skip_links: list[str] = []
        self._ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower(); a = {k.lower(): (v or "") for k,v in attrs}
        if tag == "html": self.html_lang = a.get("lang", "")
        if a.get("id"): self.ids.append(a["id"])
        if tag == "main": self.main_count += 1
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
        node = {"tag":tag,"attrs":a,"text":[],"ignored":ignored,"ru_switch":is_ru_switch(a)}
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
            self.links.append({"text":text,"aria":clean(a.get("aria-label","")),"title":clean(a.get("title","")),"href":a.get("href","")})
        del self.stack[idx:]


issues = defaultdict(list)
for page in sorted(root.rglob("*.html")):
    html = page.read_text(encoding="utf-8", errors="ignore")
    if "</head>" not in html or page.name.startswith(("google","yandex_")): continue
    rt = route(page)
    p = AuditParser(); p.feed(html)

    dup_ids = sorted({x for x in p.ids if p.ids.count(x) > 1})
    for x in dup_ids[:10]: issues["duplicate-id"].append((rt,x))
    missing_fragments = sorted({f for f in p.href_fragments if f not in set(p.ids)})
    for f in missing_fragments[:10]: issues["broken-fragment"].append((rt,"#"+f))

    if rt not in ("/404",) and p.main_count != 1:
        issues["main-count"].append((rt,str(p.main_count)))
    for target in p.skip_links:
        if target not in set(p.ids): issues["broken-skip-link"].append((rt,"#"+target))
    for b in p.buttons:
        if not (b["text"] or b["aria"] or b["title"]): issues["unnamed-button"].append((rt,b["type"] or "button"))
    for a in p.links:
        if a["href"] and not (a["text"] or a["aria"] or a["title"]): issues["unnamed-link"].append((rt,a["href"][:100]))
    if p.iframes_without_title: issues["iframe-without-title"].append((rt,str(p.iframes_without_title)))
    if p.inputs_without_name: issues["form-control-without-name"].append((rt,str(p.inputs_without_name)))

    if p.html_lang.lower().startswith("en"):
        for text in dict.fromkeys(p.en_cyrillic): issues["en-visible-cyrillic"].append((rt,text))
        for text in dict.fromkeys(p.en_cyrillic_attrs): issues["en-attribute-cyrillic"].append((rt,text))

print("stage36 language + accessibility audit")
order = (
    "en-visible-cyrillic","en-attribute-cyrillic","main-count","broken-skip-link",
    "duplicate-id","broken-fragment","unnamed-button","unnamed-link",
    "iframe-without-title","form-control-without-name"
)
for kind in order:
    rows = issues.get(kind, [])
    print(f"  {kind}: {len(rows)}")
    for rt, detail in rows[:40]: print(f"    {rt} :: {detail}")

total = sum(len(issues.get(kind, [])) for kind in order)
if total:
    raise SystemExit(f"stage36: {total} language/accessibility regression(s)")
print("stage36 language/accessibility invariant OK")
