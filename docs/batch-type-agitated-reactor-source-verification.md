# Source Verification: Batch-Type Agitated Reactor Landing Page

Every sentence and claim on the landing page is verified below with its exact source.

---

## HERO SECTION

### H1
**"Buy Used Batch-Type Agitated Reactors for Sale"**
- Source: This is the target keyword. The equipment category name "Batch-Type Agitated" comes from IPP's own IMS taxonomy at [ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated)

### First Paragraph (Visible Intro)

| Sentence | Source |
|---|---|
| "Buying used batch-type agitated reactors through International Process Plants gives chemical, pharmaceutical, biotech, and specialty manufacturers access to jacketed, agitated reactor vessels from Pfaudler, DeDietrich, Gale Process Solutions, and other OEM manufacturers." | **Manufacturers:** Each product listing on [IMS product detail pages](https://ims.internationalprocessplants.com/inventory/equipment/detail/) shows its Manufacturer field. Pfaudler, DeDietrich, and Gale Process Solutions are the most frequently listed. **"Jacketed, agitated":** IMS category page states "Jacketed and pressure-rated designs." **Industries served:** IMS category page lists pharmaceutical, chemical processing, biotech, food/beverage, cosmetics. |
| "The material of construction includes glass-lined, stainless steel 316, 316L, 304, and 321, Hastelloy C-22, C-276, and C-4, and titanium." | **Source:** The "Material" field on each IMS product detail page. Extracted from all 714 product pages via `all_products.json`. Glass-lined, SS 316, SS 316L, SS 304, SS 321, Hastelloy C-22, C-276, C-4, and Titanium all appear as distinct material values. |
| "Volume capacity ranges from 2 L to 80,000 L (0.5 to 21,150 gallons)." | **Source:** The "Capacity (Design)" field across all 714 IMS product pages. Smallest: 2 L on multiple products. Largest: 80,000 L on [IPP# 222818](https://ims.internationalprocessplants.com/inventory/equipment/detail/222818) (Mechanicca Sarda SS 316L). |
| "Pressure ratings range from 0.5 bar (7.3 psi) to 358.7 bar (5,202 psi)." | **Source:** The "Internal Pressure" field across all 714 IMS product pages. Lowest: 0.5 bar on [IPP# 207104](https://ims.internationalprocessplants.com/inventory/equipment/detail/207104) (DeDietrich CE). Highest: 358.7 bar found across inventory. |
| "Vacuum capability is available across the inventory, with reactors rated for full vacuum operation." | **Source:** The "Internal Full Vacuum" field on IMS product pages. The majority of products show "Internal Full Vacuum: Yes." |

### Expandable Section

| Sentence | Source |
|---|---|
| "IPP stocks Pfaudler reactors across models E, RA, CE, DK, and BE." | **Source:** The "Model" field on Pfaudler product pages in `all_products.json`. Model E (45 listings), RA (34), CE (26), DK (25), BE (24). |
| "DeDietrich reactors are available across models SA, STU, STA, and CE." | **Source:** The "Model" field on DeDietrich product pages in `all_products.json`. Model SA (19 listings), STU (13), STA (9), CE (various). |
| "Gale Process Solutions supplies new stainless steel 316L reactors." | **Source:** IMS product pages for Gale Process Solutions products (e.g., [IPP# 230382](https://ims.internationalprocessplants.com/inventory/equipment/detail/230382)) show Manufacturer: Gale Process Solutions, Condition: New, Material: Stainless Steel 316L. |
| "Universal Glasteel Equipment (UGE) supplies glass-lined units." | **Source:** IMS product pages listing Manufacturer: UGE show Material: Glasslined. Also, [IPP About page](https://internationalprocessplants.com/about/) confirms UGE is a subsidiary. |
| "Condition options include used, re-glassed, new, and unused surplus." | **Source:** The "Condition" field across all 714 IMS product pages shows these distinct values. |
| "Agitation seal types include mechanical seal, packing seal, and double mechanical seal." | **Source:** The "Agitation Seal Type" field across IMS product pages. Three distinct values appear. |
| "Motor power ranges from 0.2 kW (0.3 HP) to 315 kW (422 HP)." | **Source:** The "Motor Power" field across all IMS product pages. Smallest: 0.2 kW. Largest: 315 kW on [IPP# 222818](https://ims.internationalprocessplants.com/inventory/equipment/detail/222818). |
| "Jacket types include half-pipe/limpet, standard jacket, and dimple jacket." | **Source:** The "Jacket Type" field across IMS product pages. Three distinct values appear. |
| "All vessels are ASME-coded, National Board, CRN, CE-marked, or PED compliant, with sanitary and clean-in-place (CIP/SIP) options available." | **Source:** [IMS category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated) — exact quote: "ASME-coded, National Board, CRN, CE-marked, PED compliant vessels" and "Sanitary and clean-in-place (CIP/SIP) options." |
| "IPP states that used equipment systems deliver '50 percent of capital and 90 percent of lead time versus new.'" | **Source:** [IPP homepage](https://internationalprocessplants.com) — exact quote from the homepage about used equipment systems savings. |

### Hero Stats

| Stat | Source |
|---|---|
| "700+ Reactors in Stock" | **Source:** IMS search results show 714 batch-type agitated reactors. Rounded to 700+ to avoid needing updates as inventory changes. Verified via [IMS search](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated). |
| "1980 Established Since" | **Source:** [IPP homepage](https://internationalprocessplants.com) states "47 years of experience" (2026 - 47 ≈ 1979/1980). Also confirmed in the agitators page schema markup: `"foundingDate": "1980"`. |
| "15 Countries with Offices" | **Source:** [IPP About page](https://internationalprocessplants.com/about/) lists 15 countries by name: Brazil, Canada, China, Czech Republic, France, Germany, India, Italy, Mexico, Pakistan, Portugal, Romania, Turkey, United Kingdom, United States. |

---

## PRODUCT CARDS — All 6 Featured Products

Each product card's specifications are sourced from its individual IMS product detail page.

### IPP# 216389 — Pfaudler BE Glass-Lined, 70,100 L
- **Source:** [ims.internationalprocessplants.com/inventory/equipment/detail/216389](https://ims.internationalprocessplants.com/inventory/equipment/detail/216389)
- Manufacturer: Pfaudler | Model: BE | Condition: Used | Material: Glasslined
- Capacity: 70,100 L (18,500 gal) | Internal Pressure: 6 bar (87 psi) | Internal Temperature: 200°C (392°F)
- Internal Full Vacuum: Yes | Motor Power: 43 kW (57.7 HP) | Diameter: 3,750 mm | Straight Side: 5,150 mm
- Agitation Seal Type: Mechanical | Support Type: Legs

### IPP# 207104 — DeDietrich CE Glass-Lined, 54,900 L
- **Source:** [ims.internationalprocessplants.com/inventory/equipment/detail/207104](https://ims.internationalprocessplants.com/inventory/equipment/detail/207104)
- Manufacturer: DeDietrich | Model: CE | Condition: Used | Material: Glasslined
- Capacity: 54,900 L (14,500 gal) | Internal Pressure: 0.5 bar (7.3 psi) | Internal Temperature: 132°C (269.6°F)
- Internal Full Vacuum: Yes | Motor Power: 45 kW (60.3 HP) | Diameter: 3,700 mm | Straight Side: 7,500 mm

### IPP# 101388 — Re-Glassed Pfaudler P, 37.9 L
- **Source:** [ims.internationalprocessplants.com/inventory/equipment/detail/101388](https://ims.internationalprocessplants.com/inventory/equipment/detail/101388)
- Manufacturer: Pfaudler | Model: P | Condition: Re-glassed | Material: Glasslined
- Capacity: 37.9 L (10 gal) | Internal Pressure: 1.72 bar (25 psi) | Internal Temperature: 176.7°C (350°F)
- Internal Full Vacuum: Yes | Diameter: 355.6 mm | Straight Side: 457.2 mm | Support Type: Legs

### IPP# 222818 — Mechanicca Sarda SS 316L, 80,000 L
- **Source:** [ims.internationalprocessplants.com/inventory/equipment/detail/222818](https://ims.internationalprocessplants.com/inventory/equipment/detail/222818)
- Manufacturer: Mechanicca Sarda | Condition: Used | Material: Stainless Steel 316L
- Capacity: 80,000 L (21,150 gal) | Internal Pressure: 21 bar (304.6 psi) | Internal Temperature: 115°C (239°F)
- Internal Full Vacuum: Yes | Motor Power: 315 kW (422.4 HP) | Diameter: 3,900 mm | Straight Side: 5,500 mm
- Agitation Seal Type: Mechanical

### IPP# 230382 — New Gale Process Solutions SS 316L, 15,150 L
- **Source:** [ims.internationalprocessplants.com/inventory/equipment/detail/230382](https://ims.internationalprocessplants.com/inventory/equipment/detail/230382)
- Manufacturer: Gale Process Solutions | Condition: New | Material: Stainless Steel 316L
- Capacity: 15,150 L (4,000 gal) | Internal Pressure: 10 bar (145 psi) | Internal Temperature: 150°C (302°F)
- Internal Full Vacuum: Yes | Motor Power: 22.4 kW (30 HP) | Diameter: 2,450 mm | Straight Side: 3,150 mm
- Agitation Seal Type: Double Mechanical Seal | Impeller Type: Pitch Blade | Support Type: Lugs

### IPP# 108136 — Wilner and Mutter Hastelloy C4, 570 L
- **Source:** [ims.internationalprocessplants.com/inventory/equipment/detail/108136](https://ims.internationalprocessplants.com/inventory/equipment/detail/108136)
- Manufacturer: Wilner and Mutter (Germany) | Condition: Used | Material: Hastelloy - C4
- Capacity: 570 L (150.6 gal) | Internal Pressure: 64 bar (928 psi)
- Motor Power: 7.5 kW (10.1 HP) | Diameter: 800 mm | Straight Side: 1,050 mm
- Agitation Seal Type: Mechanical | Support Type: Lugs

---

## SECTION DESCRIPTIONS

### "By Material" Section Header
| Sentence | Source |
|---|---|
| "IPP stocks batch-type agitated reactors in glass-lined, stainless steel, Hastelloy, and titanium construction." | **Source:** Material field across all IMS product pages — these four material categories are present. |

### Glass-Lined Tab Description
| Sentence | Source |
|---|---|
| "IPP stocks glass-lined batch-type agitated reactors from manufacturers including Pfaudler and DeDietrich." | **Source:** Manufacturer field on glass-lined IMS product pages. |
| "Glass-lined reactors provide corrosion resistance for pharmaceutical, chemical, and specialty manufacturing processes." | **Source:** [IMS category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated) — describes glass-lined as a common material for corrosion resistance in these industries. |
| "Available in used, re-glassed, new, and unused conditions." | **Source:** Condition field on glass-lined IMS product pages shows all four values. |

### Stainless Steel Tab Description
| Sentence | Source |
|---|---|
| "IPP stocks stainless steel batch-type agitated reactors across multiple grades including SS 316, SS Austenitic, SS 316L, SS 304, SS 321, and other grades." | **Source:** Material field on IMS product pages — each grade appears as a distinct value. |
| "Stainless steel reactors serve pharmaceutical, food/beverage, biotech, and chemical processing applications." | **Source:** [IMS category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated) lists these applications. |

### Hastelloy Tab Description
| Sentence | Source |
|---|---|
| "IPP stocks Hastelloy batch-type agitated reactors in C-22, C-276, C-4, and other Hastelloy grades, as well as titanium reactors." | **Source:** Material field on IMS product pages — Hastelloy C22, C276, C4, and Titanium appear as values. |
| "Hastelloy and titanium reactors serve highly corrosive chemical processes where stainless steel and glass-lined construction are insufficient." | **Source:** General industry knowledge about Hastelloy's purpose. Corroborated by the IMS category page listing "Hastelloy and alloys" as a material option for reactors. |

---

## "BY MANUFACTURER" SECTION

### Section Header
| Sentence | Source |
|---|---|
| "IPP stocks batch-type agitated reactors from a wide range of manufacturers." | **Source:** Manufacturer field across IMS product pages shows 154 unique manufacturers. |
| "Buying from the original equipment manufacturer ensures compatibility with your existing plant infrastructure and replacement parts availability." | **Source:** General industry practice. Not a specific IPP claim — this is standard engineering guidance for reactor procurement. |

### Pfaudler Tab
| Sentence | Source |
|---|---|
| "IPP stocks Pfaudler batch-type agitated reactors across all Pfaudler variants — the largest single-manufacturer position in our reactor inventory." | **Source:** Manufacturer field across IMS product pages — Pfaudler (including "Pfaudler (Germany)" and "Pfaudler-Balfour" variants) is the most frequently listed manufacturer. |
| "Pfaudler glass-lined reactors are widely used in pharmaceutical and chemical manufacturing for their corrosion resistance and process reliability." | **Source:** Pfaudler is an industry-recognized glass-lined reactor manufacturer. IMS category page references pharmaceutical and chemical manufacturing as reactor applications. |

### DeDietrich Tab
| Sentence | Source |
|---|---|
| "IPP stocks DeDietrich batch-type agitated reactors across all DeDietrich variants." | **Source:** Manufacturer field on IMS product pages — DeDietrich and "DeDietrich (France)" both appear. |
| "IPP's inventory includes the largest DeDietrich reactor at 54,900 L (14,500 gal)." | **Source:** [IPP# 207104](https://ims.internationalprocessplants.com/inventory/equipment/detail/207104) — Capacity (Design): 54,900 L (14,500 gallons). |

### Gale Process Solutions Tab
| Sentence | Source |
|---|---|
| "IPP stocks Gale Process Solutions (GPS) batch-type agitated reactors." | **Source:** Manufacturer field on IMS product pages shows "Gale Process Solutions." |
| "GPS is an IPP subsidiary that provides custom fabricated equipment with 12–16 week average delivery." | **Source:** [IPP About page](https://internationalprocessplants.com/about/) — describes GPS as providing custom fabricated equipment with "12-16 week average delivery." |

### Other Manufacturers Tab
| Sentence | Source |
|---|---|
| "Beyond Pfaudler, DeDietrich, and Gale Process Solutions, IPP stocks batch-type agitated reactors from many additional manufacturers including UGE, Mechanicca Sarda, Schwelm, Schwelmer, Werkhuizen A Deprest, EHW Thale, Wilner and Mutter, and others." | **Source:** All manufacturer names come from the Manufacturer field on individual IMS product pages in `all_products.json`. |

---

## "BY CONDITION" SECTION

### Used Tab
| Sentence | Source |
|---|---|
| "IPP stocks used batch-type agitated reactors that have been pulled from operating plants." | **Source:** Condition field shows "Used" on IMS product pages. "Pulled from operating plants" is standard industry terminology for used equipment. |
| "Used reactors are available in glass-lined, stainless steel, Hastelloy, and titanium construction from Pfaudler, DeDietrich, and other manufacturers." | **Source:** Filtering `all_products.json` for Condition="Used" shows all four material categories and multiple manufacturers. |

### Re-Glassed Tab
| Sentence | Source |
|---|---|
| "IPP stocks re-glassed batch-type agitated reactors, restored with new borosilicate glass linings on original OEM vessels." | **Source:** Condition field shows "Re-glassed" on IMS product pages. |
| "Re-glassing is performed by IPP's UGE (Universal Glasteel Equipment) division, which stocks 700+ vessels and 2,700+ parts." | **Source:** [IPP About page](https://internationalprocessplants.com/about/) — "Founded 1995; glass-lined steel equipment; stocks 700+ vessels and 2,700+ parts." |

### New & Unused Tab
| Sentence | Source |
|---|---|
| "IPP stocks new and unused batch-type agitated reactors." | **Source:** Condition field shows "New" and "Unused" on IMS product pages. |
| "New reactors include custom-built units from Gale Process Solutions (GPS), IPP's subsidiary that delivers custom fabricated equipment in 12–16 weeks on average." | **Source:** [IPP About page](https://internationalprocessplants.com/about/) — GPS description with delivery timeline. |
| "Unused surplus reactors were manufactured but never installed, offering new-equipment performance with immediate availability." | **Source:** "Unused" is standard industry terminology for manufactured-but-never-installed equipment. |

---

## ADVANTAGES SECTION

| Claim | Source |
|---|---|
| "IPP states that used equipment systems can save '50 percent of capital and 90 percent of lead time versus new.'" | **Source:** [IPP homepage](https://internationalprocessplants.com) — exact quote for used equipment systems. |
| "IPP stocks batch reactors from Pfaudler, DeDietrich, Gale Process Solutions, UGE, and many additional manufacturers." | **Source:** Manufacturer field across IMS product pages. |
| "IPP offers re-glassed reactors through its UGE (Universal Glasteel Equipment) division, founded in 1995, which stocks 700+ vessels and 2,700+ parts." | **Source:** [IPP About page](https://internationalprocessplants.com/about/) — UGE description. |
| "IPP operates from offices in 15 countries." | **Source:** [IPP About page](https://internationalprocessplants.com/about/) — lists 15 countries by name. |
| "IPP has served more than 160,000 customers worldwide." | **Source:** [IPP homepage](https://internationalprocessplants.com) — "more than 160,000 customers worldwide." |
| "Material of construction includes glass-lined, stainless steel, Hastelloy, and titanium." | **Source:** Material field across IMS product pages. |
| "Volume capacity ranges from 2 L to 80,000 L." | **Source:** Capacity field across IMS product pages. |
| "Pressure ratings range from 0.5 to 358.7 bar." | **Source:** Internal Pressure field across IMS product pages. |
| "Motor power ranges from 0.2 to 315 kW." | **Source:** Motor Power field across IMS product pages. |

---

## COMPARISON TABLE (Used vs New)

| Claim | Source |
|---|---|
| "Volume capacity: 2 L to 80,000 L" | **Source:** Capacity field across IMS product pages. |
| "Material of construction: Glass-lined, SS, Hastelloy, titanium" | **Source:** Material field across IMS product pages. |
| "Pressure ratings: 0.5 to 358.7 bar" | **Source:** Internal Pressure field across IMS product pages. |
| "Full vacuum capable units available" | **Source:** Internal Full Vacuum field on IMS product pages. |
| "Mechanical, packing, and double mechanical seals available" | **Source:** Agitation Seal Type field on IMS product pages. |
| "Jacket types: half-pipe/limpet, standard, dimple" | **Source:** Jacket Type field on IMS product pages. |
| "Motor power: 0.2 to 315 kW" | **Source:** Motor Power field across IMS product pages. |

---

## APPLICATION / INDUSTRY CLAIMS

| Claim | Source |
|---|---|
| Pharmaceutical: "blending APIs, crystallization, and temperature-controlled mixing" | **Source:** [IMS category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated) — exact quote. |
| Chemical processing: "polymerization, hydrogenation, and oxidation" | **Source:** [IMS category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated) — exact quote. |
| Biotech: "cell culture, fermentation, and enzyme production" | **Source:** [IMS category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated) — exact quote. |
| Food/beverage: "emulsification and thermal processing" | **Source:** [IMS category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated) — exact quote. |
| Cosmetics: "base mixing and batch formulation" | **Source:** [IMS category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated) — exact quote. |

---

## OTHER REACTOR TYPES SECTION

| Claim | Source |
|---|---|
| "Batch Type Body Only, Tubular, Hydrogenation, Polymerization, Fluid Bed, Fixed Bed" | **Source:** [IMS reactor category page](https://ims.internationalprocessplants.com/inventory/equipment/reactor) — lists all 7 reactor subcategories. |

---

## COMPANY FACTS USED THROUGHOUT

| Fact | Source |
|---|---|
| Founded 1980 | [IPP homepage](https://internationalprocessplants.com): "47 years of experience" + agitators page schema `"foundingDate": "1980"` |
| 15 countries with offices | [IPP About page](https://internationalprocessplants.com/about/): lists 15 countries by name |
| 15,000+ equipment pieces | [IPP homepage](https://internationalprocessplants.com): "15,000 process systems and major equipment pieces" |
| 160,000+ customers | [IPP homepage](https://internationalprocessplants.com): "more than 160,000 customers worldwide" |
| Nearly 150 colleagues | [IPP homepage](https://internationalprocessplants.com): "nearly 150 colleagues around the world" |
| Gale Process Solutions (GPS) subsidiary | [IPP About page](https://internationalprocessplants.com/about/) |
| GPS: 12-16 week average delivery | [IPP About page](https://internationalprocessplants.com/about/) |
| Universal Glasteel Equipment (UGE) subsidiary | [IPP About page](https://internationalprocessplants.com/about/) |
| UGE: founded 1995, 700+ vessels, 2,700+ parts | [IPP About page](https://internationalprocessplants.com/about/) |
| Savings: "50 percent of capital and 90 percent of lead time versus new" | [IPP homepage](https://internationalprocessplants.com): exact quote for used equipment systems |
| USA phone: +1 609-586-8004 | [IPP homepage](https://internationalprocessplants.com) |
| UK phone: +44-1642-367910 | [IPP homepage](https://internationalprocessplants.com) |

---

## WHAT IS NOT ON THIS PAGE (Deliberately Omitted)

- No fabricated testimonials or case studies
- No unverified delivery timelines (only GPS's "12-16 week" from IPP About page)
- No inspection/testing process claims beyond what IPP states
- No cost savings percentages beyond IPP's own exact quote
- No warranty or guarantee claims
- No specific product counts (removed to avoid going stale as inventory changes)

---

## SOURCE URLS REFERENCED

1. **IMS Category Page:** https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-agitated
2. **IMS Reactor Category:** https://ims.internationalprocessplants.com/inventory/equipment/reactor
3. **IPP Homepage:** https://internationalprocessplants.com
4. **IPP About Page:** https://internationalprocessplants.com/about/
5. **IPP# 216389:** https://ims.internationalprocessplants.com/inventory/equipment/detail/216389
6. **IPP# 207104:** https://ims.internationalprocessplants.com/inventory/equipment/detail/207104
7. **IPP# 101388:** https://ims.internationalprocessplants.com/inventory/equipment/detail/101388
8. **IPP# 222818:** https://ims.internationalprocessplants.com/inventory/equipment/detail/222818
9. **IPP# 230382:** https://ims.internationalprocessplants.com/inventory/equipment/detail/230382
10. **IPP# 108136:** https://ims.internationalprocessplants.com/inventory/equipment/detail/108136
11. **Product Data (all 714 pages):** Extracted via `all_products.json` — scraped directly from IMS product detail pages using Puppeteer + Python on 2026-03-23
