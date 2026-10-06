"""Normalize layout wrappers into semantic content so the skill's Word writer keeps headings/tables."""
from pathlib import Path
from lxml import html,etree
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.build-deps'))
WORK=ROOT/'docs/chemical-build/content'
SKILL=Path.home()/'.agents/skills/anup-commercial-content/scripts'
doc=html.document_fromstring((WORK/'content.html').read_text(encoding='utf-8'))
for node in doc.xpath('//input|//select|//button|//svg|//*[@class="results-header"]|//*[@class="stock-image"]'):
 node.getparent().remove(node)
for node in doc.xpath('//img'):
 node.drop_tag()
for node in doc.xpath('//summary'):node.tag='h3'
for dl in doc.xpath('//dl'):
 table=html.Element('table')
 for row in dl.xpath('./div'):
  tr=html.Element('tr')
  for child in row.xpath('./dt|./dd'):
   cell=html.Element('td');cell.text=child.text_content();tr.append(cell)
  table.append(tr)
 dl.getparent().replace(dl,table)
for a in doc.xpath('//a[h2 or h3 or p or div]'):
 href=a.get('href');a.tag='div';a.attrib.clear()
 p=html.Element('p');link=html.Element('a',href=href);link.text='Source / details';p.append(link);a.append(p)
for node in doc.xpath('//*[@class="manufacturer-links"]'):
 node.tag='ul'
 for a in list(node):
  node.remove(a);li=html.Element('li');li.append(a);node.append(li)
etree.strip_tags(doc,'section','div','article','aside','details','nav')
body=doc.xpath('//body')[0]
clean='\n'.join(html.tostring(n,encoding='unicode') for n in body)
clean='\n'.join(line.rstrip() for line in clean.splitlines()).strip()+'\n'
(WORK/'content.html').write_text(clean,encoding='utf-8')
sys.path.insert(0,str(SKILL))
from build_outputs import build_job
from engine import output_writer
from docx.shared import RGBColor
output_writer.FONT_NAME='Roboto'
job=build_job(str(WORK))
out=ROOT/'docs/chemical-build/deliverables/used-chemical-process-plants-for-sale-content.docx'
word=output_writer._build_docx(job,clean)
for style in word.styles:
 if style.name.startswith('Heading'):
  style.font.name='Montserrat';style.font.color.rgb=RGBColor.from_string('183947')
 elif style.name in ['Normal','List Bullet','List Number']:
  style.font.name='Roboto'
for paragraph in word.paragraphs:
 if paragraph.style.name.startswith('Heading'):
  for run in paragraph.runs:run.font.name='Montserrat'
word.save(out)
print('Semantic Word copy exported:',out.name)
