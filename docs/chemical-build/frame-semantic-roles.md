# Frame semantic role labeling: chemical process plants page

Revision of October 8, 2026. Every new or changed sentence on the page is listed with the frame its main predicate evokes (FrameNet names) and its labeled roles. Each sentence carries one subject, one single-verb predicate and one object, so each row reads as a subject-predicate-object triple. Intent follows the page model: **transactional** sentences move a buyer or seller to act; **commercial** sentences help a buyer or seller evaluate IPP before acting.

Preserved original sentences (hero sentence 1, the seven category descriptions, the three original FAQ answers, the company description) keep their wording and are not relabeled here. The locked "How buying from IPP works" steps are also unchanged.

## Hero

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Transactional · buyer | Buying used chemical process plants and equipment from IPP establishes reaction, separation, and heat transfer capacity while sidelining issues like OEM lead times and new-build capital costs. | Intentionally_create (establishes); Avoiding (sidelining); embedded Commerce_buy (buying) | Buyer: implied reader · Goods: used chemical process plants and equipment · Seller: IPP · Created_entity: reaction, separation and heat transfer capacity · Undesirable_situation: OEM lead times, new-build capital costs |
| Transactional · seller | Selling shutdown chemical plants and surplus equipment to IPP converts idle assets into capital while shedding storage, carrying and closure costs. | Cause_change (converts); Removing (shedding); embedded Commerce_sell (selling) | Seller: implied plant owner · Goods: shutdown chemical plants and surplus equipment · Buyer: IPP · Entity: idle assets · Final_category: capital · Theme: storage, carrying and closure costs |
| Commercial · both | 15,000+ pieces of inventory · 20 complete plant sites · 15 countries with offices · Since 1980, supplying process equipment | Quantity / Supply (stat strip) | Supplier: IPP · Quantity: 15,000+, 20, 15 · Time: since 1980 |

## Company intro

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Commercial · seller | IPP acquires complete plants, process lines and surplus equipment from producers that restructure their operations. | Getting (acquires) | Recipient: IPP · Theme: complete plants, process lines, surplus equipment · Source: restructuring producers |
| Commercial · buyer | IPP redeploys those assets to manufacturers worldwide. | Placing (redeploys) | Agent: IPP · Theme: those assets · Goal: manufacturers worldwide |
| Commercial · both | IPP has served 160,000+ customers. | Assistance (has served) | Helper: IPP · Benefited_party: 160,000+ customers |

## Equipment types

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Commercial · buyer | IPP stocks used chemical process equipment as individual units and connected systems for reaction, heat transfer, separation, drying, filtration, distillation and storage. | Storing (stocks) | Agent: IPP · Theme: used chemical process equipment · Manner: individual units and connected systems · Purpose: reaction … storage |
| Commercial · buyer | Glass-lined units lead the reactor inventory, alongside stainless steel 316, 316L and 304, Hastelloy C-276 and C-22, and titanium. | First_rank (lead) | Item: glass-lined units · Comparison_set: reactor inventory · Co-members: stainless steel grades, Hastelloy, titanium |
| Commercial · buyer | Reactor capacities range from 2 L to 80,000 L (0.5 to 21,134 gal). | Dimension (range) | Object: reactors · Dimension: capacity · Measurement: 2 L to 80,000 L |
| Commercial · buyer | Stainless steel 316 and graphite lead the heat exchanger inventory, alongside stainless steel 304 and 316L, carbon steel, titanium and Hastelloy C-276. | First_rank (lead) | Item: stainless steel 316, graphite · Comparison_set: heat exchanger inventory |
| Commercial · buyer | Heat transfer areas reach 2,124 m² (22,863 ft²). | Dimension (reach) | Object: heat exchangers · Dimension: heat transfer area · Measurement: up to 2,124 m² |
| Commercial · buyer | Stainless steel 316 and polypropylene lead the filter inventory, alongside stainless steel 304, Hastelloy C-22 and C-276, and carbon steel. | First_rank (lead) | Item: stainless steel 316, polypropylene · Comparison_set: filter inventory |
| Commercial · buyer | Filtration areas reach 330 m² (3,557 ft²). | Dimension (reach) | Object: filters · Dimension: filtration area · Measurement: up to 330 m² |
| Commercial · buyer | Glass-lined and stainless steel 316 columns lead the inventory, alongside stainless steel 304, Hastelloy C-276 and graphite. | First_rank (lead) | Item: glass-lined and stainless steel 316 columns · Comparison_set: column inventory |
| Commercial · buyer | Column diameters range from 76 mm (3 in) to 8,000 mm (315 in). | Dimension (range) | Object: distillation columns · Dimension: diameter · Measurement: 76 mm to 8,000 mm |
| Commercial · buyer | Stainless steel 304 and glass-lined tanks lead the inventory, alongside stainless steel 316 and 316L, carbon steel and fiberglass. | First_rank (lead) | Item: stainless steel 304 and glass-lined tanks · Comparison_set: tank inventory |
| Commercial · buyer | Tank capacities range from 5 L to 565,000 L (1 to 149,258 gal). | Dimension (range) | Object: tanks · Dimension: capacity · Measurement: 5 L to 565,000 L |
| Transactional · buyer | Browse used reactors (and each type) ↗ | Seeking (browse) | Cognizer_agent: buyer · Sought_entity: used units of the type · Ground: IPP inventory |

