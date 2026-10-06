# IPP homepage hub

The homepage at `/` replaces the automatic agitator redirect with a directory of 102 page entries across 20 categories. It features the chemical process plants page and includes all 19 existing equipment families.

- Search equipment names and types, combine the search with a category filter, and clear filters from the toolbar or empty state.
- Expand a family's equipment types or use the expand-all control. Every link is rendered in HTML; native disclosures still work without JavaScript.
- The hub reuses IPP's existing Montserrat, Roboto and Inter fonts, navy and blue palette, logo, and a sourced manufacturing-site photograph.
- Existing equipment pages, chemical page copy, and Vercel routing remain unchanged. Review-site noindex settings are preserved.

The directory links to the explicitly routed review edition of the batch-type agitated reactor page, avoiding a duplicate entry for the older page at the subtype folder URL. The equipment overview is linked separately above the directory.

## Files and maintenance

Edit `src/hub-page.html`, `assets/hub/hub.css`, and `assets/hub/hub.js`. Run `python tools/build_page_hub.py` to rebuild `index.html` and `docs/hub/route-manifest.json`. The script reads existing HTML headings and exact Vercel rewrites. It does not regenerate any equipment page.

When adding a new equipment family, add its label, description, and icon to `GROUPS` in the builder. Existing family subtypes are discovered automatically. The generator fails if an unknown family has not been named.

## Verification

Static validation confirms all 111 local link and asset references resolve, 102 unique directory entries, one H1, working fragment targets, and no automatic homepage redirect. `validation.json` records the results. Browser checks cover desktop and mobile layout, search, category filtering, empty-state recovery, disclosures, and the chemical-page link.
