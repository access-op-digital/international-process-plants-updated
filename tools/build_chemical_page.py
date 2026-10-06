"""Build the static chemical collection page from an editable template and sourced records.

Run with Python + lxml. No network call and no live site change.
"""
from pathlib import Path
from html import escape
from urllib.parse import quote
from lxml import html
import json

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs/chemical-build'
WORK = DOCS/'content'
SITE = 'https://internationalprocessplants.com'
IMS = 'https://ims.internationalprocessplants.com'
CANONICAL = SITE+'/chemical-process-plant-equipment-used-systems-for-sale/'
OUT = ROOT/'chemical-process-plant-equipment-used-systems-for-sale/index.html'
E = escape
SVG = '<svg viewBox="0 0 48 48" aria-hidden="true">{}</svg>'
icons = {
 'PLANT': SVG.format('<path d="M5 40V23l12-7v9l12-7v22M29 40V6h8l3 34M4 40h40M10 32h3m8 0h3m10-15h4m-4 7h5"/>'),
 'VESSEL': SVG.format('<path d="M13 13c0-6 22-6 22 0v22c0 6-22 6-22 0zM13 14c0 6 22 6 22 0M24 3v33m-6-5h12M16 39v6m16-6v6M6 19h7m22 9h7"/>'),
 'CYCLE': SVG.format('<path d="M9 18A16 16 0 0 1 36 11l4 6M40 6v11H29M39 30A16 16 0 0 1 12 37l-4-6M8 42V31h11M19 24h10m-5-5v10"/>')
}
records = {r['id']:r for r in json.loads((DOCS/'inventory.json').read_text(encoding='utf-8'))}
# All values below are transcribed from individual IMS detail pages. Metric/imperial
# pairs use the published detail values, except formaldehyde mass conversion noted in QA.
facts = {
 '603031': [('Capacity','105 million lb/year at 40–45% concentration'),('Technology','Metal oxide'),('Feedstocks','Methanol, oxygen'),('Location','Allentown, Pennsylvania, USA')],
 '603039': [('Capacity','1,030 tpd'),('Technology','Grand-Paroisse / Uhde'),('Feedstock','Ammonia'),('Location','Montoir-de-Bretagne, France')],
 '603040': [('Capacity','1,120 tpd'),('Feedstocks','Nitric acid, ammonia'),('Location','Montoir-de-Bretagne, France')],
 '601610': [('Capacity','275 TPD (82,500 TPY)'),('Technology','ICI / Johnson Matthey'),('Feedstocks','Natural gas, CO₂'),('Location','Camaçari, Bahia, Brazil')],
 '601813': [('Reactor volume','Approx. 1,200 m³ total'),('Location','Grimsby, England, UK')],
 '603016': [('Capacity','15,000 metric tonnes/year'),('Feedstocks','Sulfur, soda ash')],
 '242492': [('Capacity','12,300 L (3,250 US gal)'),('Material','Stainless steel 316L'),('Pressure','6 bar (87 psi)'),('Temperature','185 °C (365 °F)')],
 '232498': [('Capacity','15,150 L (4,000 US gal)'),('Material','Stainless steel 316L'),('Pressure','10 bar (145 psi)'),('Temperature','150 °C (302 °F)')],
 '242533': [('Surface area','14.6 m² (approx. 157 ft²)'),('Material','Stainless steel 316L'),('Shell pressure','10 bar (145 psi)'),('Shell temp.','185 °C (365 °F)')],
 '235730': [('Basket diameter','630 mm (24.8 in)'),('Material','Hastelloy C22'),('Filtration area','0.6 m² (6.5 ft²)'),('Motor power','18 kW (24.1 hp)')],
 '238212': [('Diameter','1,250 mm (49 in)'),('Material','Stainless steel 316'),('Evaporation','31.8 kg/h (70 lb/h)'),('Inlet temp.','354.4 °C (670 °F)')],
 '225365': [('Filtration area','37 m² (398.3 ft²)'),('Material','Polypropylene'),('Pressure','6.9 bar (100 psi)'),('Temperature','21.1 °C (70 °F)')],
 '211545': [('Diameter','800 mm (31.5 in)'),('Material','Glass-lined'),('Pressure','2 bar (29 psi)'),('Temperature','200 °C (392 °F)')],
 '242886': [('Capacity','34,000 L (9,000 US gal)'),('Material','Stainless steel 316L'),('Pressure','3.5 bar (50.8 psi)'),('Temperature','100 °C (212 °F)')],
}
makers = {
 '242492':('Sinclair Stainless Fabrications LTD.','Used','Stainless steel 316L'),
 '232498':('Gale Process Solutions','New','Stainless steel 316L'),
 '242533':('Graham Hart Ltd','Used','Stainless steel 316L'),
 '235730':('Krauss Maffei','Used','Hastelloy C22'),
 '238212':('APV Anhydro','Used','Stainless steel 316'),
 '225365':('Perrin','Used','Polypropylene'),
 '211545':('Estrella','Re-glassed','Glass-lined'),
 '242886':('Cookson & Zinn Ltd','Used','Stainless steel 316L'),
}
cards=[]
for key in facts:
 r=records[key]; maker,condition,material=makers.get(key,('','',''))
 r.update({'manufacturer':maker,'condition':condition,'material':material,'display_specs':dict(facts[key])})
 image = f'<img src="{r["local_image"]}" alt="{E(r["display_title"])}; IPP stock {key}" width="{r["image_width"]}" height="{r["image_height"]}" loading="lazy" decoding="async">' if r.get('local_image') else '<span class="no-photo"><span class="line-icon">'+icons['PLANT']+'</span>Request plant photographs</span>'
 tag = condition if r['group']=='equipment' else r['category']
 attrs = ' '.join(f'data-{k}="{E(v)}"' for k,v in {'group':r['group'],'category':r['category'],'manufacturer':maker,'condition':condition,'material':material}.items())
 specs=''.join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k,v in facts[key])
 stock=('P' if r['group']=='plants' else '#')+key
 cards.append(f'''<article class="stock-card" {attrs} id="stock-{key}"><div class="stock-image">{image}<span class="stock-tag">{E(tag)}</span></div><div class="stock-content"><p class="stock-number">IPP STOCK {stock}</p><h3>{E(r['display_title'])}</h3><dl>{specs}</dl><div class="card-actions"><a class="button button-dark" href="{r['url']}" target="_blank" rel="noopener noreferrer" aria-label="View Specs for {E(r['display_title'])}, stock {stock}, opens in a new tab">View Specs <span aria-hidden="true">↗</span></a><a href="{SITE}/contact/" aria-label="Enquire about stock {stock}">Enquire ↗</a></div></div></article>''')

