#!/usr/bin/env python3
"""Build every page as ordinary HTML; no client framework or API is required."""
from pathlib import Path

def write_utf8(path, text):
 return path.write_text(text, encoding="utf-8", newline="\n")

from html import escape as esc
from importlib.util import spec_from_file_location,module_from_spec
import json,shutil,hashlib,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'site';OUT.mkdir(exist_ok=True)
spec=spec_from_file_location('mf_content',ROOT/'content/site.py');module=module_from_spec(spec);spec.loader.exec_module(module)
SITE,PAGES,PROJECTS,SOURCES,TIMELINE=module.SITE,module.PAGES,module.PROJECTS,module.SOURCES,module.TIMELINE
DOCS=json.loads((ROOT/'content/documents.json').read_text(encoding='utf-8'));ASSETS=json.loads((ROOT/'content/assets.json').read_text(encoding='utf-8'))
LOCAL_ASSETS=json.loads((ROOT/'content/local-assets.json').read_text(encoding='utf-8'))
ASSETS.update({key:['local',data['file'],data['alt']] for key,data in LOCAL_ASSETS.items()})
BYID={x['id']:x for x in PROJECTS+SOURCES+DOCS};BYPAGE={x['slug']:x for x in PAGES}
def external(url): return url.startswith(('https://','http://'))
def link(url,label,cls='',download=False):
 extra=' target="_blank" rel="noopener noreferrer"' if external(url) else ''
 if download: extra+=' download'
 return f'<a href="{esc(url,quote=True)}"'+(f' class="{cls}"' if cls else '')+extra+f'>{label}</a>'
def para(text): return ''.join('<p>'+esc(p)+'</p>' for p in text.split('\n\n') if p)
def refs(ids):
 if not ids:return ''
 items=[]
 for rid in ids:
  target=f'library.html#{rid}' if rid.startswith('D') else f'sources.html#{rid}'
  items.append(link(target,f'{rid} · {esc(BYID[rid]["title"])}'))
 return '<details class="source-notes"><summary>Sources for this section</summary><p class="source-line">'+' '.join(items)+'</p></details>'
def title_plain(p): return re.sub('<[^>]+>',' ',p['title']).replace('  ',' ').strip()
def image(key): return 'assets/images/'+key+Path(ASSETS[key][1]).suffix.lower()

