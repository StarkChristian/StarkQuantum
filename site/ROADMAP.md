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
- Learn: seven ordered lessons with self-checks, each with sources and a dated
  revision history; lesson 7 covers entanglement with a Bell-pair simulator
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

## Long term (6 to 24 months)

Drawn from an analysis of one conversation: episode 213 of a Persian-language
podcast with Ramis Movassagh, a quantum-computing theorist who has worked at
Google, IBM and IonQ. What the conversation shows about readers: they ask about
instant communication, "quantum consciousness", whether quantum computers will
replace ordinary ones, what Q-Day is, and how the hardware works, and the host
asked more than once for visuals. The guest also made claims the site should check
before anyone repeats them (an exact Q-Day window, speedups for pricing options).
None of it is used as evidence here; it only suggests what readers want.

**Inside the doctrine**
- [ ] *What quantum mechanics does not say*: a lesson or essay on consciousness,
      "manifesting", trying every answer at once, and faster-than-light messages.
      Lesson 7 covers the last one; the rest remain.
- [ ] A library of visual explainers in the style of the Bloch sphere and the
      playground: two-path interference, Grover's amplitude amplification, period
      finding in Shor's algorithm, and a comparison of the hardware approaches.
- [ ] A cryptography evidence page (`/q-day/`): the published resource estimates
      beside the largest demonstrated devices, which cryptosystems Shor's algorithm
      breaks and which it does not, and the status of the post-quantum standards
      (FIPS 203, 204 and 205, published 13 August 2024; the transition draft NIST
      IR 8547, published as an initial draft on 12 November 2024). No dates are
      predicted, in line with the doctrine.
- [ ] Quantum algorithms for finance, with the claims checked: what is known about
      speedups for linear systems and option pricing, and what the input and
      output assumptions cost.
- [ ] The hardware approaches explained from primary papers, with numbers and
      caveats and no ranking of companies: superconducting circuits, trapped ions,
      neutral atoms, photons.
- [ ] A reviewer programme: named experts review lessons, and the claims register
      shows who reviewed what and when.
- [ ] Short animations hosted on this site, with no third-party video embeds.

**Needs a doctrine decision**
- [ ] *Scope beyond computing.* The conversation spends much of its time on
      quantum communication, cryptography and sensing, which the guest says are
      further along. Doctrine section 3 puts quantum key distribution, networks and
      sensing out of scope unless the operator overrides it. A small section limited
      to results with numbers (for example certified deletion, Broadbent and Islam,
      arXiv:1910.03551) would fit if the scope is widened.
- [ ] *A Persian-language edition or glossary.* The conversation is a long argument
      about whether to use English or Persian terms, which shows an audience.
      Doctrine section 1 makes the site English only and bans links to sister
      sites, so any Persian edition would need a deliberate change.
- [ ] *Audio.* Whether the author appears on or runs a podcast, and how that is
      disclosed.

**Outside the site**
- [ ] *A company.* Doctrine section 1 says the publication is not a company and
      does not monetise, and that it has no relationship with any other site the
      author owns. If the author decides to explore a venture, it is a separate
      project: choose a problem, form a separate entity, keep it unlinked from this
      site, and disclose the connection wherever this site discusses that field.
      The site does not take part in it.

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