category_data = [
 ('Reactors','reactor','Precision-controlled systems for chemical synthesis, available in glass-lined, stainless and specialty alloys.','Featured listing: stainless steel 316L batch-type agitated reactor.'),
 ('Heat exchangers','heat-exchanger','Shell-and-tube and plate exchangers for thermal control and energy recovery.','Featured listing: shell, tubes and tubesheet in stainless steel 316L.'),
 ('Centrifuges','centrifuge','Used for purification, separation and crystallization. Basket, inverting and peeler models available.','Featured listing: Hastelloy C22 peeler centrifuge.'),
 ('Dryers','dryer','Moisture removal solutions including rotary, vacuum and disc dryers.','Featured listing: stainless steel 316 spray dryer.'),
 ('Filters','filter','Pressure and vacuum systems to remove particulates or recover solids.','Featured listing: polypropylene plate-and-frame filter press.'),
 ('Distillation columns','column','For purification, solvent recovery and fractional separation.','Featured listing: glass-lined packed column with ceramic packing.'),
 ('Tanks','tank','For storage, blending and transfer. Jacketed and non-jacketed tanks available.','Featured listing: stainless steel 316L vertical tank.'),
]
categories=[]
for name,path,desc,mat in category_data:
 hub=f'<a href="{SITE}/process-equipment/{path}/">{E(name)} guide</a>' if path!='column' else ''
 categories.append(f'<div class="category-card"><div class="category-heading"><span class="line-icon">{icons["VESSEL"]}</span><h3>{name}</h3></div><p>{desc}</p><p class="material-note">{mat}</p><div class="category-links">{hub}<a href="{IMS}/inventory/search/equipment/{path}">Browse {name.lower()} ↗</a></div></div>')

