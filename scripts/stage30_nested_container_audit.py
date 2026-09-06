#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

class ContainerAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.nested = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        is_container = "container" in classes
        active = [x for x in self.stack if x[1]]
        if is_container and active:
            parent_tag, _, parent_classes = active[-1]
            self.nested.append((parent_tag, " ".join(parent_classes), tag, " ".join(classes)))
        self.stack.append((tag, is_container, classes))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        # HTML in the project is regular enough, but pop defensively to the
        # matching tag so malformed optional tags do not poison the audit.
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

issues = []
for path in sorted(root.rglob("*.html")):
    html = path.read_text(encoding="utf-8", errors="ignore")
    if "</head>" not in html or path.name.startswith(("google", "yandex_")):
        continue
    parser = ContainerAudit()
    parser.feed(html)
    if parser.nested:
        issues.append((path.relative_to(root).as_posix(), parser.nested))

print(f"stage30 nested container audit: {len(issues)} pages with nested .container")
for rel, nested in issues:
    print(f"  {rel}")
    for parent_tag, parent_cls, child_tag, child_cls in nested[:12]:
        print(f"    {parent_tag}.{parent_cls} -> {child_tag}.{child_cls}")
