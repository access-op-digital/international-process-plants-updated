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
 '603031': [('Capacity','105 million lb/year at 40 to 45% concentration'),('Technology','Metal oxide'),('Feedstocks','Methanol, oxygen'),('Location','Allentown, Pennsylvania, USA')],
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

# (name, IMS path, original description, materials statement, range statement, featured listing).
# Materials lead by listing count and ranges come from the IMS type filters, read-only, 8 Oct 2026.
# IMS publishes no type-level material or size filter for centrifuges and dryers, so those cards
# state the featured unit's size instead of an invented range.
category_data = [
 ('Reactors','reactor','Precision-controlled systems for chemical synthesis, available in glass-lined, stainless and specialty alloys.','Glass-lined units lead the reactor inventory, alongside stainless steel 316, 316L and 304, Hastelloy C-276 and C-22, and titanium.','Reactor capacities range from 2 L to 80,000 L (0.5 to 21,134 gal).','Featured listing: stainless steel 316L batch-type agitated reactor.'),
 ('Heat exchangers','heat-exchanger','Shell-and-tube and plate exchangers for thermal control and energy recovery.','Stainless steel 316 and graphite lead the heat exchanger inventory, alongside stainless steel 304 and 316L, carbon steel, titanium and Hastelloy C-276.','Heat transfer areas reach 2,124 m² (22,863 ft²).','Featured listing: shell, tubes and tubesheet in stainless steel 316L.'),
 ('Centrifuges','centrifuge','Used for purification, separation and crystallization. Basket, inverting and peeler models available.','','','Featured listing: Hastelloy C22 peeler centrifuge with a 630 mm (24.8 in) basket.'),
 ('Dryers','dryer','Moisture removal solutions including rotary, vacuum and disc dryers.','','','Featured listing: stainless steel 316 spray dryer with 31.8 kg/h (70 lb/h) evaporation.'),
 ('Filters','filter','Pressure and vacuum systems to remove particulates or recover solids.','Stainless steel 316 and polypropylene lead the filter inventory, alongside stainless steel 304, Hastelloy C-22 and C-276, and carbon steel.','Filtration areas reach 330 m² (3,557 ft²).','Featured listing: polypropylene plate-and-frame filter press.'),
 ('Distillation columns','column','For purification, solvent recovery and fractional separation.','Glass-lined and stainless steel 316 columns lead the inventory, alongside stainless steel 304, Hastelloy C-276 and graphite.','Column diameters range from 76 mm (3 in) to 8,000 mm (315 in).','Featured listing: glass-lined packed column with ceramic packing.'),
 ('Tanks','tank','For storage, blending and transfer. Jacketed and non-jacketed tanks available.','Stainless steel 304 and glass-lined tanks lead the inventory, alongside stainless steel 316 and 316L, carbon steel and fiberglass.','Tank capacities range from 5 L to 565,000 L (1 to 149,258 gal).','Featured listing: stainless steel 316L vertical tank.'),
]
# Leading makers per type, ranked by item count in IMS manufacturer filters (read-only, 6 Oct 2026).
# Duplicate IMS spellings (DeDietrich / DeDietrich (France)) were merged; proper brand spellings shown.
makers_by_type = {
 'reactor':'Pfaudler, De Dietrich, UGE and Gale Process Solutions',
 'heat-exchanger':'Alfa Laval, Vicarb, Ralph Coidan and Graham',
 'centrifuge':'Krauss Maffei, Alfa Laval, Westfalia and Sharples',
 'dryer':'Gale Process Solutions, Glatt, Niro and Pfaudler',
 'filter':'Schenk, Cogeim, Chemap and Rosenmund',
 'column':'Pfaudler, De Dietrich, Kühni and Schott',
 'tank':'Pfaudler, De Dietrich, Grundy and Sinclair Stainless Fabrications',
}
categories=[]
# Section shape per type: context opener (what IPP supplies, from which makers, to whom, for what),
# a lead-in and the subtypes IPP lists (IPP category hubs and IMS subtype filters, 8 Oct 2026),
# then the material and range values and the fields every listing states.
type_detail = {
 'reactor':('IPP supplies used reactors from Pfaudler, De Dietrich, UGE and Gale Process Solutions to chemical producers for batch and continuous synthesis.','IPP’s used reactor inventory includes:',['Batch-type agitated reactors with complete agitation','Batch type body only reactor shells','Hydrogenation reactors','Fixed bed catalytic reactors','Tubular continuous-flow reactors'],'Each reactor listing states capacity, internal pressure, temperature, material and condition.'),
 'heat-exchanger':('IPP supplies used heat exchangers from Alfa Laval, Vicarb, Ralph Coidan and Graham to chemical plants for heating, cooling and condensing process streams.','IPP’s used heat exchanger inventory includes:',['Shell-and-tube heat exchangers','Plate-and-frame heat exchangers','Spiral heat exchangers','Graphite block heat exchangers','Welded plate heat exchangers','Air fin coolers'],'Each heat exchanger listing states heat transfer area, shell and tube pressure, temperature and material.'),
 'centrifuge':('IPP supplies used centrifuges from Krauss Maffei, Alfa Laval, Westfalia and Sharples to chemical and pharmaceutical plants for solid-liquid separation.','IPP’s used centrifuge inventory includes:',['Bottom-discharge basket centrifuges','Top-discharge basket centrifuges','Peeler centrifuges','Inverting filter centrifuges','Disc bowl centrifuges','Solid bowl decanter centrifuges'],'Each centrifuge listing states basket or bowl size, material, filtration area and motor power.'),
 'dryer':('IPP supplies used dryers from Gale Process Solutions, Glatt, Niro and Pfaudler to chemical plants for removing moisture and solvents from powders, pastes and slurries.','IPP’s used dryer inventory includes:',['Rotary vacuum dryers','Double cone and twin shell dryers','Fluid bed dryers','Spray dryers','Paddle and ribbon dryers','Porcupine and screw dryers'],'Each dryer listing states chamber size, evaporation rate, inlet temperature and material.'),
 'filter':('IPP supplies used filters from Schenk, Cogeim, Chemap and Rosenmund to chemical plants for clarifying liquids and recovering solids.','IPP’s used filter inventory includes:',['Filter presses','Rosenmund and Cogeim filter dryers','Nutsche filters','Pressure leaf filters'],'Each filter listing states filtration area, pressure, temperature and material.'),
 'column':('IPP supplies used distillation columns from Pfaudler, De Dietrich, Kühni and Schott to chemical plants for solvent recovery and product purification.','IPP’s used column inventory includes:',['Packed columns','Tray columns','Combination columns','Contactor columns'],'Each column listing states diameter, length, pressure and temperature.'),
 'tank':('IPP supplies used tanks from Pfaudler, De Dietrich, Grundy and Sinclair Stainless Fabrications to chemical plants for raw material storage, blending and product transfer.','IPP’s used tank inventory includes:',['Glass-lined tanks','Stainless steel 304, 316 and 316L tanks','Jacketed process tanks','Non-jacketed storage tanks','Carbon steel and fiberglass tanks'],'Each tank listing states capacity, internal pressure, temperature and material.'),
}
for name,path,desc,materials,size_range,featured in category_data:
 context,lead,items,fields=type_detail[path]
 values=''.join(f'<p class="range-note">{E(x)}</p>' for x in (materials,size_range) if x)
 subtypes=''.join(f'<li>{E(i)}</li>' for i in items)
 categories.append(f'<div class="category-card"><div class="category-heading"><span class="line-icon">{icons["VESSEL"]}</span><h3>{name}</h3></div><p>{desc} {E(context)}</p><p class="type-lead">{E(lead)}</p><ul class="type-list">{subtypes}</ul>{values}<p class="type-fields">{E(fields)}</p><p class="material-note">{featured}</p><div class="category-links"><a href="{IMS}/inventory/search/equipment/{path}">Browse used {name.lower()} ↗</a></div></div>')