faq_data=[
 ('Does IPP offer full chemical plants for sale?',f'Yes. In addition to individual equipment, we sell <a href="{IMS}/inventory/search/plants">complete chemical process plants</a>, including teardown and relocation services.'),
 ('Can I inspect the equipment before buying?',f'Yes. IPP offers on-site and video inspections for most equipment. <a href="{SITE}/contact/">Contact us</a> to schedule one.'),
 ('Where does IPP source its chemical equipment?','From multinational chemical producers, toll manufacturers and decommissioned or restructured facilities worldwide.'),
 ('What is chemical process plant equipment?',f'This refers to the machines and systems used in chemical manufacturing, including reactors, exchangers, centrifuges, dryers, and more. Read our <a href="{SITE}/what-is-chemical-process-plant-equipment/">chemical process plant equipment guide</a>.'),
 ('How do I get a price for a chemical plant or equipment?',f'<a href="{SITE}/contact/">Contact IPP</a> with the stock number or your process requirements. The quotation needs to define the assets included and any dismantling, loading, shipping or other services requested.'),
 ('Can IPP help with international shipping?','Yes. IPP offers international shipping options, or buyers can arrange their own shipping. Confirm the asset’s location, loading requirements and delivery destination when discussing the purchase.'),
 ('What documentation is available for a used plant?',f'Available documentation varies by asset. Ask IPP for equipment lists, drawings, process descriptions and inspection records for the plant or stock number you are considering.'),
 ('Is financing available?',f'Yes. IPP advertises financing for its plants and equipment. <a href="{SITE}/contact/">Contact IPP</a> to discuss availability and terms for your proposed purchase.'),
 ('Does IPP buy shutdown chemical plants and surplus equipment?',f'Yes. IPP buys complete plants, process lines and individual equipment. Use the <a href="{SITE}/sell-plants/">sell a plant</a> or <a href="{SITE}/sell-equipment/">sell equipment</a> form to start an assessment.'),
 ('What information should I provide when selling?',f'Share an asset list, photographs, the plant location, available technical documents and your removal timeline. <a href="{SITE}/contact/">IPP’s team</a> can then discuss the assessment and next steps.'),
 ('How quickly can IPP assess assets for sale?',f'<a href="{SITE}/sell-plants/">Send IPP your asset information</a> and removal deadline to request a project-specific schedule. The team will need to establish the asset scope, available documentation and site access.'),
 ('What happens to a chemical plant site after a sale?','A transaction may cover equipment for removal or an entire site. IPP’s published projects include equipment relocation and site repurposing. The purchase agreement defines which assets or property are included and who is responsible for the work.'),
]
faqs=''.join(f'<details><summary>{E(q)}</summary><p>{a}</p></details>' for q,a in faq_data)
resource_data=[
 ('What is chemical process plant equipment?','what-is-chemical-process-plant-equipment'),
 ('What is an industrial plant? Types of process plants','what-is-an-industrial-plant-types-of-process-plants'),
 ('What is a glass-lined reactor?','what-is-a-glass-lined-reactor-corrosion-resistant-technology-for-chemical-and-pharma-production'),
 ('What is a chemical reactor?','what-is-a-chemical-reactor'),
 ('What is petrochemical process equipment?','what-is-petro-chemical-process-equipment'),
 ('Plant decommissioning with IPP','5-reasons-ipp-is-your-best-choice-for-plant-decommissioning'),
]
resources=''.join(f'<a href="{SITE}/{path}/">{E(label)}<span aria-hidden="true">↗</span></a>' for label,path in resource_data)
verified_mfr = json.loads((DOCS/'manufacturer-verification.json').read_text(encoding='utf-8')) if (DOCS/'manufacturer-verification.json').exists() else {}
mfr_links=[]
for key,(name,condition,material) in makers.items():
 href=IMS+'/inventory/search/equipment?manufacturer='+quote(name) if verified_mfr.get('selected') else records[key]['url']
 mfr_links.append(f'<a href="{E(href)}" target="_blank" rel="noopener noreferrer">{E(name)} <span aria-hidden="true">↗</span></a>')
logos=''.join(f'<img src="/assets/chemical/{filename}" alt="{name}" width="104" height="48" loading="lazy">' for filename,name in [('shell.png','Shell'),('sanofi.png','Sanofi'),('lilly.png','Lilly'),('DOW.png','Dow'),('lonza.png','Lonza'),('air-products.png','Air Products')])