def case_study(kind):
 cases={
 'capital':('A worker-owned business: Real Pickles',
  'In 2013, Real Pickles in Massachusetts raised US$500,000 from 77 investors as part of its move to worker ownership. Its account describes a US$500,000 funding need. This is a useful case because it shows community investment supporting a handover while workers retained control.',
  'The starting target and amount raised are both US$500,000; 77 is the reported investor count. These are historical US dollars, with no currency conversion. This models the community campaign only. It does not reconstruct the entire purchase price, other finance or business cash flow.',
  [('Real Pickles: financing case study','https://realpickles.com/2013/11/real-pickles-financing-case-study/'),('Real Pickles: campaign record','https://realpickles.com/invest/')]),
 'workforce':('A funded break: Victoria’s teaching service',
  'Victoria’s published sabbatical scheme lets eligible staff work for one to four years at 80% of their salary, then take a period of leave funded by the salary set aside. It provides a concrete example of planning income and time together.',
  'The starting plan uses the four-year option: 48 months of work and 12 months of leave. At an unchanged salary, setting aside 20% for four years is equivalent to 80% of one year’s salary. The planner uses whole months as an approximate display of the 52-week option. This is a worked example of that scheme, not a named employee’s history or a general leave entitlement. Your employment terms and approval still matter.',
  [('Victorian teaching service: sabbatical leave','https://www2.education.vic.gov.au/pal/sabbatical-leave-teaching-service/overview'),('Published flexible-work options','https://www2.education.vic.gov.au/pal/flexible-work/policy-and-guidelines/11-appendix-2-overview-key-flexible-work-options')]),
 'permissions':('Why sharing choices matter: the CarCover example',
  'The OAIC published a fictionalised case based on a reported data breach. An employee uploaded a customer’s hardship application, including health and family details, to a public AI service despite a workplace policy against it. The example shows why purpose, sharing and training choices need to be understood before use.',
  'The draft starts with local use only, no training permission, no external sharing permission and a limited purpose and period. These are this site’s cautious starting choices in response to the case, not settings used by the company or a guarantee of compliance. The type of information remains undecided until you choose it. Saving this draft does not configure any AI service.',
  [('OAIC: GenAI tools in the workplace, 4 December 2025','https://www.oaic.gov.au/news/blog/GenAI-tools-in-the-workplace-balancing-protection-of-personal-information-and-business-efficiency')]),
 'dependencies':('Start with power: South Australia, 2016',
  'AEMO’s final report records about 850,000 customer connections losing electricity in South Australia on 28 September 2016. The report describes effects on households, businesses, transport, community services and industry.',
  'That documented event is why electricity is selected first. The nine services and their links below are a simplified teaching model chosen for this site. They are not outage measurements, probabilities or a claim that every linked service failed in 2016. Select a different interruption to compare paths. The model does not include backup systems or time to recovery.',
  [('AEMO: final report on the 2016 South Australian black system event','https://www.aemo.com.au/-/media/files/electricity/nem/market_notices_and_events/power_system_incident_reports/2017/integrated-final-report-sa-black-system-28-september-2016.pdf')])}
 title,story,reason,sources=cases[kind]
 h='<section class="section tint model-explanation" id="model"><div class="wrap"><h2>'+esc(title)+'</h2><div class="prose">'+para(story)+'<h3>Why the tool starts this way</h3>'+para(reason)+'</div><p class="source-line">'+''.join(link(url,label) for label,url in sources)+'</p></div></section>'
 if kind=='capital':
  h+='<section class="section"><div class="wrap"><h2>Explore the community funding campaign</h2><p class="measure">Change the three figures to see their relationship. Changes become your own scenario; the reset restores the historical figures. All amounts in this example are US dollars.</p><div class="tool"><form id="campaign-form"><div class="form-grid"><label>Funding target (US$)<input name="target" type="number" min="1" step="1" value="500000" required></label><label>Amount raised (US$)<input name="raised" type="number" min="0" step="1" value="500000" required></label><label>Number of investors<input name="investors" type="number" min="1" step="1" value="77" required></label></div></form><div class="result-grid" aria-live="polite"><div class="result"><span>Amount still needed</span><strong id="campaign-gap"></strong></div><div class="result"><span>Target funded</span><strong id="campaign-percent"></strong></div><div class="result"><span>Average per investor</span><strong id="campaign-average"></strong></div></div><p id="campaign-status" class="tool-status" role="status"></p><div class="actions"><button id="campaign-reset" class="button" type="button">Restore Real Pickles figures</button><button id="campaign-export" class="button" type="button">Download scenario</button></div></div></div></section>'
 return h

