> **Superseded build scope (October 7, 2026):** The user supplied a revised outline and authorized the complete optimization in one draft. See [the implemented draft and tracker](chemical-build/README.md). The earlier staged/equipment-only proposal below remains historical analysis.

# Chemical equipment landing page: analysis and repository intake

Prepared 7 October 2026. Scope of this first step: analyze the supplied workbook, inspect the existing page and layout reference, and connect the specified repository. The landing page build and production rollout remain subsequent work.

## 1. Recommended page identity

Optimize the existing equipment URL:

`https://internationalprocessplants.com/chemical-process-plant-equipment-used-systems-for-sale/`

Its primary entity is **used chemical process equipment**, with a commercial buying intent. “Plant” qualifies equipment in this page's topic; it does not turn the page into a complete-plant marketplace.

The workbook assigns **used chemical plants for sale** and plant-selling intent to the existing `/sell-shut-down-chemical-processing-plant-assets-with-help-from-ipp/` page. Link to that destination from a short complete-plants block and the full-plants FAQ. Do not create a competing chemical-plants URL for this equipment optimization.

Audience: chemical manufacturers, procurement teams and project teams seeking individual equipment or equipment packages. Market: worldwide supply; the supplied query-volume baseline is US-specific.

Proposed later-release H1: **Used Chemical Process Plant Equipment for Sale**.

Proposed later-release title: **Used Chemical Process Plant Equipment for Sale | IPP**.

The repository copy can show the completed proposed design for review. Production title/H1 edits should remain distinguishable from additive content and defect fixes.

## 2. Workbook reviewed

Source: `C:\Users\dilbd\Downloads\IPP-Chemical-Page-Task-Tracker-2026-10-06.xlsx`.

All 10 tabs were read. The workbook is source material and a proposed implementation plan, not authorization to publish, redirect pages, contact third parties or change accounts.

| Tab | What it contributes |
|---|---|
| Overview | Two-page strategy and R0–R5 release sequencing |
| Redirect plan (paste) | Three proposed source-post merges into the plants page, with a destination decision for the broad complete-plants post |
| Tracker | 53 tasks: 16 equipment-only, 11 plants-only, 18 shared and 8 site-wide |
| Page blueprint | Nine equipment-page blocks and eight plants-page blocks |
| Redirect map | 48 proposed language-specific redirects: three source pages × 16 language versions |
| Internal links | Equipment and plants link acquisition, cross-links, hub links and 60 repointing rows |
| Protect rankings | Existing URL, introductory copy, category order, three FAQ answers and translation protections |
| Baseline | Historical query, visibility, AI-citation and performance measurements |
| Decisions | 12 decisions: 11 open and one answered, concerning IMS plant locations |
| Related articles | Curated guides and proof sources, plus two excluded defect-related articles |

Tracker status is 52 not started and one done. The done row is baseline recording, not implementation. Those statuses were not changed.

The recorded 0.21% CTR, 37 clicks / 17,300 impressions, mobile Lighthouse 29 and ranking/AI-citation figures are supplied historical measurements, not measurements repeated in this session. The workbook's search-update narrative and release dates also require a fresh status check before a production release decision.

## 3. Live page checks performed

The production equipment page was inspected in the browser on 7 October 2026.

| Element | Observed result | Build treatment |
|---|---|---|
| Canonical | Points to the requested existing equipment URL | Preserve |
| Page title | Chemical process plant equipment – used systems for sale | Preserve in baseline; prepare proposed R2 title separately |
| H1 | Same equipment-focused wording as title | Keep equipment intent |
| Meta description | Includes “47 years of experience” | Record legacy wording; resolve founding-year conflict before new copy |
| Contact links | Two body links use `/contact-us/` | Replace with absolute `/contact/` URLs |
| Inventory links | Seven links use `ims.ippe.com` | Use direct verified IMS destinations |
| Section headings | Three H4 headings link to the homepage | Plain H2 headings with correct hierarchy |
| Schema | Article, WebPage, ImageObject, BreadcrumbList, WebSite, Person | Prepare CollectionPage, Organization, BreadcrumbList and evidence-backed ItemList |
| Open Graph | `og:type=article` | Prepare `website` |
| Language fallback | No `x-default` alternate found | Production translation/theme task; preserve existing language URLs |
| Related content | Latest Posts and Share This Story blocks visible | Curated relevant reading and commercial page treatment |
| Full-plants FAQ | Links to `/process-plants-overview/` | Link to the designated commercial plants page |

The link destinations were observed directly. This session did not repeat every external HTTP-status check, translation crawl or site-wide performance audit in the workbook.

## 4. Repository connection

Remote: `https://github.com/access-op-digital/international-process-plants.git`.

