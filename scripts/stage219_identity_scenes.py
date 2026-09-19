#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
STYLE=r'''<style id="stage219-identity-scenes">
/* Stage219 — identity scenes for the two text-led entry screens. */
body[data-stage219-scene]{--s219-accent:#c9ff4a;--s219-line:rgba(255,255,255,.10);--s219-panel:#0d1115}
body[data-stage219-scene="about"]{--s219-accent:#ff8f73}
body[data-stage219-scene="cost-guide"]{--s219-accent:#9fb0ff}

/* ABOUT / operating system */
body[data-stage219-scene="about"] .p130-hero-side.p219-profile{max-width:470px!important;padding:0!important;overflow:hidden!important;border-radius:28px!important;background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.018)),#0b0f13!important}
.p219-profile__head{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:20px 22px 17px;border-bottom:1px solid var(--s219-line)}
.p219-profile__head small,.p219-profile__status{font:750 9px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase}
.p219-profile__head small{color:#87929a}.p219-profile__status{display:flex;align-items:center;gap:7px;color:#b9c1c6}.p219-profile__status i{width:7px;height:7px;border-radius:50%;background:var(--s219-accent);box-shadow:0 0 16px color-mix(in srgb,var(--s219-accent) 65%,transparent)}
.p219-profile__core{position:relative;padding:28px 22px 22px}
.p219-profile__core::before{content:"";position:absolute;inset:0;background:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:28px 28px;mask-image:linear-gradient(#000,transparent 95%);-webkit-mask-image:linear-gradient(#000,transparent 95%);pointer-events:none}
.p219-profile__axis{position:relative;z-index:1;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.p219-profile__node{position:relative;min-width:0;padding:15px 10px 13px;border:1px solid rgba(255,255,255,.09);border-radius:14px;background:#10151a}
.p219-profile__node b{display:block;margin-bottom:7px;color:var(--s219-accent);font:800 9px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em}
.p219-profile__node strong{display:block;color:#f3f5f2;font-size:12px;line-height:1.18}.p219-profile__node span{display:block;margin-top:5px;color:#7f8b93;font-size:10px;line-height:1.3}
.p219-profile__rail{position:relative;z-index:1;display:flex;align-items:center;gap:8px;margin:24px 0 16px;color:#79858d;font:700 8px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase}.p219-profile__rail::before,.p219-profile__rail::after{content:"";height:1px;flex:1;background:linear-gradient(90deg,transparent,var(--s219-line))}.p219-profile__rail::after{background:linear-gradient(90deg,var(--s219-line),transparent)}
.p219-profile__proof{position:relative;z-index:1;display:grid;grid-template-columns:1.12fr .88fr;gap:9px}.p219-profile__proof>div{padding:14px;border:1px solid rgba(255,255,255,.08);border-radius:13px;background:rgba(255,255,255,.025)}.p219-profile__proof small{display:block;margin-bottom:5px;color:#78848c;font:700 8px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.1em;text-transform:uppercase}.p219-profile__proof strong{display:block;color:#dfe4e1;font-size:12px;line-height:1.25}
.p219-profile__foot{padding:15px 22px 17px;border-top:1px solid var(--s219-line);color:#8e989f;font-size:11px;line-height:1.5}.p219-profile__foot b{color:#dfe4e1}

/* COST GUIDE / decision map */
body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero{display:grid!important;grid-template-columns:minmax(0,1.08fr) minmax(320px,.62fr)!important;grid-template-rows:auto auto auto auto!important;column-gap:clamp(44px,5vw,78px)!important;align-items:start!important;width:min(1420px,calc(100% - 64px))!important;max-width:1420px!important;padding-top:clamp(58px,6.5vw,100px)!important}
body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>.kicker,body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>h1,body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>.lead,body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>.meta{grid-column:1!important}
body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>.kicker{grid-row:1}body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>h1{grid-row:2}body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>.lead{grid-row:3}body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>.meta{grid-row:4}
.p219-costmap{grid-column:2;grid-row:1/5;position:relative;align-self:center;min-height:430px;padding:20px;border:1px solid rgba(255,255,255,.105);border-radius:26px;background:linear-gradient(145deg,rgba(255,255,255,.05),rgba(255,255,255,.015)),#0a0e12;box-shadow:0 30px 90px rgba(0,0,0,.25);overflow:hidden}
.p219-costmap::before{content:"";position:absolute;inset:0;background:linear-gradient(rgba(255,255,255,.026) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.026) 1px,transparent 1px);background-size:30px 30px;mask-image:linear-gradient(#000,transparent 92%);-webkit-mask-image:linear-gradient(#000,transparent 92%);pointer-events:none}
.p219-costmap__top{position:relative;z-index:1;display:flex;align-items:center;justify-content:space-between;gap:12px;padding-bottom:16px;border-bottom:1px solid var(--s219-line)}.p219-costmap__top small,.p219-costmap__top span{font:750 9px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.13em;text-transform:uppercase}.p219-costmap__top small{color:#859099}.p219-costmap__top span{color:var(--s219-accent)}
.p219-costmap__formula{position:relative;z-index:1;margin:25px 0 20px;color:#f4f5f2;font-size:clamp(24px,2vw,34px);font-weight:760;line-height:1.02;letter-spacing:-.045em}.p219-costmap__formula em{display:block;margin-top:7px;color:#8f9aa2;font:650 10px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em;font-style:normal;text-transform:uppercase}
.p219-costmap__paths{position:relative;z-index:1;display:grid;gap:8px}.p219-costmap__path{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:10px;align-items:center;padding:12px 11px;border:1px solid rgba(255,255,255,.08);border-radius:13px;background:#10151a}.p219-costmap__path>b{display:grid;place-items:center;width:30px;height:30px;border-radius:9px;background:color-mix(in srgb,var(--s219-accent) 10%,#10151a);color:var(--s219-accent);font:800 9px/1 ui-monospace,SFMono-Regular,Menlo,monospace}.p219-costmap__path strong{display:block;color:#eef1ee;font-size:12px}.p219-costmap__path span{display:block;margin-top:3px;color:#7f8a92;font-size:10px}.p219-costmap__path>i{color:#717d85;font:700 8px/1 ui-monospace,SFMono-Regular,Menlo,monospace;font-style:normal;letter-spacing:.08em;text-transform:uppercase}
.p219-costmap__bottom{position:relative;z-index:1;margin-top:18px;padding-top:15px;border-top:1px solid var(--s219-line);color:#849098;font-size:11px;line-height:1.5}.p219-costmap__bottom b{color:#dce2df}

@media(max-width:980px){
 body[data-stage219-scene="about"] .p130-hero-side.p219-profile{max-width:720px!important;width:100%!important}
 body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero{grid-template-columns:1fr!important;width:min(100% - 28px,860px)!important;row-gap:0!important}
 body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero>*{grid-column:1!important}.p219-costmap{grid-column:1!important;grid-row:auto!important;margin-top:34px;min-height:0}
}
@media(max-width:600px){
 body[data-stage219-scene="about"] .p130-hero-grid{gap:30px!important}.p219-profile__head{padding:15px 16px 13px}.p219-profile__core{padding:20px 16px 16px}.p219-profile__axis{grid-template-columns:repeat(2,minmax(0,1fr))}.p219-profile__proof{grid-template-columns:1fr}.p219-profile__foot{padding:13px 16px 15px}.p219-profile__node{padding:13px 11px}
 body[data-stage219-scene="cost-guide"] .ux-guide-main>.hero{width:calc(100% - 24px)!important;padding-top:42px!important}.p219-costmap{margin-top:26px;padding:16px;border-radius:20px}.p219-costmap__formula{font-size:26px}.p219-costmap__path{grid-template-columns:32px minmax(0,1fr)}.p219-costmap__path>i{grid-column:2}.p219-costmap__top{align-items:flex-start;flex-direction:column}
}
@media(prefers-reduced-motion:reduce){.p219-profile__status i{box-shadow:none}}
</style>'''
ABOUT='''<aside class="p130-hero-side p219-profile" aria-label="Рабочий контур Александра"><div class="p219-profile__head"><small>WORK MODE / SYSTEM</small><span class="p219-profile__status"><i></i>full context</span></div><div class="p219-profile__core"><div class="p219-profile__axis"><div class="p219-profile__node"><b>01</b><strong>Разобрать</strong><span>цель / код</span></div><div class="p219-profile__node"><b>02</b><strong>Собрать</strong><span>logic / UI</span></div><div class="p219-profile__node"><b>03</b><strong>Проверить</strong><span>mobile / flow</span></div><div class="p219-profile__node"><b>04</b><strong>Выпустить</strong><span>release / fix</span></div></div><div class="p219-profile__rail">one project context</div><div class="p219-profile__proof"><div><small>PROJECT TYPES</small><strong>Web · WordPress · Telegram · Automation</strong></div><div><small>PUBLIC PROOF</small><strong>Кейсы + Freelance.ru</strong></div></div></div><div class="p219-profile__foot"><b>Без передачи между ролями:</b> контекст задачи остаётся у одного разработчика от разбора до релиза.</div></aside>'''
COST='''<aside class="p219-costmap" aria-label="Карта факторов стоимости разработки"><div class="p219-costmap__top"><small>ESTIMATE MAP / 2026</small><span>scope → estimate</span></div><div class="p219-costmap__formula">Стоимость = состав сценария<em>не название технологии</em></div><div class="p219-costmap__paths"><div class="p219-costmap__path"><b>01</b><div><strong>Интерфейс</strong><span>экраны и состояния</span></div><i>UI</i></div><div class="p219-costmap__path"><b>02</b><div><strong>Backend</strong><span>правила и роли</span></div><i>logic</i></div><div class="p219-costmap__path"><b>03</b><div><strong>Данные</strong><span>структура и хранение</span></div><i>data</i></div><div class="p219-costmap__path"><b>04</b><div><strong>Интеграции</strong><span>API и внешние системы</span></div><i>links</i></div></div><div class="p219-costmap__bottom"><b>Оценка становится точнее,</b> когда эти четыре слоя можно описать конкретными пользовательскими сценариями.</div></aside>'''

