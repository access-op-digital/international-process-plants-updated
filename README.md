# International Process Plants: equipment landing pages (review site)

Static HTML review site for the IPP equipment landing pages. There is no build step.

## Deploy on Vercel

Import this repository in Vercel with these settings:

| Setting | Value |
|---|---|
| Framework Preset | Other |
| Build Command | (leave empty) |
| Output Directory | `.` (repository root) |
| Install Command | (leave empty) |

What the config files do:

- `vercel.json`: rewrites for the root review URLs (agitator and batch-type reactor pages) and a clean URL for the plate-and-frame pilot (`/equipment/heat-exchanger/plate-and-frame/`); redirects for header and footer links that only exist on internationalprocessplants.com; a site-wide `X-Robots-Tag: noindex, nofollow` header so this review copy never competes with the live site in search.
- `.vercelignore`: keeps internal folders in Git but out of the deployment: `data/`, `docs/`, `tools/`, `meeting-notes/`.

## Folders

| Folder | Contents |
|---|---|
| `equipment/` | The pages, one folder per category (`index.html`, or an `INTERNAL-REVIEW-*.html` draft before approval) |
| `data/` | IMS inventory scrapes per category, the inputs to the page generators |
| `docs/` | Client review documents (Word and markdown) |
| `tools/` | Scrapers and page generators (Python and Node) |
| `meeting-notes/` | Client meeting notes |

## Naming rule

Every file and folder name is lowercase and hyphen-separated, with no spaces or `&`. Vercel URLs are case-sensitive, and spaces or special characters make links fragile.

## Chemical process plants optimization

The chemical plants review is available at `/chemical-process-plant-equipment-used-systems-for-sale/`. Its self-hosted assets are in `assets/chemical/`, and the editable template is `src/chemical-page.html`. See [the implementation and validation notes](docs/chemical-build/README.md) for the source records, issue tracker, content deliverables, and rebuild instructions.
