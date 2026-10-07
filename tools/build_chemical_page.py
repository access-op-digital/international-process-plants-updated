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
 '76524': [('Drive power', '11.6 kW (15.5 hp)'), ('Drive speed', '175 rpm'), ('Ratio', '10:1'), ('Transmission', 'Belt')],
 '705876': [('Capacity', '12,500 L (3,300 US gal)'), ('Material', 'Stainless steel 316'), ('Pressure', '4 bar (58 psi)'), ('Temperature', '160 °C (320 °F)')],
 '242533': [('Surface area','14.6 m² (approx. 157 ft²)'),('Material','Stainless steel 316L'),('Shell pressure','10 bar (145 psi)'),('Shell temp.','185 °C (365 °F)')],
 '220954': [('Evaporation', '340.2 kg/h (750 lb/h)'), ('Material', 'Hastelloy C22 clad'), ('Surface area', '14 m² (150.7 ft²)'), ('Temperature', '250 °C (482 °F)')],
 '211545': [('Diameter','800 mm (31.5 in)'),('Material','Glass-lined'),('Pressure','2 bar (29 psi)'),('Temperature','200 °C (392 °F)')],
 '236163': [('Diameter', '2,200 mm (86.6 in)'), ('Material', 'Stainless steel 321'), ('Pressure', '15 bar (217.6 psi)'), ('Temperature', '300 °C (572 °F)')],
 '235730': [('Basket diameter','630 mm (24.8 in)'),('Material','Hastelloy C22'),('Filtration area','0.6 m² (6.5 ft²)'),('Motor power','18 kW (24.1 hp)')],
 '225365': [('Filtration area','37 m² (398.3 ft²)'),('Material','Polypropylene'),('Pressure','6.9 bar (100 psi)'),('Temperature','21.1 °C (70 °F)')],
 '238212': [('Diameter','1,250 mm (49 in)'),('Material','Stainless steel 316'),('Evaporation','31.8 kg/h (70 lb/h)'),('Inlet temp.','354.4 °C (670 °F)')],
 '242886': [('Capacity','34,000 L (9,000 US gal)'),('Material','Stainless steel 316L'),('Pressure','3.5 bar (50.8 psi)'),('Temperature','100 °C (212 °F)')],
 '239007': [('Vessel size', '1,150 L (300 US gal)'), ('Material', 'Glass-lined, re-glassed'), ('Agitator type', '3-blade retreat curve'), ('Span', '914 mm (36 in)')],
}
makers = {
 '242492':('Sinclair Stainless Fabrications LTD.','Used','Stainless steel 316L'),
 '232498':('Gale Process Solutions','New','Stainless steel 316L'),
 '76524':('Pfaudler', 'Used', ''),
 '705876':('Tankki OY', 'Used', 'Stainless steel 316'),
 '242533':('Graham Hart Ltd','Used','Stainless steel 316L'),
 '220954':('SMS Buss', 'Used', 'Hastelloy C22'),
 '211545':('Estrella','Re-glassed','Glass-lined'),
 '236163':('Doring & Baumer', 'Used', 'Stainless steel 321'),
 '235730':('Krauss Maffei','Used','Hastelloy C22'),
 '225365':('Perrin','Used','Polypropylene'),
 '238212':('APV Anhydro','Used','Stainless steel 316'),
 '242886':('Cookson & Zinn Ltd','Used','Stainless steel 316L'),
 '239007':('Pfaudler', 'Re-glassed', 'Glass-lined'),
}
# IMS search path per equipment category; drives the type link under the listing grid.
ims_type = {'Reactors':'reactor','Agitators':'agitator','Fermenters':'fermenter','Heat exchangers':'heat-exchanger','Evaporators':'evaporator','Distillation columns':'column','Stills':'still','Centrifuges':'centrifuge','Filters':'filter','Dryers':'dryer','Tanks':'tank','Glass-lined parts':'glass-lined-parts','Reactor parts':'reactor-parts'}
# IMS plant type slug per plant category; drives the plant link under the listing grid.
plant_type = {'Chemical & specialty':'chemical-and-specialty-chemical','Fertilizer & agrochemical':'fertilizer-and-agrochemical','Petrochemical':'petrochemical','Pharmaceutical':'pharmaceutical'}
cards=[]
for key in facts:
 r=records[key]; maker,condition,material=makers.get(key,('','',''))
 r.update({'manufacturer':maker,'condition':condition,'material':material,'display_specs':dict(facts[key])})
 image = f'<img src="{r["local_image"]}" alt="{E(r["display_title"])}; IPP stock {key}" width="{r["image_width"]}" height="{r["image_height"]}" loading="lazy" decoding="async">' if r.get('local_image') else '<span class="no-photo"><span class="line-icon">'+icons['PLANT']+'</span>Request plant photographs</span>'
 tag = condition if r['group']=='equipment' else r['category']
 attrs = ' '.join(f'data-{k}="{E(v)}"' for k,v in {'group':r['group'],'category':r['category'],'manufacturer':maker,'condition':condition,'material':material,'ims':ims_type.get(r['category'],'') if r['group']=='equipment' else plant_type.get(r['category'],'')}.items())
 specs=''.join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k,v in facts[key])
 stock=('P' if r['group']=='plants' else '#')+key
 cards.append(f'''<article class="stock-card" {attrs} id="stock-{key}"><div class="stock-image">{image}<span class="stock-tag">{E(tag)}</span></div><div class="stock-content"><p class="stock-number">IPP STOCK {stock}</p><h3>{E(r['display_title'])}</h3><dl>{specs}</dl><div class="card-actions"><a class="button button-dark" href="{r['url']}" target="_blank" rel="noopener noreferrer" aria-label="View Specs for {E(r['display_title'])}, stock {stock}, opens in a new tab">View Specs <span aria-hidden="true">↗</span></a><a href="{SITE}/contact/" aria-label="Enquire about stock {stock}">Enquire ↗</a></div></div></article>''')