def patch(path,scene,replacer):
 p=ROOT/path
 if not p.is_file():raise SystemExit(f'stage219 missing {path}')
 s=p.read_text(encoding='utf8')
 s=re.sub(r'\s*<style\b[^>]*id="stage219-identity-scenes"[^>]*>.*?</style>','',s,flags=re.I|re.S)
 s=re.sub(r'\sdata-stage219-scene="[^"]+"','',s,count=1)
 s=re.sub(r'\s*<aside class="p219-costmap".*?</aside>','',s,flags=re.I|re.S)
 if path=='about/index.html':
  s=re.sub(r'<aside class="p130-hero-side(?: p219-profile)?".*?</aside>',ABOUT,s,count=1,flags=re.S)
 else:
  marker='</section><div class="container layout">'
  if marker not in s:raise SystemExit('stage219 guide hero marker missing')
  s=s.replace(marker,COST+'</section><div class="container layout">',1)
 s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+f' data-stage219-scene="{scene}">',s,count=1,flags=re.I)
 if n!=1:raise SystemExit(f'stage219 body missing {path}')
 s=s.replace('</head>',STYLE+'</head>',1)
 p.write_text(s,encoding='utf8')

patch('about/index.html','about',ABOUT)
patch('guides/development-cost/index.html','cost-guide',COST)
for path,scene,needle in [('about/index.html','about','p219-profile__axis'),('guides/development-cost/index.html','cost-guide','p219-costmap__paths')]:
 s=(ROOT/path).read_text(encoding='utf8')
 if s.count('id="stage219-identity-scenes"')!=1 or len(re.findall(r'<body\b[^>]*data-stage219-scene="'+re.escape(scene)+r'"',s,re.I))!=1 or needle not in s:
  raise SystemExit(f'stage219 guard {path}')
print('stage219 identity scenes: about=work-system, development-cost=estimate-map')
