#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import gzip,hashlib,re,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
TARGETS=(
 'universal-media.css','site-enhancements.css','stage105-layout-core.css',
 'stage94-site-ux.css','stage105-theme-search.css','growth.css','ux-pass.css',
 'portfolio-showcase.css','stage105-final-ui.css','stage213-impossible-polish.css','stage214-case-exhibition.css','stage215-service-scenes.css','stage217-flagship-cases.css','stage221-services-system.css','stage222-reputation-ledger.css','stage223-decision-library.css',
)

def minify_css(s:str)->str:
    out=[];i=0;n=len(s);quote=None;pending_space=False
    while i<n:
        c=s[i]
        if quote:
            out.append(c)
            if c=='\\' and i+1<n:
                out.append(s[i+1]);i+=2;continue
            if c==quote: quote=None
            i+=1;continue
        if c in ('"',"'"):
            if pending_space and out and out[-1] not in '{:;,}': out.append(' ')
            pending_space=False;quote=c;out.append(c);i+=1;continue
        if c=='/' and i+1<n and s[i+1]=='*':
            j=s.find('*/',i+2)
            if j<0: raise SystemExit('stage209 unterminated CSS comment')
            i=j+2;pending_space=True;continue
        if c.isspace():
            pending_space=True;i+=1;continue
        if c in '{};,':
            while out and out[-1]==' ': out.pop()
            if c=='}' and out and out[-1]==';': out.pop()
            out.append(c);pending_space=False;i+=1;continue
        if pending_space:
            if out and out[-1] not in '{:;,}': out.append(' ')
            pending_space=False
        out.append(c);i+=1
    if quote: raise SystemExit('stage209 unterminated CSS string')
    return ''.join(out).strip()

# Regression guard: whitespace before a pseudo-class can be a descendant combinator.
# `.a :is(...)` and `.a:is(...)` are different selectors and must never collapse.
_MINIFIER_PROBE=minify_css('.a :is(.b,.c) { color: red; } .x:hover { opacity: 1; }')
if '.a :is(' not in _MINIFIER_PROBE or '.a:is(' in _MINIFIER_PROBE or '.x:hover' not in _MINIFIER_PROBE:
    raise SystemExit(f'stage209 selector whitespace regression: {_MINIFIER_PROBE}')

def syntax_guard(s:str,name:str):
    depth=0;quote=None;i=0
    while i<len(s):
        c=s[i]
        if quote:
            if c=='\\' and i+1<len(s): i+=2;continue
            if c==quote:quote=None
        elif c in ('"',"'"):quote=c
        elif c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth<0:raise SystemExit(f'stage209 negative brace depth: {name}')
        i+=1
    if quote or depth!=0:raise SystemExit(f'stage209 syntax guard failed {name}: quote={bool(quote)} depth={depth}')

assets=ROOT/'assets'; stats=[]; hashes={}
for name in TARGETS:
    p=assets/name
    if not p.is_file(): raise SystemExit(f'stage209 missing CSS: {name}')
    src=p.read_text(encoding='utf-8'); before=len(src.encode()); before_gz=len(gzip.compress(src.encode(),9))
    dst=minify_css(src); syntax_guard(dst,name)
    p.write_text(dst,encoding='utf-8')
    after=len(dst.encode()); after_gz=len(gzip.compress(dst.encode(),9))
    if after>before: raise SystemExit(f'stage209 CSS expanded unexpectedly: {name}')
    digest=hashlib.sha256(dst.encode()).hexdigest()[:12];hashes[name]=digest
    stats.append((name,before,after,before_gz,after_gz))

# Rotate every HTML cache key for files whose bytes changed.
refs=0
for p in ROOT.rglob('*.html'):
    s=p.read_text(encoding='utf-8',errors='ignore'); original=s
    for name,digest in hashes.items():
        pat=rf'(/assets/{re.escape(name)})(?:\?v=[^"\']+)?'
        s,n=re.subn(pat,rf'\1?v={digest}',s)
        refs+=n
    if s!=original:p.write_text(s,encoding='utf-8')

# Every optimized asset must retain at least one hashed reference wherever it is scoped.
# Global bundles happen to be on the homepage; page-specific visual layers are intentionally not.
for name,digest in hashes.items():
    hashed=f'/assets/{name}?v={digest}'
    total=0
    stale=0
    for hp in ROOT.rglob('*.html'):
        hs=hp.read_text(encoding='utf-8',errors='ignore')
        total += hs.count(hashed)
        stale += len(re.findall(rf'/assets/{re.escape(name)}(?!\?v=)',hs))
    if total<1:
        raise SystemExit(f'stage209 cache ref missing: {name}')
    if stale:
        raise SystemExit(f'stage209 unhashed cache ref remains: {name}={stale}')
raw_before=sum(x[1] for x in stats); raw_after=sum(x[2] for x in stats)
gz_before=sum(x[3] for x in stats); gz_after=sum(x[4] for x in stats)
saving=gz_before-gz_after
mode='fresh' if saving>=15000 else 'repeat/minimal'
print(f'stage209 CSS delivery: files={len(stats)}, html_refs={refs}, raw={raw_before}->{raw_after} (-{raw_before-raw_after}), gzip={gz_before}->{gz_after} (-{saving}), mode={mode}')
