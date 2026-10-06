"""Prepare the operator-authored commercial outline for deterministic skill checks."""
from pathlib import Path
import json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT/'docs/chemical-build/content'
SKILL = Path.home()/'.agents/skills/anup-commercial-content/scripts'
WORK.mkdir(parents=True,exist_ok=True)
def save(name,obj): (WORK/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
save('input.json', {'entity':'Used chemical process plants','primary keyword':'used chemical process plants for sale','title':'Used Chemical Process Plants for Sale','commercial sub-type':'collection','market country':'us','business context':'International Process Plants (IPP) buys and sells complete used process plants, process lines and individual equipment worldwide. Preserve valuable existing copy and brand. User supplied a revised outline and tracker.','page macro context':'Optimize the existing chemical page for buyers first, with a supporting seller section. Preserve existing URL and seven categories.','direct query network':'used chemical process plants for sale\nused chemical plant equipment\nchemical process equipment for sale'})
subprocess.run([sys.executable,str(SKILL/'prepare_job.py'),'--work',str(WORK),'--input',str(WORK/'input.json')],check=True)
save('context.json',{'macro_context':'Purchase and sale of chemical manufacturing assets','primary_entity':'Used chemical process plants','primary_intent':'Find available plants and equipment; inspect specifications and contact IPP','business_entity':'International Process Plants (IPP)','content_type':'Commercial collection page','audience_type':'Chemical plant owners, procurement teams, engineering and operations managers','commercial_orientation':'Buyer first, seller support','generation_route':'in-session','template':'Updated user workbook: Suggested Outline plus Task Tracker. Relative section order preserved; category, seller, manufacturer and location sections inserted from tracker.','constraints':['No new canonical URL','No fabricated prices, reviews, warranties or reviewer sign-off','No live publication or redirects','Preserve valuable existing category and FAQ copy']})
headings = [
 ('H1','Used Chemical Process Plants for Sale','Primary entity and preserved equipment-led introduction','business_weighted'),
 ('H2','Trusted around the world by','Six client logos featured on the IPP homepage; no invented rating','business_weighted'),
 ('H2','Buy used chemical plants and equipment from International Process Plants (IPP)','Retain company description, published inventory footprint with date and source','business_weighted'),
 ('H2','Chemical plants and equipment for sale','Selected verified IMS listings; type, capacity, material, condition, location and stock numbers; no location filter','business_weighted'),
 ('H2','Available chemical plant equipment types','Preserve original seven categories and descriptions; link each hub and IMS search','service_weighted'),
 ('H2','Equipment manufacturers in our inventory','Manufacturers verified on exact IMS detail pages; scope to featured listings','business_weighted'),
 ('H2','Why chemical manufacturers choose IPP for chemical process plants','Preserve five existing benefit labels; source supported values; no generic savings promise','business_weighted'),
 ('H2','What do chemical manufacturers say about IPP? Reviews','Link real company customer video playlist; no invented quote or aggregate rating; distinguish general customer stories','business_weighted'),
 ('H2','How buying from IPP works','Specifications and photos; inspection; purchase; dismantling/relocation; shipping; start-up scope; financing','business_weighted'),
 ('H2','Industries we serve','Preserve six original sectors verbatim as a bare list','business_weighted'),
 ('H2','Sell chemical plants and surplus equipment to IPP','Complete plants, lines and equipment; valuation, decommissioning, dismantling, global marketing; two seller form destinations','business_weighted'),
 ('H2','Global inventory. Local support.','Published warehouses in Eastover, Billingham, Bitterfeld; offices; no location filter','business_weighted'),
 ('H2','Chemical plant projects and industry recognition','BASF, Novartis, CDMO, SOCMA GEO, 2024 ISN announcement and Ross Gale industry coverage; dated claims','business_weighted'),
 ('H2','FAQs','Preserve three key original answers; definition link, price factors, buying, selling, shipping questions','business_weighted'),
 ('H2','Chemical Process Plants Resources','Six relevant resource links; no latest-posts feed','business_weighted'),
 ('H2','Find the right plant or equipment for your project','Contact, phone and inventory destinations','business_weighted'),
]
nodes=[]
for i,(hv,topic,facts,kind) in enumerate(headings):
 nodes.append({'hv':hv,'topic':topic,'from_template':True,'parent_index':None if i==0 else 0,'content_order':i,'section_role':'macro' if i<5 else 'micro','section_class':kind,'carries_prose':True,'content_needed':True,'ai_overview_needed':None if kind=='service_weighted' else False,'assigned_facts':facts,'attribute':facts,'optimized_query_network':'used chemical plant equipment' if kind=='service_weighted' else '', 'answer_type':'definitive','funnel_stage':1 if i<4 else 2 if i<6 else 3 if i<13 else 4,'methodology':'Content type: sourced commercial copy. State each owned attribute once with its value. '+facts,'writing_path_start':'Answer the heading directly using verified IPP evidence.','writing_path_expand':facts,'writing_path_close':'Close with the relevant inventory, source or contact link where useful.','evidence_requirement':'IPP current public pages and user workbook. IMS detail pages govern listing-specific values.'})
save('outline.json',nodes)
job=json.loads((WORK/'job.json').read_text(encoding='utf-8'))
job['verified_facts']={topic:{'values':[facts],'source':'User revised workbook and verified public IPP pages; see ../sources/manifest.json and ../inventory.json'} for _,topic,facts,_ in headings}
job['seo_meta']={'title':'Used Chemical Process Plants for Sale | IPP','description':'Explore used chemical process plants, complete lines and equipment from IPP. View specifications, arrange inspections, or sell your surplus chemical assets.','canonical':'https://internationalprocessplants.com/chemical-process-plant-equipment-used-systems-for-sale/'}
save('job.json',job)
save('segmentation.json',{'context_segments':[{'context':topic,'attributes':facts,'source':'Updated workbook'} for _,topic,facts,_ in headings],'query_dimensions':[],'vector_contexts':[],'page_signals':[],'optimized_query_network':[],'excluded_keywords':[]})
save('review_notes.json',['Draft optimizes existing canonical; user postponed staged before/after approach.','Original category descriptions and three high-value FAQ answers retained.','No exact reviewer sign-off supplied: reviewedBy omitted.','Founding dates inconsistent across public sources: foundingDate omitted.','No competitor URLs supplied; no competitor NLP evidence fabricated.','No search-volume estimates supplied; absent values stay empty.','Redirect directions conflict between manual inputs and tracker: production redirect decisions remain outside this static page build.'])
subprocess.run([sys.executable,str(SKILL/'outline_post.py'),'--work',str(WORK)],check=True)
subprocess.run([sys.executable,str(SKILL/'prepare_job.py'),'--work',str(WORK)],check=True)
