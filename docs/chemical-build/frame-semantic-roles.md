# Frame semantic role labeling: chemical process plants page

Revision of October 8, 2026. Every new or changed sentence on the page is listed with the frame its main predicate evokes (FrameNet names) and its labeled roles. Each sentence carries one subject, one single-verb predicate and one object, so each row reads as a subject-predicate-object triple. Intent follows the page model: **transactional** sentences move a buyer or seller to act; **commercial** sentences help a buyer or seller evaluate IPP before acting.

Preserved original sentences (hero sentence 1, the seven category descriptions, the three original FAQ answers, the company description) keep their wording and are not relabeled here. The locked "How buying from IPP works" steps are also unchanged.

## Hero

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Transactional · buyer | Buying used chemical process plants and equipment from IPP establishes reaction, separation, and heat transfer capacity while sidelining issues like OEM lead times and new-build capital costs. | Intentionally_create (establishes); Avoiding (sidelining); embedded Commerce_buy (buying) | Buyer: implied reader · Goods: used chemical process plants and equipment · Seller: IPP · Created_entity: reaction, separation and heat transfer capacity · Undesirable_situation: OEM lead times, new-build capital costs |
| Transactional · seller | Selling shutdown chemical plants and surplus equipment to IPP converts idle assets into capital while shedding storage, carrying and closure costs. | Cause_change (converts); Removing (shedding); embedded Commerce_sell (selling) | Seller: implied plant owner · Goods: shutdown chemical plants and surplus equipment · Buyer: IPP · Entity: idle assets · Final_category: capital · Theme: storage, carrying and closure costs |
| Commercial · both | 15,000+ pieces of inventory · 20 complete plant sites · 15 countries with offices · Since 1980, supplying process equipment | Quantity / Supply (stat strip) | Supplier: IPP · Quantity: 15,000+, 20, 15 · Time: since 1980 |

## Company intro (reactor hub format, both sides)