## Manufacturers

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Commercial · buyer | IPP’s chemical process inventory carries equipment from the manufacturers below. | Possession (carries) | Owner: IPP’s inventory · Possession: equipment · Source: listed manufacturers |
| Transactional · buyer | Each link opens that manufacturer’s listings in IPP’s inventory. | Navigation, no business frame | Theme: manufacturer listings |
| Commercial · buyer | Pfaudler: glass-lined reactors, tanks and agitators (and six more maker labels) | Manufacturing (label) | Manufacturer: Pfaudler · Product: glass-lined reactors, tanks, agitators |

## Why IPP (changed sentence only)

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Commercial · buyer | IPP supplies the records available for each stock number. | Supply (supplies) | Supplier: IPP · Theme: available records · Recipient: buyer of each stock number |

## Seller path

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Transactional · seller | IPP buys complete chemical plants, process lines and individual surplus equipment from shutdown, idled and restructured facilities. | Commerce_buy (buys) | Buyer: IPP · Goods: complete plants, process lines, surplus equipment · Seller: shutdown, idled and restructured facilities |
| Commercial · seller | Its team handles intact, mothballed and partially dismantled plant sites. | Taking_care_of (handles) | Agent: IPP’s team · Task: intact, mothballed, partially dismantled plant sites |
| Commercial · seller | IPP reports that Fortune 100 and Fortune 500 companies typically represent 95% of its sellers. | Statement (reports) | Speaker: IPP · Message: Fortune 100 and 500 companies represent 95% of sellers |
| Transactional · seller | Selling used chemical equipment to IPP replaces piecemeal disposal and ends the seller’s storage and maintenance costs. | Replacing (replaces); Cause_to_end (ends); embedded Commerce_sell | Seller: implied owner · Goods: used chemical equipment · Buyer: IPP · Old: piecemeal disposal · Process: storage and maintenance costs |
| Transactional · seller | Send the asset list, photographs, plant location, available technical documents and removal deadline. | Sending (send) | Sender: seller · Theme: asset list, photographs, location, documents, deadline · Recipient: IPP |
| Transactional · seller | IPP’s forms to sell a plant or sell equipment collect each item. | Gathering_up (collect) | Agent: IPP’s seller forms · Individuals: each item |
| Commercial · seller | IPP reviews the information and inspects the plant site where needed. | Scrutiny (reviews); Inspecting (inspects) | Cognizer / Inspector: IPP · Ground: the information, the plant site |
| Commercial · seller | IPP then values the assets for an outright purchase or for marketing to its global buyer network. | Assessing (values) | Assessor: IPP · Phenomenon: the assets · Purpose: outright purchase or marketing |
| Transactional · seller | IPP buys equipment as-is, where-is, as a principal buyer rather than a broker. | Commerce_buy (buys) | Buyer: IPP · Goods: equipment · Manner: as-is, where-is, principal buyer |
| Commercial · seller | A complete plant sale can include the land, buildings, equipment and intellectual property. | Inclusion (include) | Total: a complete plant sale · Part: land, buildings, equipment, intellectual property |
| Transactional · seller | IPP coordinates plant decommissioning, dismantling, packaging, freight and export. | Arranging (coordinates) | Agent: IPP · Theme: decommissioning, dismantling, packaging, freight, export |
| Commercial · seller | IPP’s team works with the owner’s EHS team on permit closure, emissions compliance and utility shutoffs. | Collaboration (works with) | Partner_1: IPP’s team · Partner_2: owner’s EHS team · Undertaking: permit closure, emissions compliance, utility shutoffs |

