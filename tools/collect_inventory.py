from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/chemical-build/sources'
IMS='https://ims.internationalprocessplants.com'
paths=['plants','equipment/chemical-process-family','equipment/heat-exchanger','equipment/centrifuge','equipment/dryer','equipment/filter','equipment/column','equipment/tank']
def fetch(path):
 url=IMS+'/inventory/search/'+path
 with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r: raw=r.read().decode('utf-8')
 key='inventory-'+path.replace('/','-')
 (OUT/(key+'.html')).write_text(raw,encoding='utf-8')
 d=html.fromstring(raw)
 cards=[]
 for node in d.cssselect('.productRow') if False else d.xpath('//*[@class="productRow"]'):
  a=node.xpath('.//a[@class="productLink"]')
  if not a: continue
  attrs={}
  for r in node.xpath('.//*[@class="attributeText"]'):
   labels=r.xpath('.//*[@class="attributeLabel"]'); vals=r.xpath('.//*[@class="attributeValue"]')
   if labels and vals: attrs[labels[0].text_content().strip().rstrip(':')]=' '.join(vals[0].text_content().split())
  imgs=node.xpath('.//*[@class="imgContainer"]//img[1]')
  if not imgs: imgs=node.xpath('.//img[1]')
  cards.append({'title':' '.join(a[0].text_content().split()),'url':IMS+a[0].get('href'),'image':IMS+imgs[0].get('src') if imgs else '', 'attributes':attrs,'source':url})
 (OUT/(key+'.json')).write_text(json.dumps(cards,indent=2,ensure_ascii=False),encoding='utf-8')
 return key,len(cards),cards[:1],[(a.text_content().strip(),a.get('href')) for a in d.xpath('//a[contains(@href,"chemical") or contains(@href,"Chemical")]')][:8]
with ThreadPoolExecutor(max_workers=4) as pool:
 for r in pool.map(fetch,paths): print(r)
