#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
PRIORITY={'/telegram-bots/':8,'/wordpress-development/':8,'/n8n-automation/':8}
STOP=set('и в на для с под от до без по или из это как что не alexuys заказать заказ разработка сайта сайтов'.split())
EXCLUDE_PREFIX=('/en/',)
EXCLUDE={'/privacy/'}

class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title='';self.h1=[];self.desc='';self.robots='';self.lang='';self.links=[];self._mode=None;self._buf=''
    def handle_starttag(self,t,attrs):
        a=dict(attrs); t=t.lower()
        if t=='html': self.lang=a.get('lang','')
        elif t=='title': self._mode='title';self._buf=''
        elif t=='h1': self._mode='h1';self._buf=''
        elif t=='meta' and a.get('name','').lower()=='description': self.desc=a.get('content','').strip()
        elif t=='meta' and a.get('name','').lower()=='robots': self.robots=a.get('content','')
        elif t=='a':
            h=a.get('href','').split('#')[0].split('?')[0]
            if h.startswith('/') and not h.startswith('//'):self.links.append(h)
    def handle_endtag(self,t):
        if t=='title' and self._mode=='title':self.title=' '.join(self._buf.split());self._mode=None
        elif t=='h1' and self._mode=='h1':self.h1.append(' '.join(self._buf.split()));self._mode=None
    def handle_data(self,d):
        if self._mode:self._buf+=d+' '

def route(path:Path)->str:
    return '/' if path==ROOT/'index.html' else '/'+str(path.parent.relative_to(ROOT)).replace('\\','/')+'/'
def tokens(s:str)->set[str]:
    return {x for x in re.findall(r'[a-zа-яё0-9]+',s.lower()) if len(x)>2 and x not in STOP}

pages={}
for p in ROOT.rglob('index.html'):
    r=route(p); d=Doc(); d.feed(p.read_text(encoding='utf-8',errors='ignore')); pages[r]=d

ru={r:d for r,d in pages.items() if not r.startswith(EXCLUDE_PREFIX) and d.lang.lower().startswith('ru') and 'noindex' not in d.robots.lower() and r not in EXCLUDE}
issues=[]
for r,d in ru.items():
    if not 35<=len(d.title)<=65: issues.append(f'title-length {r}: {len(d.title)} :: {d.title}')
    if not 90<=len(d.desc)<=180: issues.append(f'description-length {r}: {len(d.desc)}')
    if len(d.h1)!=1: issues.append(f'h1-count {r}: {len(d.h1)}')

# Detect money-page intent collisions from title + H1, excluding hubs/cases/guides/tools.
commercial=[]
for r,d in ru.items():
    if r=='/' or r.startswith(('/cases/','/guides/','/tools/')) or r in {'/about/','/services/','/demos/','/freelance-os/'}:continue
    commercial.append((r,tokens(d.title+' '+d.h1[0])))
collisions=[]
for i,a in enumerate(commercial):
    for b in commercial[i+1:]:
        union=a[1]|b[1]
        sim=len(a[1]&b[1])/len(union) if union else 0
        if sim>=.55: collisions.append((sim,a[0],b[0],sorted(a[1]&b[1])))
for sim,a,b,shared in collisions:
    issues.append(f'intent-collision {sim:.2f} {a} <-> {b}: {",".join(shared)}')

# Priority cluster must be reachable from home and supported by contextual internal links.
home=pages.get('/')
if not home: issues.append('homepage missing')
inbound=Counter()
for src,d in pages.items():
    for h in set(d.links):
        if h in pages: inbound[h]+=1
for target,min_inbound in PRIORITY.items():
    if target not in pages: issues.append(f'priority page missing: {target}');continue
    if not home or target not in home.links: issues.append(f'priority page not linked from home: {target}')
    if inbound[target] < min_inbound: issues.append(f'priority inbound too low: {target}={inbound[target]} < {min_inbound}')
    d=pages[target]
    supporting=sum(1 for h in d.links if h.startswith('/cases/') or h.startswith('/guides/'))
    if supporting<3: issues.append(f'priority support links too low: {target}={supporting}')

if issues:
    raise SystemExit('stage208 search intent guard failed:\n'+'\n'.join(' - '+x for x in issues))
print(f'stage208 search intent guard: ru_indexable={len(ru)}, commercial={len(commercial)}, collisions=0, priority='+', '.join(f'{k}:{inbound[k]}' for k in PRIORITY))
