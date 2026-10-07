# Chemical page optimization draft

Built October 7, 2026 on `codex/chemical-process-plants` in the user-requested repository, `access-op-digital/international-process-plants-updated`.

This is a complete **optimization draft for the existing URL**. It is not a published page or a new competing SEO destination. The revised workbook and the user's latest request supersede the earlier equipment-only, staged-update proposal in `docs/chemical-equipment-analysis.md`.

## Revision 2, October 8, 2026: two-sided semantic arrangement

Built with the anup-commercial-content skill in Mode B: the user's Suggested Outline plus the tracker sections already on the page, arranged after the live reactor hub (hero triples, listings, browse by type, makers, advantages, process, industries, FAQ, call to action) and adjusted so the seller path mirrors the buyer path. The outline (73 rows), Context JSON, verified facts, evidence and review notes are in `content/`; generation ran in-session.

- **Intent model.** Every outline row declares its intent: transactional (buy or sell now) or commercial (evaluate first), and buyer, seller or both. See `context.json` and the `intent` field in `outline.json`.
- **Sentence form.** Every sentence is a subject-predicate-object triple with one single verb. `frame-semantic-roles.md` labels each new or changed sentence with its FrameNet frame and roles.
- **Hero.** Adds the seller triple ("Selling shutdown chemical plants and surplus equipment to IPP converts idle assets into capital while shedding storage, carrying and closure costs.") and a stat strip: 15,000+ inventory items, 20 plant sites, 15 countries, since 1980.
- **Equipment types.** Each card adds materials (leading first) and the size range from the IMS type filters, metric with imperial in brackets. IMS publishes no type-level filters for centrifuges and dryers, so those cards state the featured unit's size. Values: `content/ims-facets-2026-10-08.json` and `content/facts.json`.
- **Manufacturers.** The list now names the leading makers by IMS listings (Pfaudler, De Dietrich, Alfa Laval, Krauss Maffei, Westfalia) plus GPS and UGE, each linked to a type-scoped IMS search that renders its listings.
- **Seller path.** "Sell chemical plants and surplus equipment to IPP" moves directly after the buying steps and becomes a four-step path: send the asset information, IPP values the assets, agree the sale structure, decommissioning, dismantling and removal. Facts come from IPP's Sell to IPP, Sell plants and Sell equipment pages and its decommissioning article.
- **Proof.** A fourth project card adds ISN RAVS Plus verification and the Nuol Green Chemistry site transfer.
- **FAQs.** Fourteen: nine buyer (new: new equipment from GPS and UGE) and five seller (new: land and buildings, environmental obligations). "How quickly can IPP assess assets for sale?" was dropped because no published value supports an answer.
- **Call to action.** "Ready to buy or sell chemical plants and equipment?" with contact, phone, email, headquarters address and both seller forms.
- **Unchanged.** H1, URL, canonical, the locked "How buying from IPP works" copy, preserved original sentences and the tabbed resources design.
- **Evidence.** DataForSEO SERP and AI Overview pulls for the seven type rows and the definition FAQ (`content/evidence/`); the reactor query's AI Overview already cites IPP. One query returned a search-engine error.
- **Checks.** Validator 104 checks; IPP page checker 0 issues; section checks leave two accepted exceptions (the locked buying section and the preserved "In addition" FAQ answer), recorded in `content/review_notes.json`.

## Revision, October 8, 2026

Copy was tightened section by section to the reactor page standard: IPP as the explicit subject, one fact per sentence, answer-first FAQs and stated attribute values. The heading outline, the preserved original sentences and the "How buying from IPP works" steps are unchanged.