# (name, IMS path, original description, materials statement, range statement, featured listing).
# Materials lead by listing count and ranges come from the IMS type filters, read-only, 8 Oct 2026.
# IMS publishes no type-level material or size filter for centrifuges and dryers, so those cards
# state the featured unit's size instead of an invented range.
# Equipment types in the reference service-section format: one tab and one panel per type.
# Panel shape: preserved original sentence, a two-sentence context opener (what IPP supplies, to whom,
# from which makers), a lead-in, descriptive items, then a closing paragraph with the listing fields,
# the leading materials and the IMS range (read-only, 8 Oct 2026), and the pricing factors with the
# quote and inspection offer. IPP publishes no prices, so the reference page's price ranges become
# the factors each quote depends on.
type_panels = [
 ('Reactors',
  'reactor',
  'Precision-controlled systems for chemical synthesis, available in glass-lined, stainless and specialty alloys.',
  'We supply used reactors to chemical plants that need batch or continuous synthesis capacity for reaction, mixing and heat transfer under controlled pressure '
  'and temperature. As a supplier chemical producers trust worldwide, IPP sources reactors from Pfaudler, De Dietrich, UGE and Gale Process Solutions, '
  'documents each stock number and coordinates removal, shipping and start-up support through one team.',
  'Our used reactor inventory covers:',
  ['Batch-type agitated reactors with complete agitation systems',
   'Batch type body only reactor shells for buyers with existing drives',
   'Hydrogenation reactors for high-pressure hydrogen service',
   'Fixed bed catalytic and tubular continuous-flow reactors',
   'Glass-lined reactors re-glassed through Universal Glasteel Equipment'],
  ['Each reactor listing states capacity, internal pressure, temperature, material and condition, so process engineers can match a unit to the reaction before '
   'an inspection.',
   'Glass-lined units lead our reactor inventory, alongside stainless steel 316, 316L and 304, Hastelloy C-276 and C-22 and titanium, with capacities from 2 L '
   'to 80,000 L (0.5 to 21,134 gal).',
   'Pricing depends on manufacturer, capacity, material of construction and condition, and IPP quotes each stock number individually with a video or on-site '
   'inspection on request.'],
  'Featured listing: stainless steel 316L batch-type agitated reactor.'),
 ('Agitators',
  'agitator',
  'Glass drives, drive units and shaft mixers for reactors, tanks and blending vessels.',
  'IPP supplies used agitators to chemical plants that mix, suspend and disperse materials in reactors, tanks and blending vessels. With agitators from '
  'Pfaudler, Lightnin, De Dietrich, Philadelphia and Chemineer in stock, our team matches the drive power, shaft length and impeller to the vessel each buyer '
  'runs.',
  'Agitator types in our inventory cover:',
  ['Glass drives for glass-lined reactors',
   'Motor and gear drive units for vertical mounting',
   'Shaft and mixer assemblies with pitch-blade impellers',
   'Hastelloy C-276 shafts for corrosive service',
   'Pfaudler DTW and De Dietrich DIN drive models'],
  ['Each agitator listing states drive power, speed, shaft length and impeller type.',
   'Glass-lined and carbon steel units lead our agitator inventory, alongside Hastelloy C-276 and stainless steel 316, for vessels from 76 L to 10,031 L (20 to '
   '2,650 gal) and drives up to 101 kW (135 hp).',
   'Pricing depends on manufacturer, drive power, material of construction and condition, and our team quotes each stock number individually.'],
  'Featured listing: Pfaudler 4DTW glass drive with 11.6 kW (15.5 hp) drive power.'),
 ('Fermenters',
  'fermenter',
  'Stainless steel fermenters for biochemical, pharmaceutical and fermentation-based chemical production.',
  'We supply used fermenters to chemical, pharmaceutical and biotech plants that grow cultures and make fermentation-based products under controlled '
  'temperature and pressure. As a source process engineers trust for fermentation capacity, IPP stocks units from ThermoFisher, B. Braun Diessel Biotech, '
  'Bujalski, Biolafitte, Chemap and Sartorius.',
  'Our used fermenter inventory covers:',
  ['Agitated stainless steel fermenters',
   'Fermenters with standard and dimple jackets',
   'Single-use fermenters from ThermoFisher',
   'Laboratory and pilot fermenters',
   'Unused production-scale fermenters'],
  ['Each fermenter listing states capacity, pressure, temperature, jacket and agitation details.',
   'Stainless steel 316 and 304 lead our fermenter inventory, alongside stainless steel 316L, with capacities from 19 L to 65,300 L (5 to 17,250 gal).',
   'Pricing depends on manufacturer, capacity, material of construction and condition, and IPP quotes each stock number individually with a video or on-site '
   'inspection on request.'],
  'Featured listing: stainless steel 316 fermenter with 12,500 L (3,300 gal) capacity.'),
 ('Heat exchangers',
  'heat-exchanger',
  'Shell-and-tube and plate exchangers for thermal control and energy recovery.',
  'IPP supplies used heat exchangers to chemical plants for heating, cooling, condensing and heat recovery across process streams. With exchangers from Alfa '
  'Laval, Vicarb, Ralph Coidan and Graham in stock, our team matches shell, tube and plate configurations to the thermal duty each buyer specifies.',
  'Our used heat exchanger inventory covers:',
  ['Shell-and-tube heat exchangers for process heating and cooling',
   'Plate-and-frame heat exchangers for compact thermal duty',
   'Graphite block heat exchangers for corrosive process streams',
   'Spiral and welded plate heat exchangers',
   'Air fin coolers for process stream cooling'],
  ['Each heat exchanger listing states heat transfer area, shell and tube pressure, temperature and material.',
   'Stainless steel 316 and graphite lead our heat exchanger inventory, alongside stainless steel 304 and 316L, carbon steel, titanium and Hastelloy C-276, '
   'with heat transfer areas up to 2,124 m² (22,863 ft²).',
   'Pricing depends on manufacturer, heat transfer area, material of construction and condition, and our team quotes each stock number individually.'],
  'Featured listing: shell, tubes and tubesheet in stainless steel 316L.'),
 ('Evaporators',
  'evaporator',
  'Film, flash and crystallizer evaporators for concentration and solvent removal.',
  'We supply used evaporators to chemical plants that concentrate solutions, recover solvents and crystallize products. As a supplier chemical producers trust '
  'for evaporation duty, IPP sources units from Luwa SMS, Buss-SMS-Canzler, Buflovak/Blaw Knox and Pfaudler and records evaporation rate and heat transfer area '
  'for each stock number.',
  'Evaporator types in our inventory cover:',
  ['Rising and falling film evaporators, including multiple-effect systems',
   'Wiped and thin film evaporators',
   'Flash evaporators',
   'Crystallizer evaporators from zero liquid discharge systems',
   'Hastelloy C-22 clad and titanium units for corrosive service'],
  ['Each evaporator listing states evaporation rate, heat transfer area, pressure and temperature.',
   'Stainless steel 316 leads our evaporator inventory, alongside stainless steel 304 and 316L, fiberglass, glass-lined steel and titanium, with evaporation '
   'rates from 4.5 kg/h to 36,300 kg/h (10 to 80,000 lb/h) and heat transfer areas up to 1,473 m² (15,850 ft²).',
   'Pricing depends on manufacturer, evaporation rate, material of construction and condition, and our team quotes each stock number individually.'],
  'Featured listing: Hastelloy C-22 clad wiped film evaporator with 340 kg/h (750 lb/h) evaporation.'),
 ('Distillation columns and stills',
  'column',
  'For purification, solvent recovery and fractional separation.',
  'IPP supplies used distillation columns and stills to chemical and pharmaceutical plants for solvent recovery, product purification and fractional '
  'separation. With Pfaudler, De Dietrich, Kühni and Schott columns and Santasalo-Sohlberg, Finn-Aqua and Paul Mueller stills in stock, we supply packed, tray '
  'and column still designs in glass-lined steel, stainless steel and specialty alloys.',
  'Column and still types in our inventory cover:',
  ['Packed columns, including ceramic-packed glass-lined units',
   'Tray and combination packed and tray columns',
   'Contactor columns for liquid-liquid extraction',
   'Column stills and pot stills',
   'Multiple-effect stills with skid-mounted controls'],
  ['Each column and still listing states diameter, length, pressure and temperature.',
   'Glass-lined and stainless steel 316 columns lead our column inventory, alongside stainless steel 304, Hastelloy C-276 and graphite, with diameters from 76 '
   'mm (3 in) to 8,000 mm (315 in).',
   'Stainless steel 316, 316L and 321 lead our still inventory, with diameters from 229 mm (9 in) to 2,210 mm (87 in).',
   'Pricing depends on manufacturer, diameter, material of construction and condition, and our team quotes each stock number individually.'],
  'Featured listings: glass-lined packed column with ceramic packing and a stainless steel 321 column still.',
  [('Browse used distillation columns', 'column'), ('Browse used stills', 'still')]),
 ('Centrifuges',
  'centrifuge',
  'Used for purification, separation and crystallization. Basket, inverting and peeler models available.',
  'We supply used centrifuges to chemical and pharmaceutical plants for solid-liquid separation, crystal recovery and product purification. As a source process '
  'engineers trust for separation equipment, IPP stocks Krauss Maffei, Alfa Laval, Westfalia and Sharples machines and records the basket or bowl size, '
  'material and motor power for each stock number.',
  'Centrifuge types in our inventory cover:',
  ['Bottom-discharge and top-discharge basket centrifuges',
   'Peeler centrifuges, including Hastelloy units',
   'Inverting filter centrifuges',
   'Disc bowl centrifuges for liquid clarification',
   'Solid bowl decanter centrifuges for continuous separation'],
  ['Each centrifuge listing states basket or bowl size, material, filtration area and motor power.',
   'Our featured Krauss Maffei peeler centrifuge carries 0.6 m² (6.5 ft²) of filtration area and an 18 kW (24.1 hp) motor.',
   'Pricing depends on manufacturer, model, material of construction and condition, and IPP quotes each stock number individually with a video or on-site '
   'inspection on request.'],
  'Featured listing: Hastelloy C22 peeler centrifuge with a 630 mm (24.8 in) basket.'),
 ('Filters',
  'filter',
  'Pressure and vacuum systems to remove particulates or recover solids.',
  'We supply used filters to chemical plants that clarify process liquids, recover solids and wash and dry filter cake. As a supplier chemical producers trust '
  'for solid-liquid separation, IPP sources filters from Schenk, Cogeim, Chemap and Rosenmund and lists filtration area, pressure and material for each stock '
  'number.',
  'Our used filter inventory covers:',
  ['Filter presses for high-volume solids recovery',
   'Rosenmund and Cogeim filter dryers',
   'Nutsche filters for batch filtration',
   'Pressure leaf filters for liquid clarification'],
  ['Each filter listing states filtration area, pressure, temperature and material.',
   'Stainless steel 316 and polypropylene lead our filter inventory, alongside stainless steel 304, Hastelloy C-22 and C-276 and carbon steel, with filtration '
   'areas up to 330 m² (3,557 ft²).',
   'Pricing depends on manufacturer, filtration area, material of construction and condition, and IPP quotes each stock number individually with a video or '
   'on-site inspection on request.'],
  'Featured listing: polypropylene plate-and-frame filter press.'),
 ('Dryers',
  'dryer',
  'Moisture removal solutions including rotary, vacuum and disc dryers.',
  'IPP supplies used dryers to chemical plants that remove moisture and solvents from powders, pastes, crystals and slurries. With dryers from Gale Process '
  'Solutions, Glatt, Niro and Pfaudler in stock, we match the drying principle, chamber size and material to each product.',
  'Our used dryer inventory covers:',
  ['Rotary vacuum dryers',
   'Double cone and twin shell dryers',
   'Fluid bed dryers for granular products',
   'Spray dryers for liquid feeds',
   'Paddle, ribbon, porcupine and screw dryers'],
  ['Each dryer listing states chamber size, evaporation rate, inlet temperature and material.',
   'Our featured APV Anhydro spray dryer evaporates 31.8 kg/h (70 lb/h) at a 354.4 °C (670 °F) inlet temperature in stainless steel 316.',
   'Pricing depends on manufacturer, drying capacity, material of construction and condition, and our team quotes each stock number individually.'],
  'Featured listing: stainless steel 316 spray dryer with 31.8 kg/h (70 lb/h) evaporation.'),
 ('Tanks',
  'tank',
  'For storage, blending and transfer. Jacketed and non-jacketed tanks available.',
  'We supply used tanks to chemical plants for raw material storage, blending and product transfer. As a supplier chemical producers trust for vessel capacity, '
  'IPP sources tanks from Pfaudler, De Dietrich, Grundy and Sinclair Stainless Fabrications in jacketed and non-jacketed designs.',
  'Our used tank inventory covers:',
  ['Glass-lined tanks for corrosive chemicals',
   'Stainless steel 304, 316 and 316L process tanks',
   'Jacketed tanks for heating and cooling',
   'Non-jacketed storage tanks',
   'Carbon steel and fiberglass storage tanks'],
  ['Each tank listing states capacity, internal pressure, temperature and material.',
   'Stainless steel 304 and glass-lined tanks lead our tank inventory, alongside stainless steel 316 and 316L, carbon steel and fiberglass, with capacities '
   'from 5 L to 565,000 L (1 to 149,258 gal).',
   'Pricing depends on manufacturer, capacity, material of construction and condition, and IPP quotes each stock number individually with a video or on-site '
   'inspection on request.'],
  'Featured listing: stainless steel 316L vertical tank.'),
 ('Glass-lined and reactor parts',
  'glass-lined-parts',
  'Spare parts that return glass-lined and alloy reactors to service.',
  'IPP supplies used, re-glassed and new glass-lined parts to chemical plants that maintain Pfaudler, De Dietrich and other glass-lined reactors and tanks. '
  'Glass-lined parts form the largest equipment type in our chemical processing inventory, and we also stock new seals and seal plans for exotic alloy '
  'reactors.',
  'Glass-lined and reactor parts in our inventory cover:',
  ['Glass-lined agitators, including retreat curve and Cryo-Lock blades',
   'Main covers and manway covers',
   'Baffles, thermowells and adapter plates',
   'Pro-rings, split flanges and clamps',
   'Hastelloy C-22 seals and seal plans for exotic alloy reactors'],
  ['Each part listing states the vessel size it fits, diameter, length and whether the part is re-glassed.',
   'Pfaudler and De Dietrich parts lead our glass-lined parts inventory, alongside 3V Tech, Schott and UGE, for vessels from 8 L to 37,850 L (2 to 10,000 gal).',
   'Pricing depends on manufacturer, vessel size, glass condition and re-glassing, and IPP quotes each stock number individually with a video or on-site '
   'inspection on request.'],
  'Featured listing: re-glassed Pfaudler retreat curve agitator for a 1,150 L (300 gal) vessel.',
  [('Browse used glass-lined parts', 'glass-lined-parts'), ('Browse reactor parts', 'reactor-parts')])
]

