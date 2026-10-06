"""Read public IPP sources and the supplied workbook; does not alter remote systems."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, openpyxl
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'chemical-build' / 'sources'
OUT.mkdir(parents=True, exist_ok=True)
BOOK = Path(r'C:\Users\dilbd\Downloads\Used Chemical Process Plants for Sale _ International Process Plants .xlsx')
wb = openpyxl.load_workbook(BOOK, data_only=True)
intake = {s.title:[{'row':i,'values':list(r)} for i,r in enumerate(s.iter_rows(values_only=True),1) if any(v is not None for v in r)] for s in wb}
(OUT.parent/'workbook-intake.json').write_text(json.dumps(intake,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
BASE = 'https://internationalprocessplants.com/'
urls = {
 'existing':BASE+'chemical-process-plant-equipment-used-systems-for-sale/',
 'reactor-reference':BASE+'process-equipment/reactor/',
 'home':BASE,
 'about':BASE+'about-us/',
 'plants':BASE+'plants/',
 'seller':BASE+'sell-shut-down-chemical-processing-plant-assets-with-help-from-ipp/',
 'sell-equipment':BASE+'sell-equipment/',
 'sell-plants':BASE+'sell-plants/',
 'buy-used':BASE+'buy-used/',
 'basf':BASE+'basf-and-ipp-partner-to-market-ammonia-methanol-and-melamine-plants/',
 'chemical-processing':BASE+'ipp-featured-in-chemical-processing-for-its-chemical-plant-work/',
 'novartis':BASE+'ipp-acquires-novartis-uks-grimsby-api-manufacturing-plant-boosting-onshoring-efforts/',
 'isn':BASE+'ipp-earns-isn-ravs-plus-designation-highlighting-its-excellence-in-safe-and-sustainable-plants-and-equipment-decommissioning/',
 'cdmo':BASE+'ipp-completes-acquisition-of-cdmos-api-process-plant-equipment/',
 'chemical-engineering':'https://www.chemengonline.com/cost-engineering-with-previously-owned-process-equipment/',
 'ims':'https://ims.internationalprocessplants.com/inventory/search/equipment/reactor',
 'ims-plants':'https://ims.internationalprocessplants.com/search',
}
def fetch(pair):
 name,url=pair
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r:
   raw=r.read()
   (OUT/(name+'.html')).write_text(raw.decode('utf-8',errors='replace'),encoding='utf-8')
   return {'name':name,'url':url,'final_url':r.url,'status':r.status,'bytes':len(raw)}
 except Exception as e: return {'name':name,'url':url,'error':str(e)}
with ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(fetch,urls.items()))
(OUT/'manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
for r in results: print(r)