- Hero: "Buying used chemical process plants and equipment from IPP establishes reaction, separation, and heat transfer capacity while sidelining issues like OEM lead times and new-build capital costs."
- Each category card names makers from IPP's inventory, taken from the IMS manufacturer filters on October 6, 2026.
- Benefit, partner, review, industry, seller and closing copy uses first-party IPP and IMS sources. The savings line uses the approved wording: up to 50% of capital and 90% of lead time.
- FAQs and resources are now one "Chemical Process Plants Resources" section with About Us, FAQs and Blog tabs, following the tabbed resources design the user supplied. The About Us panel adds a company profile beside the team photo from IPP's About page (`assets/chemical/about/ipp-team.webp`, 99 KB). The three preserved FAQ answers are verbatim; the other nine were tightened.
- The tabs are progressive enhancement: without JavaScript all three panels render. `#about-ipp`, `#faqs` and `#blog` open the matching tab.
- Outline node 13 (FAQs) is merged into node 14, so `sections/H013.html` is no longer generated.
- The validator adds tab, FAQ placement, blog card, reviews heading, unchanged buying steps and About photo checks (93 in total). Browser checks are recorded under `revision_2026_10_08` in `browser-validation.json`.
- The Word copy, standalone preview and preview images were regenerated. The preview inlines the current CSS and JavaScript and points at `../../../assets/`; the earlier copy referenced a `public/` folder that no longer exists.
- The manufacturers section still lists the makers of the 14 featured listings. Switching it to the leading inventory makers (Pfaudler, De Dietrich, Alfa Laval) awaits approval.

## Review

- Page: `chemical-process-plant-equipment-used-systems-for-sale/index.html`
- Editable layout/copy: `src/chemical-page.html`
- Presentation and interactions: `assets/chemical/page.css` and `page.js`
- Updated tracker copy: `IPP-Chemical-Optimization-Tracker.xlsx`
- Entity, associated entity and closed attribute values: `entity-associated-entities-closed-attributes.csv`
- Commercial copy and briefs: `deliverables/`
- Sources: `source-log.json`, `merge-sources.json`, `asset-sources.json`, `font-sources.json`, `inventory.json` and `display-inventory.json`
- Structured data: `structured-data.json`
- Automated checks: `validation.json`; browser checks: `browser-validation.json`

The original workbooks in Downloads remain unchanged. All five tabs of the revised workbook were examined, including the tracker, supplied outline, historical baseline and related articles. Original Status values remain unchanged in the tracker copy; the added columns describe work completed in this draft.

## Existing value retained

- The production path and canonical stay `/chemical-process-plant-equipment-used-systems-for-sale/`.
- The opening equipment entity, reactors/heat exchangers/centrifuges and redeployment value remain; first mention expands IPP to its full brand name.
- Both original company-description paragraphs remain, with punctuation corrections and an explicit date/source for the company-wide figures.
- All seven equipment category names, their original order, and their original description sentences remain. Specimen-specific material facts and hub/IMS links add detail without claiming universal materials or suitability.
- The original full-plant, inspection and sourcing FAQ answers remain. The definition answer links to its dedicated guide.
- The original six industry sectors remain; no unapproved sector list was invented.
- The five benefit labels remain. The broad “up to 70%” saving and “operational in weeks” promise were replaced with asset-specific commercial wording, because the supporting company claims do not establish those outcomes for every piece of chemical equipment.
- The H1 follows the revised user outline: “Used Chemical Process Plants for Sale”.

## What was added or fixed

The draft uses the live reactor reference's Montserrat/Roboto/Inter typography, dark navy and blue palette, rounded hero panels, equipment grid, specification labels and restrained footer. The original IPP logo and customer marks are used. The principal action blue is a darker accessible shade within that palette (white-text contrast 4.56:1); the original blue remains an accent. White-lettered customer logos sit on navy.

Six plant and eight equipment listings were read from public IMS detail records on October 7, 2026. Cards are server-rendered, labeled as selected listings, and linked to exact detail pages. Filters work locally for type and, for equipment, material, condition and manufacturer. Stock-number/text search, empty-state recovery, reset, mobile navigation and native FAQ controls work without a backend. All eight manufacturer destination URLs were checked to confirm the requested manufacturer is selected. There is no invented quote form: enquiry, plant-sale and equipment-sale actions use the real IPP destinations.

This is a dated inventory snapshot, not an automatic IMS feed. Confirm availability in IMS before publication and whenever refreshing the page. One source record has no photograph; its card requests photographs instead of using an unrelated plant image. All 13 original inventory photographs are WebP, each below 200 KB; combined photographs are approximately 238 KB. Three self-hosted WOFF2 variable fonts total approximately 129 KB.

Buyer steps, seller content, warehouse locations, linked project evidence, twelve FAQs and six relevant resources complete the supplied outline. Seller themes from the related posts are incorporated, including intact, mothballed and partially dismantled sites. No unsupported closing-speed guarantee, blanket compliance promise or broker comparison was carried over.

