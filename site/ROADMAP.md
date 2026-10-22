# Roadmap

What the site has, what was built in the latest round, and what is deliberately
left for later. The doctrine (`DOCTRINE.md`, version 1.2, in the operator's
folder) wins over this list: nothing here adds advertising, tracking,
monetisation or futurist artwork.

## Built

- Link-preview card per page, MathML formulas, glossary autolinks, in-page outline,
  previous/next, Pagefind search
- Security headers with an enforced Content-Security-Policy
- `llms.txt`, a plain Markdown copy of every page, schema.org and Scholar data
- Cross-document view transitions, hover prefetch
- Flat single-colour mark, with favicons drawn from the same curve
- Learn: six ordered lessons with self-checks
- Overhead calculator at `/overhead/`, with a choice of threshold
- **The threshold, measured** at `/threshold/`: a Stim simulation of surface codes
  of distance 3 to 9, drawn as an SVG chart at build time, with the raw numbers
  at `/threshold.json` and the script in `tools/threshold_sim.py`
- Surface-code figure in the error-correction lesson, with its layout checked
  (four X checks, four Z checks, all commuting) every time the site builds
- Reality Board history: every dated change, across all four cells
- The build fails on a broken internal link or anchor

## Next

- [ ] Rerun the threshold simulation with a second decoder (union-find) and a
      noise model with unequal rates, and show how far the crossing moves
- [ ] A figure for "The decoder has to keep up": syndrome rounds arriving against
      the decoder's deadline
- [ ] Glossary terms for what the lessons introduce: syndrome, code distance,
      Clifford gate, T gate, no-cloning
- [ ] A lesson on reading a resource estimate, once an estimate worth teaching
      from has been reviewed
- [ ] Search filter by type (essay, lesson, brief, glossary)
- [ ] Review the six lessons line by line against sources, and add a `sources`
      list to each

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