plain=lambda s: html.fromstring('<div>'+s+'</div>').text_content()
schema={'@context':'https://schema.org','@graph':[
 {'@type':'Organization','@id':SITE+'/#organization','name':'International Process Plants','alternateName':'IPP','url':SITE+'/','logo':SITE+'/wp-content/uploads/2023/12/IPP-LOGO_DARKBLUE-FINAL.png','telephone':'+1-609-586-8004','email':'sales@internationalprocessplants.com','address':{'@type':'PostalAddress','streetAddress':'410 Princeton Hightstown Road','addressLocality':'Princeton Junction','addressRegion':'NJ','postalCode':'08550','addressCountry':'US'}},
 {'@type':'CollectionPage','@id':CANONICAL+'#webpage','url':CANONICAL,'name':'Used Chemical Process Plants for Sale','description':'Used chemical plants, process lines and individual equipment for sale from International Process Plants.','inLanguage':'en','publisher':{'@id':SITE+'/#organization'},'about':{'@type':'Thing','name':'Used chemical process plants'},'mainEntity':{'@id':CANONICAL+'#inventory'},'breadcrumb':{'@id':CANONICAL+'#breadcrumb'}},
 {'@type':'BreadcrumbList','@id':CANONICAL+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':url} for i,(name,url) in enumerate([('Home',SITE+'/'),('Process plants',SITE+'/plants/'),('Chemical plants and equipment',CANONICAL)])]},
 {'@type':'ItemList','@id':CANONICAL+'#inventory','name':'Selected chemical plant and process equipment listings','itemListElement':[{'@type':'ListItem','position':i+1,'name':records[key]['display_title'],'url':records[key]['url']} for i,key in enumerate(facts)]},
 {'@type':'FAQPage','@id':CANONICAL+'#faqs','isPartOf':{'@id':CANONICAL+'#webpage'},'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':plain(a)}} for q,a in faq_data]}
]}
template=(ROOT/'src/chemical-page.html').read_text(encoding='utf-8')
substitutions={'SCHEMA':json.dumps(schema,ensure_ascii=False,separators=(',',':')),'OG_IMAGE':records['603031']['image'],'LOGOS':logos,'INVENTORY':'\n'.join(cards),'CATEGORIES':'\n'.join(categories),'MANUFACTURERS':'\n'.join(mfr_links),'FAQS':faqs,'RESOURCES':resources,**{'ICON_'+k:v for k,v in icons.items()}}
for key,value in substitutions.items(): template=template.replace('{{'+key+'}}',value)
assert '{{' not in template,'Unfilled template slot'
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(template,encoding='utf-8')
(DOCS/'display-inventory.json').write_text(json.dumps(list(records.values()),indent=2,ensure_ascii=False),encoding='utf-8')
(DOCS/'structured-data.json').write_text(json.dumps(schema,indent=2,ensure_ascii=False),encoding='utf-8')

# Keep exported copy and the outline aligned with the actual built page.
doc=html.fromstring(template)
sections=doc.xpath('//section[@data-section]')
outline=json.loads((WORK/'outline.json').read_text(encoding='utf-8'))
(WORK/'sections').mkdir(exist_ok=True)
plain_sections=[]
for section in sections:
 idx=int(section.get('data-section'))
 # Section bodies include all authored subordinate headings and lists.
 snippet=html.tostring(section,encoding='unicode')
 for node in section.xpath('.//svg|.//aside|.//*[@id="inventory-tools"]|.//*[@id="empty-results"]'):
  node.getparent().remove(node)
 section_text=html.tostring(section,encoding='unicode').strip()+'\n'
 node=outline[idx];node.update({'written_html':section_text,'written_ok':True,'written_summary':node['assigned_facts']})
 (WORK/'sections'/f'H{idx:03}.html').write_text(section_text,encoding='utf-8')
 plain_sections.append(section_text)
(WORK/'outline.json').write_text(json.dumps(outline,indent=2,ensure_ascii=False),encoding='utf-8')
(WORK/'content.html').write_text('\n'.join(plain_sections),encoding='utf-8')
print('Built',OUT.relative_to(ROOT), 'with',len(cards),'sourced listings and',len(faq_data),'FAQs.')