faq_data=[
 ('Does IPP offer full chemical plants for sale?',f'Yes. In addition to individual equipment, we sell <a href="{IMS}/inventory/search/plants">complete chemical process plants</a>, including teardown and relocation services.'),
 ('Can I inspect the equipment before buying?',f'Yes. IPP offers on-site and video inspections for most equipment. <a href="{SITE}/contact/">Contact us</a> to schedule one.'),
 ('Where does IPP source its chemical equipment?','From multinational chemical producers, toll manufacturers and decommissioned or restructured facilities worldwide.'),
 ('What is chemical process plant equipment?',f'Chemical process plant equipment is the set of reactors, heat exchangers, centrifuges, dryers, filters, columns and tanks that converts raw materials into chemical products. Read IPP’s <a href="{SITE}/what-is-chemical-process-plant-equipment/">chemical process plant equipment guide</a>.'),
 ('How do I get a price for a chemical plant or equipment?',f'IPP quotes each plant and unit individually. <a href="{SITE}/contact/">Contact IPP</a> with the stock number or your process requirements. The quotation defines the assets included and any dismantling, loading, shipping or start-up services.'),
 ('Can IPP help with international shipping?','Yes. IPP coordinates packaging, crating, freight and delivery, or buyers can arrange their own shipping. Confirm the asset location, loading requirements and destination when you request a quotation.'),
 ('What documentation is available for a used plant?','Documentation varies by asset. IPP shares the equipment lists, drawings, process descriptions and inspection records available for each plant or stock number.'),
 ('Is financing available?',f'Yes. IPP advertises financing for its plants and equipment. <a href="{SITE}/contact/">Contact IPP</a> to discuss terms for your purchase.'),
 ('Does IPP sell new chemical process equipment?',f'Yes. <a href="https://www.galeprocesssolutions.com/">Gale Process Solutions (GPS)</a>, an IPP group company, fabricates new stainless steel process equipment with 12 to 16 week average delivery. <a href="https://www.uge-inc.com/">Universal Glasteel Equipment (UGE)</a> supplies new and re-glassed glass-lined equipment.'),
 ('Does IPP buy shutdown chemical plants and surplus equipment?',f'Yes. IPP buys complete plants, process lines and individual equipment from shutdown, idled and restructured sites. Start with the <a href="{SITE}/sell-plants/">sell a plant</a> or <a href="{SITE}/sell-equipment/">sell equipment</a> form.'),
 ('What information should I provide when selling?',f'Provide an asset list, photographs, the plant location, available technical documents and your removal deadline. <a href="{SITE}/contact/">IPP’s team</a> reviews the information and confirms the next steps.'),
 ('Does IPP buy the land and buildings with a chemical plant?',f'Yes. IPP purchases complete plant sites, including the land, buildings, equipment and intellectual property. IPP also buys individual process units and equipment systems within a site. <a href="{SITE}/sell-to-ipp/">Read how selling to IPP works</a>.'),
 ('Does IPP assume environmental obligations at a plant site?',f'Yes, in some acquisitions. IPP buys sites with known contamination and assumes site cleanup and regulatory compliance obligations as the buyer. IPP’s remediation partners work with local environmental authorities on each site. <a href="{SITE}/sell-plants/">Discuss a site exit with IPP</a>.'),
 ('What happens to a chemical plant site after a sale?','The purchase agreement defines the outcome. A sale can cover equipment for removal or the entire site, and IPP’s published projects include equipment relocation and site repurposing.'),
]
faqs=''.join(f'<details><summary>{E(q)}</summary><p>{a}</p></details>' for q,a in faq_data)
resource_data=[
 ('Guide','What is chemical process plant equipment?','what-is-chemical-process-plant-equipment','The reactors, heat exchangers, separators and dryers inside a chemical process plant.'),
 ('Guide','What is an industrial plant? Types of process plants','what-is-an-industrial-plant-types-of-process-plants','How industrial and process plants are classified by product and process.'),
 ('Guide','What is a glass-lined reactor?','what-is-a-glass-lined-reactor-corrosion-resistant-technology-for-chemical-and-pharma-production','How a glass lining protects reactors in corrosive chemical and pharmaceutical service.'),
 ('Guide','What is a chemical reactor?','what-is-a-chemical-reactor','How chemical reactors work, with the main reactor types.'),
 ('Guide','What is petrochemical process equipment?','what-is-petro-chemical-process-equipment','The equipment that converts oil and gas feedstocks into petrochemicals.'),
 ('For sellers','Plant decommissioning with IPP','5-reasons-ipp-is-your-best-choice-for-plant-decommissioning','Why plant owners choose IPP for decommissioning and dismantling.'),
]
resources=''.join(f'<a class="blog-card" href="{SITE}/{path}/"><span class="blog-label">{E(kind)}</span><h4>{E(label)}</h4><p>{E(desc)}</p><span class="text-link" aria-hidden="true">Read article ↗</span></a>' for kind,label,path,desc in resource_data)
# Leading manufacturers by listing count in the IMS manufacturer filters (read-only, 8 Oct 2026),
# then the two IPP group companies. Each link is a type-scoped IMS search that renders that maker's
# listings: Pfaudler 349 reactors, DeDietrich 129, Alfa Laval 95 heat exchangers, Krauss Maffei 62
# and Westfalia 57 centrifuges, Gale Process Solutions 38 and UGE 42 reactors. Counts stay out of the copy.
leading_makers=[
 ('Pfaudler','reactor','Pfaudler','Glass-lined reactors, tanks and agitators'),
 ('De Dietrich','reactor','DeDietrich','Glass-lined reactors and tanks'),
 ('Alfa Laval','heat-exchanger','Alfa Laval','Heat exchangers and centrifuges'),
 ('Krauss Maffei','centrifuge','Krauss Maffei','Centrifuges'),
 ('Westfalia','centrifuge','Westfalia','Centrifuges'),
 ('Gale Process Solutions','reactor','Gale Process Solutions','New stainless steel equipment from the IPP group'),
 ('Universal Glasteel Equipment','reactor','UGE','New and re-glassed glass-lined equipment from the IPP group'),
]
mfr_links=[f'<li><a href="{E(IMS+"/inventory/search/equipment/"+path+"?manufacturer="+quote(ims_name))}" target="_blank" rel="noopener noreferrer">{E(name)} <span aria-hidden="true">↗</span></a><span>{E(families)}</span></li>' for name,path,ims_name,families in leading_makers]
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