Query semantics come first: for "used chemical process plants for sale" the Commerce_sell frame puts **Seller = IPP** in subject position and **Goods = used chemical process plants and equipment** directly after the predicate, then **Buyer = producers**. For seller queries ("sell chemical plant") the Commerce_buy frame keeps **Buyer = IPP** as subject, **Goods = shutdown chemical plants** next, then **Seller = plant owners**. Each paragraph closes on an action role (Sender, Means) for conversion.

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Transactional · buyer | International Process Plants (IPP) sells used chemical process plants and equipment to chemical, petrochemical, fertilizer, polymer, agrochemical and specialty chemical producers worldwide. | Commerce_sell (sells) | Seller: IPP · Goods: used chemical process plants and equipment · Buyer: chemical, petrochemical, fertilizer, polymer, agrochemical and specialty chemical producers · Place: worldwide |
| Commercial · buyer | IPP stocks complete plants, process lines and individual reactors, heat exchangers, centrifuges, dryers, filters, distillation columns and tanks from Pfaudler, De Dietrich, Alfa Laval, Krauss Maffei, Westfalia and other OEM manufacturers. | Storing (stocks) | Agent: IPP · Theme: complete plants, process lines, seven equipment families · Source: OEM manufacturers |
| Commercial · buyer | Purchasing used from IPP can save up to 50% of capital and 90% of lead time versus buying new. | Frugality (save); embedded Commerce_buy | Buyer: implied reader · Seller: IPP · Resource: capital, lead time · Amount: up to 50%, 90% |
| Commercial · both | IPP has supplied process equipment worldwide since 1980. | Supply (has supplied) | Supplier: IPP · Theme: process equipment · Place: worldwide · Time: since 1980 |
| Commercial · both | International Process Plants (IPP) is the world’s largest seller of used process plants and equipment, with 15,000+ pieces of inventory and nearly five decades of experience. (preserved, AI-quoted) | Commerce_sell, nominal (seller) | Seller: IPP · Goods: used process plants and equipment · Degree: world’s largest · Quantity: 15,000+ pieces · Duration: nearly five decades |
| Commercial · both | IPP owns 20 complete process plant sites. | Possession (owns) | Owner: IPP · Possession: 20 complete process plant sites |
| Commercial · buyer | Materials of construction include glass-lined, stainless steel 316, 316L, 304 and 321, Hastelloy C-22 and C-276, titanium, graphite and polypropylene. | Inclusion (include) | Total: materials of construction · Part: the listed materials |
| Commercial · buyer | Capacities range from 2 L (0.5 gal) reactors to 565,000 L (149,258 gal) tanks. | Dimension (range) | Dimension: capacity · Measurement: 2 L to 565,000 L · Object: reactors to tanks |
| Commercial · buyer | Reactor pressure ratings reach 358.7 bar (5,203 psi). | Dimension (reach) | Object: reactors · Dimension: pressure rating · Measurement: up to 358.7 bar |
| Commercial · buyer | Condition options include used, unused, refurbished, re-glassed and new. | Inclusion (include) | Total: condition options · Part: used, unused, refurbished, re-glassed, new |
| Commercial · buyer | IPP offers re-glassed glass-lined equipment through Universal Glasteel Equipment (UGE) and new stainless steel equipment through Gale Process Solutions (GPS). | Offering (offers) | Offerer: IPP · Theme: re-glassed glass-lined and new stainless steel equipment · Means: UGE, GPS |
| Commercial · buyer | IPP’s reactor inventory includes ASME, National Board, CRN, CE and PED coded vessels. | Inclusion (includes) | Total: IPP’s reactor inventory · Part: coded vessels |
| Transactional · seller | IPP buys shutdown chemical plants, idle process lines and surplus equipment from plant owners and asset managers. | Commerce_buy (buys) | Buyer: IPP · Goods: shutdown chemical plants, idle process lines, surplus equipment · Seller: plant owners and asset managers |
| Commercial · seller | IPP values each asset at the seller’s site. | Assessing (values) | Assessor: IPP · Phenomenon: each asset · Place: seller’s site |
| Commercial · seller | IPP handles decommissioning, dismantling and removal. | Taking_care_of (handles) | Agent: IPP · Task: decommissioning, dismantling, removal |
| Transactional · seller | Plant owners start a sale through the sell-a-plant or sell-equipment form. | Activity_start (start); embedded Commerce_sell | Agent / Seller: plant owners · Activity: a sale · Means: seller forms |
| Transactional · buyer | Buyers request specifications, inspections and quotations from IPP’s team. | Request (request) | Speaker / Buyer: buyers · Message: specifications, inspections, quotations · Addressee: IPP’s team |

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

## Revision 4: section openers bound to the page context

Each equipment type, the manufacturers section, the industries section and the advantage cards now open with what IPP supplies, from which makers, to whom and for what process role, then a lead-in and a list, then the values each listing states.