type_tabs=''.join(f'<button type="button" role="tab" id="tab-type-{path}" aria-controls="type-{path}" aria-selected="{"true" if i==0 else "false"}"{"" if i==0 else " tabindex=\"-1\""}>{E(name)}</button>' for i,(name,path,*_) in enumerate(type_panels))
categories=[]
for name,path,summary,opener,lead,items,close,featured,*more in type_panels:
 links=more[0] if more else [(f'Browse used {name.lower()}',path)]
 subtypes=''.join(f'<li>{E(i)}</li>' for i in items)
 categories.append(f'<div class="category-card type-panel" id="type-{path}" role="tabpanel" aria-labelledby="tab-type-{path}"><div class="category-heading"><h3>{name}</h3></div><p class="type-summary">{summary}</p><p>{E(opener)}</p><p class="type-lead">{E(lead)}</p><ul class="type-list">{subtypes}</ul><p class="type-close">{E(" ".join(close))}</p><p class="material-note">{featured}</p><div class="category-links">{"".join(f'<a href="{IMS}/inventory/search/equipment/{p}">{E(label)} ↗</a>' for label,p in links)}</div></div>')

faq_data=[
 ('Does IPP offer full chemical plants for sale?',f'Yes. In addition to individual equipment, we sell <a href="{IMS}/inventory/search/plants">complete chemical process plants</a>, including teardown and relocation services.'),
 ('Can I inspect the equipment before buying?',f'Yes. IPP offers on-site and video inspections for most equipment. <a href="{SITE}/contact/">Contact us</a> to schedule one.'),
 ('Where does IPP source its chemical equipment?','From multinational chemical producers, toll manufacturers and decommissioned or restructured facilities worldwide.'),
 ('What is chemical process plant equipment?',f'Chemical process plant equipment is the set of reactors, heat exchangers, centrifuges, dryers, filters, columns and tanks that converts raw materials into chemical products. Read IPP’s <a href="{SITE}/what-is-chemical-process-plant-equipment/">chemical process plant equipment guide</a>.'),
 ('How do I get a price for a chemical plant or equipment?',f'We quote each plant and unit individually. <a href="{SITE}/contact/">Contact IPP</a> with the stock number or your process requirements. The quotation defines the assets included and any dismantling, loading, shipping or start-up services.'),
 ('Can IPP help with international shipping?','Yes. We coordinate packaging, crating, freight and delivery, or buyers can arrange their own shipping. Confirm the asset location, loading requirements and destination when you request a quotation.'),
 ('What documentation is available for a used plant?','Documentation varies by asset. We share the equipment lists, drawings, process descriptions and inspection records available for each plant or stock number.'),
 ('Is financing available?',f'Yes. IPP advertises financing for its plants and equipment. <a href="{SITE}/contact/">Contact IPP</a> to discuss terms for your purchase.'),
 ('Does IPP sell new chemical process equipment?',f'Yes. <a href="https://www.galeprocesssolutions.com/">Gale Process Solutions (GPS)</a>, an IPP group company, fabricates new stainless steel process equipment with 12 to 16 week average delivery. <a href="https://www.uge-inc.com/">Universal Glasteel Equipment (UGE)</a> supplies new and re-glassed glass-lined equipment.'),
 ('Does IPP buy shutdown chemical plants and surplus equipment?',f'Yes. We buy complete plants, process lines and individual equipment from shutdown, idled and restructured sites. Start with the <a href="{SITE}/sell-plants/">sell a plant</a> or <a href="{SITE}/sell-equipment/">sell equipment</a> form.'),
 ('What information should I provide when selling?',f'Provide an asset list, photographs, the plant location, available technical documents and your removal deadline. <a href="{SITE}/contact/">Our team</a> reviews the information and confirms the next steps.'),
 ('Does IPP buy the land and buildings with a chemical plant?',f'Yes. IPP purchases complete plant sites, including the land, buildings, equipment and intellectual property. We also buy individual process units and equipment systems within a site. <a href="{SITE}/sell-to-ipp/">Read how selling to IPP works</a>.'),
 ('Does IPP assume environmental obligations at a plant site?',f'Yes, in some acquisitions. IPP buys sites with known contamination and assumes site cleanup and regulatory compliance obligations as the buyer. Our remediation partners work with local environmental authorities on each site. <a href="{SITE}/sell-plants/">Discuss a site exit with IPP</a>.'),
 ("Which companies sell chemical plants to IPP?","Fortune 100 and Fortune 500 companies typically represent 95% of the sellers IPP works with, according to IPP. IPP occasionally buys assets from smaller manufacturers in distressed situations."),
 ("Does IPP buy equipment as-is, where-is?","Yes. IPP buys used, surplus and idled equipment as-is, where-is, as a principal buyer rather than a broker. Our team arranges inspection, dismantling, packaging, freight and export."),
 ("Can IPP market a plant instead of buying it outright?","Yes. IPP proposes either an outright purchase or a marketing arrangement that offers the assets to its global buyer network. IPP markets BASF’s ammonia, methanol and melamine plants at Ludwigshafen under such an agreement."),
 ("Does IPP handle decommissioning and dismantling?","Yes. Our team decommissions and dismantles the plant, then packs, ships and exports the equipment. IPP holds ISN RAVS Plus verification for plant decommissioning work."),
 ('What happens to a chemical plant site after a sale?','The purchase agreement defines the outcome. A sale can cover equipment for removal or the entire site, and our published projects include equipment relocation and site repurposing.'),
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
 ('Pfaudler','reactor','Pfaudler','Glass-lined reactors (RA, E, BE and ELL models), tanks, agitators and columns'),
 ('De Dietrich','reactor','DeDietrich','Glass-lined reactors (SA, CTJ, STA and CSA models), tanks and columns'),
 ('Alfa Laval','heat-exchanger','Alfa Laval','Heat exchangers and centrifuges'),
 ('Krauss Maffei','centrifuge','Krauss Maffei','Centrifuges, including Hastelloy C22 peeler units'),
 ('Westfalia','centrifuge','Westfalia','Centrifuges'),
 ('Gale Process Solutions','reactor','Gale Process Solutions','New 316L stainless steel and Hastelloy reactors from the IPP group, 12 to 16 week average delivery'),
 ('Universal Glasteel Equipment','reactor','UGE','New, used, rebuilt and re-glassed glass-lined equipment, including UA-300 and UA-500 reactors'),
]
mfr_links=[f'<li><a href="{E(IMS+"/inventory/search/equipment/"+path+"?manufacturer="+quote(ims_name))}" target="_blank" rel="noopener noreferrer">{E(name)} <span aria-hidden="true">↗</span></a><span>{E(families)}</span></li>' for name,path,ims_name,families in leading_makers]
logos=''.join(f'<img src="/assets/chemical/{filename}" alt="{name}" width="104" height="48" loading="lazy">' for filename,name in [('shell.png','Shell'),('sanofi.png','Sanofi'),('lilly.png','Lilly'),('DOW.png','Dow'),('lonza.png','Lonza'),('air-products.png','Air Products')])

