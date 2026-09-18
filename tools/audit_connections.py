#!/usr/bin/env python3
"""Verify the small authorised backlinks without changing source projects."""
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,urllib.request,urllib.error
ROOT=Path(__file__).resolve().parents[1]
spec=spec_from_file_location('mf_content',ROOT/'content/site.py');module=module_from_spec(spec);spec.loader.exec_module(module)
def get(url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mutual-Futures-connection-audit/1.0','Cache-Control':'no-cache'})
  with urllib.request.urlopen(req,timeout=30) as r:return r.status,r.read()
 except urllib.error.HTTPError as e:return e.code,b''
 except Exception as e:return str(e),b''
def audit(p):
 repo=p['repo'];base=f'https://raw.githubusercontent.com/auraofintelligence/{repo}/HEAD/'
 rs,rb=get(base+'README.md');ps,pb=get(base+'index.html')
 return {'source_id':p['id'],'repository':'auraofintelligence/'+repo,'readme_backlink':b'<!-- mutual-futures-connection -->' in rb,'readme_http_status':rs,'homepage_backlink':b'id="mutual-futures-connection"' in pb,'homepage_http_status':ps,'homepage_expected':repo!='australian-legal-engine','source_homepage':p['url'],'readme_sha256':hashlib.sha256(rb).hexdigest() if rb else None,'homepage_sha256':hashlib.sha256(pb).hexdigest() if pb else None}
with ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(audit,module.PROJECTS))
report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'method':'HTTP reads of the current public repository README and index source. A source backlink is separate from verification of its hosted Pages deployment.','connections':results,'readme_confirmed':sum(x['readme_backlink'] for x in results),'homepage_source_confirmed':sum(x['homepage_backlink'] for x in results)}
(ROOT/'docs').mkdir(exist_ok=True);(ROOT/'docs/reciprocal-links.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