def tools(kind):
 if kind=='capital':
  def inp(name,label,value,minv=0,maxv=None,step=1000):
   return f'<label>{label}<input name="{name}" type="number" value="" min="{minv}"'+(f' max="{maxv}"' if maxv is not None else '')+f' step="{step}" placeholder="Enter your assumption" required></label>'
  result=lambda id,label:f'<div class="result"><span'+(' id="gap-label"' if id=='gap' else '')+f'>{label}</span><strong id="{id}-out" data-capital-result>Calculating</strong></div>'
  return '<section class="section" id="tool"><div class="wrap"><span class="tag demo">Interactive illustration</span><h2 style="margin-top:20px">Your purchase and upgrade calculator</h2><p class="measure muted">Build your own purchase and upgrade scenario in Australian dollars. Start with verified business records and quotes. Unknown figures are blank, not zero. Enter zero only where you have chosen to exclude a cost or funding source. Nothing is uploaded or automatically saved.</p><div class="tool"><form id="capital-form" onsubmit="return false"><fieldset><legend>What needs funding</legend><div class="form-grid">'+''.join([inp('price','Negotiated purchase price (A$)',1000000),inp('working','Working capital (A$)',150000),inp('upgrade','AI, robotics and systems upgrades (A$)',100000),inp('fees','Transaction expenses (A$)',50000)])+'</div></fieldset><fieldset><legend>Loans, contributions and payments due later</legend><div class="form-grid">'+''.join([inp('senior','Main business loan (A$)',500000),inp('seniorRate','Main loan interest (% per year)',8,0,40,.1),inp('seniorTerm','Main loan repayment term (years)',7,1,30,1),inp('vendor','Deferred seller price (A$)',300000),inp('vendorRate','Interest on deferred seller payment (% per year)',5,0,40,.1),inp('vendorTerm','Seller repayment term (years)',5,1,30,1),inp('equity','Outside investment (A$)',450000),inp('members','Member contributions (A$)',50000)])+'</div></fieldset><fieldset><legend>Annual cash and transition</legend><div class="form-grid">'+''.join([inp('cash','Cash before acquisition financing (A$/year)',280000),inp('transition','Added workforce budget (A$/year)',40000),inp('stress','Stress: reduction in annual cash (%)',25,0,100,1)])+'</div></fieldset></form><div class="result-grid" aria-live="polite">'+''.join([result('uses','Total funding needed'),result('gap','Funding difference'),result('debt','Estimated annual loan repayments'),result('base','Base cash after debt and workforce budget'),result('stress','Stressed cash after debt and workforce budget'),result('ratio','Reduced cash / loan repayments')])+'</div><p class="tool-status" id="capital-status" role="status"></p><div class="actions"><button class="button primary-button" id="capital-export" type="button">Download scenario .md</button><button class="button subtle" id="capital-reset" type="button">Clear your assumptions</button></div><p class="consent-note">Level annual repayments are used. Investor distributions, earn-outs, refinancing and tax changes are not forecast. A guarantee is not counted as funding. The ratio is a simple cash comparison, not a lender\'s eligibility test.</p></div></div></section>'
 if kind=='workforce':
  return '''<section class="section" id="tool"><div class="wrap"><span class="tag demo">Plan in your browser</span><h2 style="margin-top:20px">My next chapter</h2><p class="measure muted">Sketch preferences, not an approved employment arrangement. Save only when you choose, or download a Markdown copy to keep elsewhere.</p><div class="tool"><form id="life-planner" onsubmit="return false"><label>Plan title<input id="plan-title" maxlength="160" value="My next chapter"></label><fieldset><legend>Phases of work and life</legend><div id="phase-list"></div><button id="phase-add" class="button subtle" type="button">Add a phase</button></fieldset><div class="phase-strip" id="phase-strip" aria-label="Proposed cycle"></div><h3 id="cycle-total"></h3><p class="tool-intro" id="cycle-note"></p><label>What would make this possible?<textarea id="plan-notes" maxlength="5000" placeholder="Funding, care, qualifications, hosts, travel permissions, coverage and return arrangements..."></textarea></label></form><div class="actions"><button id="life-export" class="button primary-button" type="button">Download plan .md</button><button id="life-save" class="button" type="button">Save in this browser</button><button id="life-load" class="button" type="button">Load saved draft</button><button id="life-clear" class="button subtle" type="button">Remove saved copy</button><button id="life-reset" class="button subtle" type="button">Restore sourced example</button></div><p id="life-status" class="tool-status" role="status"></p><p class="consent-note">This tool has no account or remote storage. Browser storage is not encryption. A draft does not create a leave entitlement, employment contract, income guarantee or permission to undertake an activity overseas.</p></div></div></section>'''
 if kind=='permissions':
  opts=lambda name,label,values:'<label>'+label+f'<select name="{name}">'+''.join('<option>'+esc(v)+'</option>' for v in values)+'</select></label>'
  return '<section class="section" id="tool"><div class="wrap"><span class="tag demo">Draft your preferences</span><h2 style="margin-top:20px">My permissions, in plain language</h2><p class="measure muted">Choose how your information may be used without entering private records. Download a draft to discuss with a provider or workplace. It does not change their systems or enforce your choices.</p><div class="tool"><form id="permissions-form" onsubmit="return false"><div class="form-grid two"><label>Draft name<input name="profileName" maxlength="160" placeholder="A name for this draft"></label>'+opts('scope','Material covered',['Not yet decided','Personal preferences','Professional record','Household material','Collective material: authority still to be established'])+opts('inference','Use to answer questions',['Local use only, as authorised','Specific external service, by separate agreement','Not yet decided'])+opts('training','Use for model training',['Not authorised by this draft','Specific research only, separately agreed','Specific model only, separately agreed','Not yet decided'])+opts('offDevice','Sharing beyond your device',['No sharing authorised by this draft','Named recipients and purposes only','An agreed public subset only','Not yet decided'])+opts('retention','How long information may be kept',['For the agreed purpose and period only','Keep my own copy; external retention separately agreed','Not yet decided'])+'<label>Named recipients and purposes<textarea name="recipients" maxlength="3000" placeholder="Describe roles or purposes, without adding private contact details."></textarea></label><label>What should happen when permission changes?<textarea name="revoke" maxlength="3000" placeholder="Future use, access, retention and records each need an actual arrangement."></textarea></label><label class="full-width">Questions and implementation notes<textarea name="notes" maxlength="5000" placeholder="Legal obligations, cultural authority, trained-model effects and technical enforcement remain distinct questions."></textarea></label></div></form><div class="actions"><button id="permissions-export" class="button primary-button" type="button">Download draft .md</button><button id="permissions-json" class="button" type="button">Download draft .json</button><button id="permissions-save" class="button" type="button">Save in this browser</button><button id="permissions-load" class="button" type="button">Load saved draft</button><button id="permissions-clear" class="button subtle" type="button">Remove saved copy</button></div><p id="permissions-status" class="tool-status" role="status"></p><p class="consent-note">No personal data is sent to a model or server by this tool. Applicable retention requirements, collective authority and the limits of revocation need their own treatment in an actual implementation.</p></div></div></section>'
 if kind=='dependencies':
  return '''<section class="section" id="tool"><div class="wrap"><span class="tag demo">A simple example</span><h2 style="margin-top:20px">Service connections example</h2><p class="measure muted">Select an interruption and trace a small service network. A path in this graph is not a prediction of real-world failure.</p><div class="tool" id="dependency-tool"><h3>Which service is unavailable in this sketch?</h3><div id="dependency-inputs" class="check-grid"></div><div class="tag-row"><span class="tag source">Gold: selected interruption</span><span class="tag proposal">Violet: dependency path</span><span class="tag demo">Teal: no path traced</span></div><div id="dependency-grid" class="dependency-grid" aria-live="polite"></div><p id="dependency-status" class="tool-status" role="status"></p><label>Notes, substitutes and questions<textarea id="dependency-notes" maxlength="5000" placeholder="Which real assets, people, tested alternatives or uncertain assumptions would change this sketch?"></textarea></label><div class="actions"><button id="dependency-export" class="button primary-button" type="button">Download scenario .md</button><button id="dependency-reset" class="button subtle" type="button">Clear interruptions</button></div><p class="consent-note">The example treats each link as necessary. Real services may have backups, stored supplies or alternative providers. It does not calculate how likely an interruption is, how long it lasts or how serious it becomes. It is not an emergency assessment.</p></div></div></section>'''
 return ''