plain=lambda s: html.fromstring('<div>'+s+'</div>').text_content()
schema={'@context':'https://schema.org','@graph':[
 {'@type':'Organization','@id':SITE+'/#organization','name':'International Process Plants','alternateName':'IPP','url':SITE+'/','logo':SITE+'/wp-content/uploads/2023/12/IPP-LOGO_DARKBLUE-FINAL.png','telephone':'+1-609-586-8004','email':'sales@internationalprocessplants.com','address':{'@type':'PostalAddress','streetAddress':'410 Princeton Hightstown Road','addressLocality':'Princeton Junction','addressRegion':'NJ','postalCode':'08550','addressCountry':'US'}},
 {'@type':'CollectionPage','@id':CANONICAL+'#webpage','url':CANONICAL,'name':'Used Chemical Process Plants for Sale','description':'Used chemical plants, process lines and individual equipment for sale from International Process Plants.','inLanguage':'en','publisher':{'@id':SITE+'/#organization'},'about':{'@type':'Thing','name':'Used chemical process plants'},'mainEntity':{'@id':CANONICAL+'#inventory'},'breadcrumb':{'@id':CANONICAL+'#breadcrumb'}},
 {'@type':'BreadcrumbList','@id':CANONICAL+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':url} for i,(name,url) in enumerate([('Home',SITE+'/'),('Process plants',SITE+'/plants/'),('Chemical plants and equipment',CANONICAL)])]},
 {'@type':'ItemList','@id':CANONICAL+'#inventory','name':'Selected chemical plant and process equipment listings','itemListElement':[{'@type':'ListItem','position':i+1,'name':records[key]['display_title'],'url':records[key]['url']} for i,key in enumerate(facts)]},
 {'@type':'VideoObject','name':'The International Process Plants team is outstanding! They understand my business','description':'Chuck Castley, commercial vice president at Chemicals Incorporated in Baytown, Texas, checks in with International Process Plants at the SOCMA 2024 trade show in Nashville, Tuesday, Feb. 20, 2024.','thumbnailUrl':'https://i.ytimg.com/vi/1Qhma3r0Cas/hqdefault.jpg','uploadDate':'2024-03-12','embedUrl':'https://www.youtube.com/embed/1Qhma3r0Cas','url':'https://www.youtube.com/watch?v=1Qhma3r0Cas','publisher':{'@id':SITE+'/#organization'}},
 {'@type':'VideoObject','name':'If somebody asked me to rate IPP 1-10, I’d give them a 10 every time!','description':'Joel Salzman, VP of Operations for ChemDesign Products, Inc., in Marinette, Wisconsin, takes a minute at SOCMA 2024 in Nashville to explain why he values his decades-long business relationship with International Process Plants.','thumbnailUrl':'https://i.ytimg.com/vi/WlsjZMptSZg/hqdefault.jpg','uploadDate':'2024-03-12','embedUrl':'https://www.youtube.com/embed/WlsjZMptSZg','url':'https://www.youtube.com/watch?v=WlsjZMptSZg','publisher':{'@id':SITE+'/#organization'}},
 {'@type':'VideoObject','name':'The power of partnership: A testimonial to International Process Plants’ customer commitment','description':'Clay Pace, President of Commercial & Technology at Seatex, LLC in Houston shares how International Process Plants puts the needs of its customers first and share an example of the company’s commitment to customer satisfaction. Pace spoke at SOCMA 2024 in Nashville on February 20, 2024.','thumbnailUrl':'https://i.ytimg.com/vi/BWWcZNOchrY/hqdefault.jpg','uploadDate':'2024-03-05','embedUrl':'https://www.youtube.com/embed/BWWcZNOchrY','url':'https://www.youtube.com/watch?v=BWWcZNOchrY','publisher':{'@id':SITE+'/#organization'}},
 {'@type':'VideoObject','name':'Communication and quick customer response are what sets IPP apart','description':'Keith West, International Process Plants’ Director of Global Equipment Sales, catches up with Anna Nguyen, Hoyer Global’s Commercial Sales & Operations Manager, at SOCMA 2024 in Nashville on February 20, 2024.','thumbnailUrl':'https://i.ytimg.com/vi/Kz6N9uacqkY/hqdefault.jpg','uploadDate':'2024-03-10','embedUrl':'https://www.youtube.com/embed/Kz6N9uacqkY','url':'https://www.youtube.com/watch?v=Kz6N9uacqkY','publisher':{'@id':SITE+'/#organization'}},
 {'@type':'FAQPage','@id':CANONICAL+'#faqs','isPartOf':{'@id':CANONICAL+'#webpage'},'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':plain(a)}} for q,a in faq_data]}
]}
template=(ROOT/'src/chemical-page.html').read_text(encoding='utf-8')
substitutions={'SCHEMA':json.dumps(schema,ensure_ascii=False,separators=(',',':')),'OG_IMAGE':records['603031']['image'],'LOGOS':logos,'INVENTORY':'\n'.join(cards),'CATEGORIES':'\n'.join(categories),'TYPE_TABS':type_tabs,'MANUFACTURERS':'\n'.join(mfr_links),'FAQS':faqs,'RESOURCES':resources,**{'ICON_'+k:v for k,v in icons.items()}}
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
  for deco in el.xpath('.//*[contains(@class,"eyebrow") or contains(@class,"seller-visual") or contains(@class,"button-row") or contains(@class,"source-note") or contains(@class,"recognition-badges") or contains(@class,"vtab-list") or contains(@class,"type-tab-list")]'):
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