The page has CollectionPage, Organization, BreadcrumbList, ItemList and matching FAQPage structured data. It has no Article node, Person author, fabricated review/rating/Offer, author email, reading-time label or share box. Social metadata uses `website`. All contact CTAs use the real `/contact/` path. The old AIChE article was confirmed as a rendered 404 in a browser and omitted; the Chemical Engineering replacement and current privacy policy were checked.

## Decisions requiring facts or production access

These are recorded per row in the tracker; they do not prevent reviewing the complete draft.

- Ross Gale's published commentary is linked. A real review must occur before adding “Reviewed by” or `reviewedBy`. The workbook's proposed byline does not prove he reviewed this draft.
- Conflicting founding dates are not resolved by inventing a founding year. Corporate brand name, HQ, phone and About link are consistent; exact legal-name/founding-date confirmation remains with IPP.
- The manufacturer selection is based on real records, not an unsupported claim about the leading manufacturers. IPP can confirm its preferred featured selection.
- The Manual Inputs tab and tracker disagree about redirect destinations, including seller pages, and the all-industry plant post also has an unresolved destination. No redirects, post unpublishing or sitemap edits were performed.
- Translations, global WordPress author/Yoast settings, sitewide navigation and inbound hub links need CMS work. The repository contains static previews, not the live WordPress theme.
- No Search Console submission, production monitoring, directory listing or outreach was performed.

The staging page deliberately remains `noindex,nofollow` with the **production canonical**. When approved content is transferred to the existing WordPress URL, retain its canonical and replace the staging robots setting with the live page's intended indexable setting. Avoid duplicating the standalone preview header/footer within the CMS body. Replace conflicting Yoast output rather than emitting duplicate schema blocks. No source live page has been changed, so no ranking outcome is claimed.

## Validation and skill notes

The IPP landing-page checker reports zero issues. The repository validator verifies category and FAQ preservation, metadata, structured-data parity, exact IMS link contracts, anchors, asset existence and photo budgets. Browser verification covers desktop and mobile layout, no horizontal overflow, filters, search, reset, menu and FAQ expansion. The contact destination loads its actual form in the browser even though the automated HTTP client received a 403.

The commercial-content skill's template post-pass preserved authored order and assigned nonzero funnel stages. Its “Industries we serve” unhosted-fact note was a matching error: the original six industries appear explicitly. Its question-heading quota is advisory and does not override the user-authored headings.

The only remaining lexical-check exception is **“addition” in the exact retained original FAQ sentence**. This is explicitly accepted to honor the user's preservation requirement; newly written sections passed that lexical check. No padding was added to satisfy length instruments.

Text generation ran in-session. No competitor URLs or search volumes were supplied, and no competitor NLP or volume estimates are claimed. The DataForSEO request first rejected a location string; the corrected request returned an upstream internal search-engine error. No AI Overview or SERP consensus was fabricated. Public first-party IPP and IMS sources govern the page's factual claims.

## Rebuild and preview

With Python and lxml installed:

```powershell
python tools/build_chemical_page.py
python tools/validate_chemical_page.py
python -m http.server 8766 --bind 127.0.0.1 --directory .
```

Open `http://127.0.0.1:8766/chemical-process-plant-equipment-used-systems-for-sale/`.

`build_chemical_page.py` reads the template and the committed source snapshot. Its card facts are deliberately curated and should be reviewed against IMS when refreshed. `prepare_chemical_assets.py`, `collect_chemical_sources.py`, `collect_inventory.py`, `prepare_chemical_fonts.py` and `check_chemical_links.py` perform network reads only. `encode_chemical_images.cjs` requires Sharp and encodes the original photographs without generating or inventing equipment imagery. Raw downloaded HTML and original image caches stay local and are ignored by Git. `finalize_chemical_documents.py` uses the user's local source workbook to create a separate tracker copy and skill export inputs.

No push or deployment was performed.

`export_chemical_copy.py` prepares semantic content for the commercial skill’s Word writer, preserving heading levels and 14 specification tables. It needs python-docx, lxml and BeautifulSoup4 (the missing parser was installed locally into ignored `.build-deps/`, without changing global Python). The final HTML review copy uses the actual IPP page design, replacing the skill’s default agency-branded preview.
