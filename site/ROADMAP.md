# Roadmap, version 3

Written 22 October 2026. The aim: a publication that reads like 2026, uses the
platform as it is today, and can show a visitor what it runs on. The doctrine
(`DOCTRINE.md`, version 1.2, in the operator's folder) wins over this list: no
advertising, no tracking, no monetisation, no futurist artwork, English only.

## Built

**Reading**
- Link-preview cards, MathML, glossary links with popover definitions, in-page
  outline, previous/next, a scroll-driven reading bar, Pagefind search that can
  be limited to lessons, essays, briefs or glossary
- OKLCH colour tokens with `light-dark()`, `text-wrap: pretty`, cross-document
  view transitions with a fixed masthead, hover prefetch

**Trust**
- A claims register (`/claims/`): every factual or numerical claim on the Learn
  and tool pages, its source, and what was done with the source
- Sources on every lesson; the calculator and the threshold page cite the
  primary papers and say which constants come from where
- "Cite this" with BibTeX on essays and lessons
- A build that fails on a broken link or anchor, and on any page over 150 KB

**Explainers**
- Learn: six ordered lessons with self-checks, each with sources and a dated
  revision history
- A decoder deadline model (`/decoder/`): cycle time against decoder time and
  parallel decoders, scaled to the latency Google reported for a distance-5 run
- A surface-code playground (distance 3 and 5, exact matching decoder checked
  against PyMatching on 9,000 cases) and a Bloch sphere
- The threshold, measured with Stim, drawn as SVG at build time, with hover
  values, raw data and the script published
- Overhead calculator with three published or simulated models

**Platform**
- Enforced CSP, security headers, `security.txt`, web manifest
- `llms.txt`, a Markdown copy of every page, RSS and JSON Feed, schema.org and
  Scholar metadata
- `/colophon/`: what the site runs on, with page weights measured by the build;
  each page's footer shows its own weight

## Next

**Explainers**
- [ ] Threshold explorer: toggle distances; add a second decoder (union-find) and
      an unequal-noise model and show how far the crossing moves
- [ ] A lesson on reading a resource estimate

**Trust**
- [ ] DOIs for published versions through Zenodo's GitHub integration (needs the
      editor's decision)
- [ ] The editor's review of every lesson, recorded in the claims register

**Platform**
- [ ] Automated audits on every change: Lighthouse, axe (WCAG 2.2 AA) and HTML
      validation (needs GitHub Actions, the editor's decision). A one-off axe
      audit on 23 October 2026 found and fixed one real fault and is recorded on
      the colophon.
- [ ] A manual accessibility pass with a keyboard and a screen reader

## Waiting on the editor

- The glossary entry "Magic state" says distillation dominates the cost in most
  resource estimates. Magic state cultivation (2024) may have changed that.
- Whether the site should say that an AI assistant helped check sources.
- Whether lessons carry the editor's byline until each has been reviewed.

## Not planned, by doctrine

- Scored quizzes, capstone, certificates, any account or stored progress
- Advertising, affiliates, donations, newsletters that sell anything
- Quantum-futurism artwork

## Notes

- Build: `pip install -r requirements.txt && python build.py`, output in `public/`.
  The build needs no simulator; `data/threshold.json` is committed.
- To refresh the chart: `pip install stim sinter pymatching` and
  `python tools/threshold_sim.py`, then rebuild.
- `og/` holds the fonts used to draw link-preview cards. It is read at build
  time and is not published.
- The CSP allows scripts from `umami.homomorphicprivacy.com` and
  `'wasm-unsafe-eval'` (Pagefind). Adding any other third-party script means
  changing it.
- Interactive pieces are written without dependencies, run from files served by
  this site, store nothing, and leave a static figure when script is off.
