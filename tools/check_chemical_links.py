"""Read-only validation of the draft's public links, with no form submissions."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from lxml import html
import json

ROOT=Path(__file__).resolve().parents[1]
doc=html.fromstring((ROOT/'chemical-process-plant-equipment-used-systems-for-sale/index.html').read_text(encoding='utf-8'))
urls=sorted({a for a in doc.xpath('//a/@href') if a.startswith('https://')})
def check(url):
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'},method='GET'),timeout=35) as r:
   raw=r.read().decode('utf-8',errors='replace')
   result={'url':url,'status':r.status,'final':r.geturl()}
  if 'ims.internationalprocessplants.com' in url and 'manufacturer=' in url:
   d=html.fromstring(raw); state=d.xpath('//script[@id="beta-search-state-data"]/text()')
   result['selected_manufacturer']=json.loads(state[0])['criteria']['SelectedManufacturerNames'] if state else []
  return result
 except Exception as ex: return {'url':url,'error':str(ex)}
with ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(check,urls))
(ROOT/'docs/chemical-build/link-check.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('Checked',len(results),'distinct public URLs.')
for r in results:
 if r.get('error') or r.get('status')!=200 or ('selected_manufacturer' in r and not r['selected_manufacturer']): print(r)