| Intent | Sentence | Frame (predicate) | Roles |
|---|---|---|---|
| Transactional · buyer | IPP supplies used reactors from Pfaudler, De Dietrich, UGE and Gale Process Solutions to chemical producers for batch and continuous synthesis. | Supply (supplies) | Supplier: IPP · Theme: used reactors · Source: listed makers · Recipient: chemical producers · Purpose: batch and continuous synthesis |
| Transactional · buyer | IPP supplies used heat exchangers from Alfa Laval, Vicarb, Ralph Coidan and Graham to chemical plants for heating, cooling and condensing process streams. | Supply (supplies) | Supplier: IPP · Theme: used heat exchangers · Recipient: chemical plants · Purpose: heating, cooling, condensing |
| Transactional · buyer | IPP supplies used centrifuges from Krauss Maffei, Alfa Laval, Westfalia and Sharples to chemical and pharmaceutical plants for solid-liquid separation. | Supply (supplies) | Supplier: IPP · Theme: used centrifuges · Recipient: chemical and pharmaceutical plants · Purpose: solid-liquid separation |
| Transactional · buyer | IPP supplies used dryers from Gale Process Solutions, Glatt, Niro and Pfaudler to chemical plants for removing moisture and solvents from powders, pastes and slurries. | Supply (supplies) | Supplier: IPP · Theme: used dryers · Recipient: chemical plants · Purpose: removing moisture and solvents |
| Transactional · buyer | IPP supplies used filters from Schenk, Cogeim, Chemap and Rosenmund to chemical plants for clarifying liquids and recovering solids. | Supply (supplies) | Supplier: IPP · Theme: used filters · Recipient: chemical plants · Purpose: clarifying liquids, recovering solids |
| Transactional · buyer | IPP supplies used distillation columns from Pfaudler, De Dietrich, Kühni and Schott to chemical plants for solvent recovery and product purification. | Supply (supplies) | Supplier: IPP · Theme: used distillation columns · Recipient: chemical plants · Purpose: solvent recovery, purification |
| Transactional · buyer | IPP supplies used tanks from Pfaudler, De Dietrich, Grundy and Sinclair Stainless Fabrications to chemical plants for raw material storage, blending and product transfer. | Supply (supplies) | Supplier: IPP · Theme: used tanks · Recipient: chemical plants · Purpose: storage, blending, transfer |
| Commercial · buyer | Each reactor listing states capacity, internal pressure, temperature, material and condition (one such sentence per type). | Statement (states) | Speaker: each listing · Message: the listed attributes |
| Commercial · buyer | Chemical producers buy these units to add capacity or replace process units. | Commerce_buy (buy) | Buyer: chemical producers · Goods: these units · Purpose: add capacity, replace process units |
| Commercial · buyer | IPP's chemical process inventory carries reactors, heat exchangers, centrifuges, tanks and columns from the original manufacturers that built them. | Possession (carries) | Owner: IPP's inventory · Possession: equipment families · Source: original manufacturers |
| Transactional · buyer | Buyers search a maker's units directly through IPP's inventory filters. | Seeking (search) | Cognizer_agent: buyers · Sought_entity: a maker's units · Means: inventory filters |
| Transactional · buyer | IPP's sourcing team searches its global network for a maker or model not listed. | Seeking (searches) | Cognizer_agent: IPP's sourcing team · Ground: global network · Sought_entity: unlisted maker or model |
| Commercial · both | IPP's plant listings include formaldehyde, nitric acid, ammonium nitrate, methanol and sodium metabisulfite plants. | Inclusion (include) | Total: IPP's plant listings · Part: five plant types |
| Transactional · seller | Producers in these sectors also sell idle plants and surplus equipment to IPP. | Commerce_sell (sell) | Seller: producers in these sectors · Goods: idle plants, surplus equipment · Buyer: IPP |
| Commercial · both | IPP's chemical plant projects cover both sides of the market. | Inclusion (cover) | Total: IPP's chemical plant projects · Part: both sides of the market |
| Transactional · both | Producers sell plants and sites through IPP, and buyers redeploy those assets in new production. | Commerce_sell (sell); Placing (redeploy) | Seller: producers · Goods: plants and sites · Intermediary: IPP · Agent: buyers · Goal: new production |
| Commercial · buyer | IPP stores units at company-owned warehouses and workshops in South Carolina, England and Germany. | Storing (stores) | Agent: IPP · Theme: units · Location: three company-owned sites |
| Commercial · buyer | IPP arranges international shipping, or buyers arrange their own. | Arranging (arranges) | Agent: IPP or buyers · Theme: international shipping |
| Commercial · buyer | Buyers review photographs, drawings and inspection records before purchase. | Scrutiny (review) | Cognizer: buyers · Ground: photographs, drawings, inspection records · Time: before purchase |
| Transactional · buyer | IPP provides a detailed quote for each stock number on request. | Supply (provides) | Supplier: IPP · Theme: a detailed quote · Recipient: buyer of each stock number · Condition: on request |