## Industries, warehouses, projects

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Commercial · both | IPP buys and supplies chemical plants and process equipment across these sectors. | Commerce_buy (buys); Supply (supplies) | Buyer / Supplier: IPP · Goods: chemical plants and process equipment · Domain: six sectors |
| Commercial · both | IPP stores equipment at company-owned warehouses and workshops in South Carolina, England and Germany. | Storing (stores) | Agent: IPP · Theme: equipment · Location: warehouses in South Carolina, England, Germany |
| Commercial · seller | IPP holds ISN RAVS Plus verification for plant decommissioning. | Possession (holds) | Owner: IPP · Possession: ISN RAVS Plus verification · Domain: plant decommissioning |
| Commercial · seller | IPP enabled the transfer of a shuttered biobased chemicals plant in Minnesota to Nuol Green Chemistry, a deal SOCMA highlighted. | Transfer (transfer); Enabling (enabled) | Enabler: IPP · Theme: shuttered biobased chemicals plant · Place: Minnesota · Recipient: Nuol Green Chemistry · Evaluator: SOCMA |

## FAQs (new and changed answers)

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Commercial · both | IPP answers questions from buyers of second-hand chemical equipment and from sellers of used chemical machinery. | Communication_response (answers) | Speaker: IPP · Trigger: questions · Addressee: buyers and sellers |
| Transactional · buyer | IPP quotes each plant and unit individually. | Commerce_scenario: price quotation (quotes) | Seller: IPP · Goods: each plant and unit · Manner: individually |
| Commercial · buyer | Gale Process Solutions (GPS), an IPP group company, fabricates new stainless steel process equipment with 12 to 16 week average delivery. | Manufacturing (fabricates) | Manufacturer: GPS · Product: new stainless steel process equipment · Duration: 12 to 16 week average delivery |
| Commercial · buyer | Universal Glasteel Equipment (UGE) supplies new and re-glassed glass-lined equipment. | Supply (supplies) | Supplier: UGE · Theme: new and re-glassed glass-lined equipment |
| Transactional · seller | IPP purchases complete plant sites, including the land, buildings, equipment and intellectual property. | Commerce_buy (purchases) | Buyer: IPP · Goods: complete plant sites with land, buildings, equipment, IP |
| Transactional · seller | IPP also buys individual process units and equipment systems within a site. | Commerce_buy (buys) | Buyer: IPP · Goods: process units and equipment systems · Place: within a site |
| Commercial · seller | IPP buys sites with known contamination and assumes site cleanup and regulatory compliance obligations as the buyer. | Commerce_buy (buys); Being_obligated (assumes) | Buyer / Responsible_party: IPP · Goods: contaminated sites · Duty: cleanup and compliance obligations |
| Commercial · seller | IPP’s remediation partners work with local environmental authorities on each site. | Collaboration (work with) | Partner_1: IPP’s remediation partners · Partner_2: local environmental authorities · Place: each site |

## Closing call to action

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Transactional · buyer | Buyers send the process, capacity and destination. | Sending (send) | Sender: buyers · Theme: process, capacity, destination · Recipient: IPP |
| Transactional · buyer | IPP’s sourcing team searches its inventory and the global market for candidate plants and equipment. | Seeking (searches) | Cognizer_agent: IPP’s sourcing team · Ground: inventory and global market · Sought_entity: candidate plants and equipment |
| Transactional · seller | Sellers send the asset list and removal deadline through the sell-a-plant or sell-equipment form. | Sending (send) | Sender: sellers · Theme: asset list, removal deadline · Means: seller forms · Recipient: IPP |