def section(s,n):
 h='<section class="section'+(' tint' if n%2 else '')+f'" id="section-{n}"><div class="wrap"><div class="section-head reveal"><div><h2>{s["title"]}</h2></div></div>'
 if s.get('text'):h+='<div class="prose measure reveal">'+para(s['text'])+'</div>'
 if s.get('statement'):h+='<p class="statement reveal">'+esc(s['statement'])+'</p>'
 if s.get('visual'):
  v=LOCAL_ASSETS[s['visual']]
  h+='<figure class="content-visual"><img loading="lazy" src="'+v['file']+'" alt="'+esc(v['alt'],quote=True)+'" width="1672" height="941"><figcaption>'+esc(v['caption'])+' AI-generated concept image.</figcaption></figure>'
 if s.get('cards'):
  cards=s['cards'];cl='four-col' if len(cards)==4 else 'three-col' if len(cards)%3==0 else 'two-col'
  h+=f'<div class="{cl}">'
  for i,c in enumerate(cards):
   inside=f'<h3>{esc(c["title"])}</h3><p>{esc(c["text"])}</p>'
   h+=link(c['href'],inside+'<span class="arrow" aria-hidden="true">↗</span>','card card-link reveal') if c.get('href') else '<article class="card reveal">'+inside+'</article>'
  h+='</div>'
 if s.get('flow'):h+='<div class="flow reveal">'+''.join('<span><strong>'+esc(a)+'</strong>'+esc(b)+'</span>' for a,b in s['flow'])+'</div>'
 if s.get('table'):
  t=s['table'];h+='<div class="table-scroll reveal"><table class="info-table"><thead><tr>'+''.join('<th scope="col">'+esc(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td data-label="'+esc(t['headers'][i],quote=True)+'">'+esc(x)+'</td>' for i,x in enumerate(row))+'</tr>' for row in t['rows'])+'</tbody></table></div>'
 if s.get('callout'):h+='<aside class="callout reveal">'+para(s['callout'])+'</aside>'
 h+=refs(s.get('refs',[]))+'</div></section>';return h

def guide(d):
 return f'''# {d['title']}: source reading guide\n\nSource ID: {d['id']}\nOriginal filename: {d['original_name']}\nType: {d['kind']}\nExtent: {d['pages']}\nSupplied: {d['supplied']}\nOriginal SHA-256: {d['sha256']}\n\n## Relationship to Mutual Futures\n\n{d['summary']}\n\n## Selected source locations\n\n{d['locations']}\n\n## Source status and open questions\n\n{d['caution']}\n\n## Guide and original are different\n\nThis is a reading guide, not a full transcription or replacement for the original. The public library reports whether the unchanged original is actually present in the repository. Original files in the handover bundle retain their original bytes. A proposal, an archived claim, a calculation and an independently verified fact are distinct.\n\nMutual Futures: {SITE['url']}\nRepository: {SITE['repo']}\n\nSource by Luke Nathan Hayes and the collaborators identified in the original. Guide prepared for Mutual Futures with ChatGPT, September 2026. Strange But True Public Source Licence; third-party rights remain with their holders.\n'''

for folder in ['assets','documents/guides','documents/originals']:(OUT/folder).mkdir(parents=True,exist_ok=True)
for name in ['style.css','app.js']:shutil.copy2(ROOT/'assets'/name,OUT/'assets'/name)
if (ROOT/'assets/images').exists():shutil.copytree(ROOT/'assets/images',OUT/'assets/images',dirs_exist_ok=True)
if (ROOT/'assets/asset-manifest.json').exists():shutil.copy2(ROOT/'assets/asset-manifest.json',OUT/'assets/asset-manifest.json')
for d in DOCS:
 write_utf8(OUT/d['guide_path'], guide(d));orig=ROOT/d['original_path'];d['original_available']=False
 if orig.exists():
  if hashlib.sha256(orig.read_bytes()).hexdigest()!=d['sha256']:raise ValueError('Original checksum mismatch: '+d['original_name'])
  shutil.copy2(orig,OUT/d['original_path']);d['original_available']=True
write_utf8(OUT/'documents/manifest.json', json.dumps(DOCS,indent=2,ensure_ascii=False)+'\n')
shutil.copy2(ROOT/'LICENCE.md',OUT/'LICENCE.md')

def extra(p):
 typ=p.get('type');h=''
 if typ=='library':
  h='<section class="section"><div class="wrap" data-filter-scope><label for="library-search" class="kicker">Search the document library</label><input class="search-box" id="library-search" data-search type="search" placeholder="Search titles, themes or source status"><div class="filter-row">'+''.join(f'<button class="filter {"active" if v=="all" else ""}" data-filter="{v}" aria-pressed="{str(v=="all").lower()}">{t}</button>' for v,t in [('all','All sources'),('working','Working papers'),('submission','Submissions'),('discussion','Discussion')])+'</div><p data-count class="small muted" role="status"></p><div class="library-grid">'
  for d in DOCS:
   category='working' if d['kind']=='Working paper' or d['kind']=='Specification working paper' else 'discussion' if d['kind']=='Discussion paper' else 'submission'
   h+=f'<article class="document" id="{d["id"]}" data-item data-category="{category}"><p class="doc-meta">{d["id"]} / {esc(d["kind"])} / {esc(d["pages"])}</p><h3>{esc(d["title"])}</h3><p>{esc(d["summary"])}</p><div class="tag-row"><span class="tag archived">Author source, not independent verification</span></div><div class="actions">'+link(d['guide_path'],'Download reading guide .md','button download',True)
   if d['original_available']:h+=link(d['original_path'],'Download unchanged original','button download',True)
   h+='</div>'
   if not d['original_available']:h+='<p class="original-pending">The unchanged original is not yet published in this repository. The downloadable guide is not the original document.</p>'
   h+='<details><summary>Source passages, status and credits</summary><p>'+esc(d['locations'])+'</p><p>'+esc(d['caution'])+'</p><p>Original filename: '+esc(d['original_name'])+'</p><p>Original checksum: <code>'+d['sha256']+'</code></p></details></article>'
  h+='</div><p hidden data-no-results class="no-results">No sources match this search.</p></div></section>'
 elif typ=='sources':
  h='<section class="section"><div class="wrap" data-filter-scope><label for="source-search" class="kicker">Search references and connections</label><input id="source-search" class="search-box" data-search type="search" placeholder="A project, source or subject"><div class="filter-row"><button class="filter active" data-filter="all" aria-pressed="true">All references</button><button class="filter" data-filter="project" aria-pressed="false">Project family</button><button class="filter" data-filter="external" aria-pressed="false">External sources</button></div><p data-count class="small muted" role="status"></p>'
  for r in PROJECTS+SOURCES:
   isproj=r in PROJECTS;h+=f'<article class="reference" id="{r["id"]}" data-item data-category="{"project" if isproj else "external"}"><span class="ref-code">{r["id"]}</span><div><h3>{esc(r["title"])}</h3><p>{esc(r["text"])}</p><p class="small">'+esc(r['role'] if isproj else r['kind']+' · '+r['checked'])+'</p>'+link(r['url'],'Open source ↗')
   if isproj:h+=' &nbsp; '+link('https://github.com/auraofintelligence/'+r['repo'],'Repository ↗')
   h+='</div></article>'
  h+='<p hidden data-no-results class="no-results">No references match this search.</p></div></section>'
 elif typ=='roadmap':
  h='<section class="section tint"><div class="wrap"><div class="timeline">'
  for year,title,text,status in TIMELINE:h+='<article class="reveal"><span class="year">'+esc(year)+'</span><h3>'+esc(title)+'</h3><p>'+esc(text)+'</p><span class="tag proposal">'+esc(status)+'</span></article>'
  h+='</div>'+refs(['P03','P10','D04','S03'])+'</div></section>'
 elif typ=='sitemap':
  h='<section class="section"><div class="wrap"><ol class="page-map">'+''.join('<li>'+link(q['slug']+'.html#top','<strong>'+esc(q['label'])+'</strong><span>'+esc(q['intro'])+'</span>')+'</li>' for q in PAGES)+'</ol></div></section>'
 elif typ=='about':
  h='<section class="section tint"><div class="wrap"><h2>Project links and tags</h2><div class="actions">'+link(SITE['repo'],'Open the standalone repository','button')+link('LICENCE.md','Read the source licence','button download',True)+'</div><p class="source-line">Public page: '+link(SITE['url'],esc(SITE['url']))+'</p></div></section>'
 elif typ=='licence':
  text=(ROOT/'LICENCE.md').read_text(encoding='utf-8');h='<section class="section"><div class="wrap prose measure">'
  for block in text.strip().split('\n\n'):
   if block.startswith('# '):continue
   if block.startswith('## '):h+='<h2 style="margin-top:38px">'+esc(block[3:])+'</h2>'
   else:h+='<p>'+esc(block).replace('\n','<br>')+'</p>'
  h+='<div class="actions">'+link('LICENCE.md','Download the licence .md','button download',True)+'</div></div></section>'
 return h

def build_page(p,index):
 plain=title_plain(p);base=SITE['url'];slug=p['slug'];home=slug=='index';accent={'gold':'var(--gold)','mint':'var(--mint)','violet':'var(--violet)'}[p['accent']]
 out=f'<!doctype html>\n<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(p["label"])} | Mutual Futures</title><meta name="description" content="{esc(p["intro"],quote=True)}"><meta name="theme-color" content="#f5f7f8"><link rel="canonical" href="{base}{"" if home else slug+".html"}"><meta property="og:type" content="website"><meta property="og:site_name" content="Mutual Futures"><meta property="og:title" content="{esc(plain,quote=True)}"><meta property="og:description" content="{esc(p["intro"],quote=True)}"><meta property="og:image" content="{base+image(p.get("image") or "civilisation-upgrade")}"><meta property="og:url" content="{base}{"" if home else slug+".html"}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/png" href="assets/images/mutual-futures-icon-32.png"><link rel="apple-touch-icon" href="assets/images/mutual-futures-icon-192.png"><link rel="stylesheet" href="assets/style.css?v=20260924-whole-systems"><script defer src="assets/app.js?v=20260924-upgrade"></script></head><body id="top" style="--accent:{accent}"><a class="skip" href="#main">Skip to content</a>'
 out+='<header class="site-head"><div class="wrap head-inner"><a class="brand" href="index.html#top"><img src="assets/images/mutual-futures-icon-192.png" alt="" width="44" height="44"><span>Mutual Futures</span></a><nav class="primary" aria-label="Primary">'
 for s,l in [('gajra','GAJRA Earth'),('ownership','Ownership'),('workforce','Work & life'),('take-part','Take part'),('library','Library')]:out+=f'<a href="{s}.html"'+(' aria-current="page"' if s==slug else '')+'>'+l+'</a>'
 out+='</nav><button class="index-toggle" data-open-index aria-expanded="false" aria-controls="site-index" type="button"><span>All chapters</span><span aria-hidden="true">+</span></button></div><div class="reading-progress" aria-hidden="true"></div></header>'
 out+='<dialog class="index-dialog" id="site-index" aria-labelledby="index-heading"><div class="dialog-inner"><div class="dialog-top"><h2 id="index-heading">Explore the topics</h2><button data-close-index class="close-menu" aria-label="Close chapter index" type="button">×</button></div><label for="index-search" class="kicker">Find a chapter</label><input id="index-search" class="search-box" type="search" placeholder="Search the topics"><p id="index-count" class="small muted" role="status">'+str(len(PAGES))+' pages</p><nav class="menu-grid" aria-label="All chapters">'+''.join(link(q['slug']+'.html#top',f'<small>{j:02d}</small>'+esc(q['label'])) for j,q in enumerate(PAGES))+'</nav></div></dialog>'
 out+='<main id="main"><section class="hero'+(' home' if home else '')+'"><div class="wrap hero-content">'
 if not home:out+='<div class="breadcrumb">'+link('index.html','Mutual Futures')+' / '+esc(p['label'])+'</div>'
 out+='<h1>'+p['title']+'</h1><p class="lede">'+esc(p['intro'])+'</p>'
 if home:out+='<div class="actions">'+link('gajra.html','Understand the guiding principle','button primary-button')+link('take-part.html','Find a way to contribute','button')+'</div>'
 elif p.get('tool'):out+='<div class="actions">'+link('#model','Read the case study and use the tool','button primary-button')+'</div>'
 out+='</div>'
 if p.get('image'):out+='<img class="hero-image" src="'+image(p['image'])+'" alt="'+esc(ASSETS[p['image']][2],quote=True)+'" fetchpriority="high">'
 out+='</section><div id="chapter">'
 if not home:
  out+='<nav class="wrap page-contents" aria-label="On this page"><strong>On this page</strong><ul>'+''.join('<li>'+link('#section-'+str(n),esc(s['title']))+'</li>' for n,s in enumerate(p['sections'],1))+'</ul></nav>'
 for n,s in enumerate(p['sections'],1):
  out+=section(s,n)
 if p.get('tool'):out+=case_study(p['tool'])+tools(p['tool'])
 out+=extra(p)+'</div>'
 prev=PAGES[index-1] if index else None;nextp=PAGES[index+1] if index<len(PAGES)-1 else PAGES[0]
 out+='<nav class="wrap chapter-nav" aria-label="Previous and next chapters">'
 out+=link((prev['slug'] if prev else 'site-map')+'.html#top','<span><small>'+('Previous chapter' if prev else 'Choose a path')+'</small><strong>'+esc(prev['label'] if prev else 'Full site map')+'</strong></span><span aria-hidden="true">↖</span>')
 out+=link(nextp['slug']+'.html#top','<span aria-hidden="true">↗</span><span><small>'+('Next chapter' if index<len(PAGES)-1 else 'Back to the beginning')+'</small><strong>'+esc(nextp['label'])+'</strong></span>')+'</nav></main>'
 out+='<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><a class="brand" href="index.html#top"><img src="assets/images/mutual-futures-icon-192.png" alt="" width="44" height="44"><span>Mutual Futures</span></a><p>A proposal for Joyful Responsible Abundance during the AI and automation transition, by Luke Nathan Hayes.</p></div><nav class="footer-links" aria-label="Workbench links"><h3>Explore the site</h3>'+link('site-map.html','Every chapter')+link('library.html','Document library')+link('sources.html','Sources and connections')+link('about.html','About and contact')+'</nav><nav class="footer-links" aria-label="Related project links"><h3>Related projects</h3>'+link('https://auraofintelligence.github.io/','Aura of Intelligence ↗')+link('https://auraofintelligence.github.io/500-Queens-VC-2026/','500 Queens ↗')+link('https://auraofintelligence.github.io/C-Hour-introduction/','C-Hour ↗')+link('https://auraofintelligence.github.io/GAJRA-earth-infinity/','GAJRA Earth ↗')+link(SITE['repo'],'GitHub repository ↗')+'</nav></div><div class="footer-bottom"><span>© 2026 Luke Nathan Hayes · '+link('licence.html','Strange But True Public Source Licence')+'</span><span>Tools run in your browser · No account · <button type="button" data-print class="print-button">Print this page</button></span></div></div></footer><a href="#top" class="to-top" aria-label="Back to top">↑</a></body></html>\n'
 return out
for i,p in enumerate(PAGES):write_utf8(OUT/(p['slug']+'.html'), build_page(p,i))
write_utf8(OUT/'.nojekyll', '')
write_utf8(OUT/'robots.txt', 'User-agent: *\nAllow: /\nSitemap: '+SITE['url']+'sitemap.xml\n')
write_utf8(OUT/'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+SITE['url']+('' if p['slug']=='index' else p['slug']+'.html')+'</loc></url>' for p in PAGES)+'</urlset>\n')
write_utf8(OUT/'404.html', '<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Mutual Futures</title><link rel="icon" type="image/png" href="https://auraofintelligence.github.io/mutual-futures/assets/images/mutual-futures-icon-32.png"><link rel="stylesheet" href="'+SITE['url']+'assets/style.css?v=20260924-whole-systems"></head><body><main class="wrap section"><p class="kicker">Mutual Futures / 404</p><h1>Page not found</h1><p>This address does not point to a page on this site.</p>'+link(SITE['url']+'site-map.html','Open the complete site map','button primary-button')+'</main></body></html>')
originals=sum(d['original_available'] for d in DOCS)
report=f'- {len(PAGES)} chapter and utility pages, plus a custom 404.\n- Four tool pages, including two funding models.\n- {len(DOCS)} source reading guides.\n- {originals} unchanged original documents present in this build.\n- {len(PROJECTS)} project connections and {len(SOURCES)} external source records.\n- Raster illustrations, no bundled fonts, no SVG.\n- Standalone public URL: {SITE["url"]}\n'
write_utf8(OUT/'build-report.md', report)
write_utf8(ROOT/'repository-metadata.json', json.dumps(dict(name='mutual-futures',description=SITE['description'][:350],homepage=SITE['url'],topics=SITE['topics']),indent=2)+'\n')
print(report)