Local checkout: `C:\Users\dilbd\OneDrive\Documents\ChatGPT\International process plants\international-process-plants`.

Working branch: `codex/chemical-equipment-optimization`.

Baseline commit: `231cffe` (Restructure for Vercel static deployment).

This is a small static Vercel repository. `vercel.json` publishes `public/`, uses clean URLs and trailing slashes. It has a staging index, an existing `public/buy-used-reactors/index.html` and two reactor research documents. It has no chemical equipment page, build framework, inventory dataset, page generator or repository AGENTS.md.

Proposed implementation path: `public/chemical-process-plant-equipment-used-systems-for-sale/index.html`. This is a new file in staging that represents optimization of the existing production URL, not a new SEO landing-page target.

The generate-landing-page skill points to a different, older `parbatn/IPP` checkout. The explicitly requested `access-op-digital` repository takes precedence. Its chemical page must be hand-maintained unless a small local build process is introduced. Do not run the older all-category generator against this repository or overwrite the reactor page.

The existing reactor draft explicitly labels its palette/fonts as provisional. It is not the brand source. Production WordPress changes, Yoast settings, translated pages, redirects, sitemaps and inbound links cannot be completed merely by editing this static repository.

No changes were pushed, deployed or made to WordPress/IMS during this intake.

## 5. Brand and layout contract

Reference: `https://internationalprocessplants.com/process-equipment/reactor/`.

Values below were read from rendered DOM/computed styles on the live reference, rather than inferred from the repository draft.

| Element | Verified value |
|---|---|
| Heading family | Montserrat, sans-serif |
| Desktop H1 | 40px, weight 600, white |
| Desktop H2 | 35px, weight 600 |
| Desktop H3 | 20px, weight 600 |
| Body family | Roboto, Arial/Helvetica/sans-serif |
| Body size | 16px; inventory interface 15px |
| Main button family | Inter, 15px, weight 700 |
| Main button radius | 5px |
| Main blue | `#1A8FC4` |
| Hero background | `#183947` |
| Hero card background / border | `#2A5263` / `#3C7086` |
| Inventory navy / deep blue | `#18333E` / `#134A62` |
| Inventory surface / rule | `#F4F7F9` / `#E1E7EB` |
| Body text | `#333333`; inventory body `#4A5A63` |
| Navigation | Montserrat, 14px, weight 600, uppercase |
| Logo | IPP's existing dark-blue logo asset |

Follow the reference's white navigation, equipment subnavigation, two-column dark hero, blue quote CTA, outlined inventory CTA, supporting hero cards, inventory sidebar and product grid, grouped content, FAQ treatment and footer. Adapt the inventory controls and spacing for mobile. Use real IPP equipment images with descriptive alt text and fixed dimensions.

Reuse the visual language, not unsupported numerical claims or application advice found in the reference copy. Verified brand values are also saved in `chemical-equipment-brand.json`.

## 6. Entity + associated entities + closed attributes

A closed attribute is a specific value with a source and a clearly bounded subject. For example, a stock number's documented material and capacity are usable; “all equipment is compliant” or “ready to ship” cannot be inferred for every product. Missing values remain internal evidence gaps and are omitted from public claims.

| Entity | Associated entities | Attributes to resolve | Source / boundary |
|---|---|---|---|
| Used chemical process equipment | IPP; seven main categories | Commercial purpose; category set; buying/contact destination | Existing page and workbook |
| Equipment type | Reactors, heat exchangers, centrifuges, dryers, filters, distillation columns, tanks | Type, subtype and hub/IMS link | Keep the seven types in that order; verify destinations |
| Individual equipment item | Manufacturer, model, stock number | Type, condition, material, capacity, units, image, detail URL; ratings only where documented | Current IMS record, with retrieval date |
| Manufacturer | Actual manufacturers represented by records | Exact name and corresponding inventory/filter destination | Do not infer stock or dealership status from a brand mention |
| IPP | Organization; contact; About page | Consistent name, phone, HQ and organization URL | Verify against authoritative IPP pages before schema completion |
| Buying process | Specification package, inspection, purchase, logistics | Required enquiry information; available next step; item-specific scope | Business evidence; no promised delivery/financing/start-up terms without proof |
| New / re-glassed options | Gale Process Solutions; Universal Glasteel Equipment | Exact relationship, equipment scope and company links | Existing IPP links, then current company sources |
| Complete chemical plants | Existing plants page | Separate page destination and buyer/seller intent | One short cross-link block, not duplicate plant inventory |
| Surplus equipment sale | Sell Equipment page | Seller destination | One concise seller line |
| FAQs | Complete plants, inspection, sourcing, buyer questions | Direct answer, scope and next link | Preserve the three protected answers; evidence for added answers |
| Proof | Equipment acquisition; industry coverage | Event, date, source, exact attributed fact | Verify each publication before writing |