# Keep exported copy and the outline aligned with the actual built page. Every H2 section carries
# data-section = its outline index; H3/H4 rows are found by heading text inside their parent section,
# so each prose row gets its own sections/H###.html for the commercial-content section checks.
doc=html.fromstring(template)
outline=json.loads((WORK/'outline.json').read_text(encoding='utf-8'))
(WORK/'sections').mkdir(exist_ok=True)
for stale in (WORK/'sections').glob('H*.html'): stale.unlink()
norm=lambda s: ' '.join(s.split()).lower()
def container_of(heading):
 el=heading.getparent()
 for _ in range(4):
  if el.xpath('.//p'): return el
  el=el.getparent()
 return heading.getparent()
section_el={}
plain_sections=[]
for section in doc.xpath('//section[@data-section]'):
 for node in section.xpath('.//svg|.//aside|.//*[@id="inventory-tools"]|.//*[@id="empty-results"]'):
  node.getparent().remove(node)
 section_el[int(section.get('data-section'))]=section
 plain_sections.append(html.tostring(section,encoding='unicode').strip()+'\n')
def top_parent(i):
 while outline[i].get('parent_index') not in (None,0): i=outline[i]['parent_index']
 return i
missing=[]
for idx,row in enumerate(outline):
 if row['hv']=='li' or row.get('carries_prose') is False: continue
 if idx in section_el:
  # A parent section's own copy excludes the cards and steps its child rows carry.
  el=html.fromstring(html.tostring(section_el[idx],encoding='unicode'))
  kids={norm(r['topic']) for r in outline if r.get('parent_index')==idx and r['hv'] in ('H3','H4')}
  for h in [h for h in el.xpath('.//h3|.//h4') if norm(h.text_content()) in kids]:
   box=container_of(h)
   if box is not el and box.getparent() is not None: box.getparent().remove(box)
  for empty in el.xpath('.//ol[not(li)]|.//ul[not(li)]'): empty.getparent().remove(empty)
  # Labels, captions, buttons, citation lines and badge rows are page furniture, not section prose.
  for deco in el.xpath('.//*[contains(@class,"eyebrow") or contains(@class,"seller-visual") or contains(@class,"button-row") or contains(@class,"source-note") or contains(@class,"recognition-badges")]'):
   if deco.getparent() is not None: deco.getparent().remove(deco)
 else:
  scope=section_el.get(top_parent(idx))
  hits=[h for h in (scope.xpath('.//h3|.//h4|.//summary') if scope is not None else []) if norm(h.text_content())==norm(row['topic'])]
  if not hits: missing.append(row['topic']); continue
  el=container_of(hits[0])
  if hits[0].tag=='summary':
   # An FAQ row's copy is its answer; the question is the row heading.
   el=html.fromstring(html.tostring(el,encoding='unicode'))
   for q in el.xpath('.//summary'): q.getparent().remove(q)
 text=html.tostring(el,encoding='unicode').strip()+'\n'
 row.update({'written_html':text,'written_ok':True})
 (WORK/'sections'/f'H{idx:03}.html').write_text(text,encoding='utf-8')
assert not missing,f'Outline rows with no rendered copy: {missing}'
(WORK/'outline.json').write_text(json.dumps(outline,indent=2,ensure_ascii=False),encoding='utf-8')
(WORK/'content.html').write_text('\n'.join(plain_sections),encoding='utf-8')
print('Built',OUT.relative_to(ROOT), 'with',len(cards),'sourced listings and',len(faq_data),'FAQs.')