Detailed fields and evidence statuses are in `chemical-equipment-entity-attributes.csv`.

## 7. Content skeleton for the build

Use the workbook's Page blueprint as the authored structure. Use the reactor page as the visual reference.

1. Equipment-focused H1, protected opening copy, quote and inventory CTAs.
2. Company introduction with About link and controlled treatment of legacy claims.
3. Seven equipment-category cards in the existing order.
4. Chemical equipment inventory with type, condition, manufacturer and material filters. Cards must exist in HTML, link to real IMS detail pages, and expose only verified summary fields.
5. Manufacturers supported by inventory records and valid destinations.
6. Buying process: specifications, inspection and purchasing/logistics steps that can be evidenced.
7. Short complete-chemical-plants cross-link.
8. Short surplus-equipment seller line.
9. Verified equipment proof, company attribution, protected and new buyer FAQs, and curated chemical-equipment guides.

The listing source is broader than the seven editorial categories: the workbook specifies IMS's Chemical Processing Equipment family plus centrifuges, dryers and filters. Do not label a handful of reactor examples as the full chemical inventory. Any limited demonstration dataset must be explicitly identified as such in review materials and accurately labeled in the UI.

Avoid exact stock-count marketing claims, em dashes, defect-focused content, used-versus-new selection advice, equipment parts outside glass-lined equipment, and newly inferred process-suitability claims. Metric specifications need their imperial counterparts. Use “glass-lined,” and link re-glassed options to UGE.

## 8. Evidence and editorial decisions

- **Protected copy versus unverified claims:** preserve a baseline copy and make proposed edits reviewable. Adding “as of 2026” does not independently verify 15,000+ pieces, 20 sites, 15 countries, “world's largest,” or savings percentages. The workbook's D-04 marks these unresolved. Do not introduce them into new copy/schema as newly verified facts.
- **Founding year:** the workbook records conflicting years/experience statements. Leave a founding date out of new copy/schema until resolved.
- **Named reviewer:** D-02 is open. Use company attribution; do not claim Ross Gale reviewed the new page without evidence of that review.
- **Applications versus sectors:** preserve the existing six-item context for review, but avoid turning it into new claims that specific units suit particular chemical processes. D-05 is open.
- **Financing, start-up support and delivery:** the tracker requests these topics but does not establish exact current terms. Verify the service scope or use a request-to-discuss phrasing.
- **Inventory and manufacturers:** no inventory dataset exists in the requested repository. Current public IMS records or an approved export are needed before factual cards and filters are populated. IMS remains read-only.
- **SERP coverage:** the workbook contains historical keyword baselines, not per-section SERP consensus. No fresh DataForSEO run, AI Overview synthesis or competitor linguistic analysis has been completed during intake. These must not be presented as done.
- **External proof links:** verify the proposed Chemical Engineering replacement, acquisition proof and any credential before use. Do not invent a testimonial or certification.

These evidence gaps do not prevent building a reviewable layout, preparing the outline or implementing static-page corrections.

## 9. Implementation and release boundaries

The workbook proposes R0 fixes, R1 additive content, R2 title/H1/meta changes, R3 redirects, R4 site structure and R5 authority/performance work. It is a staged rollout proposal, not an instruction to execute all 53 tasks in this landing-page build.

The local build should supply a noindex preview at the existing slug, retain the production canonical, document proposed title/H1 changes, use functional responsive inventory controls, and include schema that matches rendered content. Keep analysis files outside `public/` (the repository already excludes docs from Vercel).

A WordPress handoff should separately identify: template/author/share changes, Yoast schema changes, language handling, image replacement, inbound links, original revision IDs and rollback points. Site-wide tag cleanup, sitemap repairs, 48 redirects and repointing 60 posts require their own production execution and verification.

Before completion of the build, check desktop/mobile rendering, keyboard navigation, filters/reset/empty state, contact and detail links, missing images, heading hierarchy, schema syntax/content parity, brand typography, protected copy differences and IPP wording conventions. Report results without claiming production indexing or ranking effects.

## Sources

- User-supplied workbook, all 10 tabs, read 7 October 2026.
- [Existing chemical equipment page](https://internationalprocessplants.com/chemical-process-plant-equipment-used-systems-for-sale/), live browser inspection.
- [Live reactor layout reference](https://internationalprocessplants.com/process-equipment/reactor/), rendered styles and layout inspected.
- [Requested repository](https://github.com/access-op-digital/international-process-plants), cloned and inspected at baseline `231cffe`.
- Requested local skills: `generate-landing-page/SKILL.md` and `anup-commercial-content/SKILL.md`; commercial-content quality baseline and outline/methodology references.
