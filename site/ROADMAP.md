# Roadmap

What has been built for the site's reading experience, and what has not. The
doctrine (`DOCTRINE.md` in the operator's folder) wins over this list: nothing
here may add advertising, tracking, monetisation or futurist artwork.

## Done

- [x] Link-preview card per essay and brief (`og:image`, `twitter:card`)
- [x] Formulas as MathML (`$...$`, `$$...$$`), no client script
- [x] First mention of a glossary term links to its definition
- [x] In-essay outline, reading time, previous/next essay
- [x] Full-text search with Pagefind; the JSON index is the fallback
- [x] Security headers and an enforced Content-Security-Policy (checked on a
      preview: search, theme toggle, analytics and Pagefind raised no violations)
- [x] `llms.txt` and a plain Markdown copy of every essay and brief
- [x] schema.org `Article` data and Google Scholar meta tags on essays
- [x] Cross-document view transitions and hover prefetch
- [x] Mobile layout checked at 390 px: no overflow on essay, glossary and home
- [x] Glossary search hits show the term alone, aliases moved below the heading
- [x] Overhead calculator at `/overhead/` (surface-code physical qubits per logical qubit)

## Next

- [ ] A real threshold chart: logical error rate against code distance,
      simulated with Stim and sinter at build time, seed and script in the repo.
- [ ] Surface-code diagram for "The decoder has to keep up": a patch, one
      error, the syndrome, the decoder's answer.
- [ ] More lessons: quantum algorithms (what is and is not believed), and reading
      a hardware spec sheet
- [ ] Reality Board history: show each cell's dated changes as a timeline.

## Decided in doctrine 1.2 (22 October 2026)

- [x] Flat single-colour mark in the accent colour, replacing the copper-and-neon one
- [x] Learn: four ordered lessons with self-check questions at `/learn/`
- Still not built: scored quizzes, capstone, certificates (doctrine section 7)

## Notes

- Build: `pip install -r requirements.txt && python build.py`, output in `public/`.
- `og/` holds the fonts used to draw link-preview cards. It is read at build
  time and is not published.
- The CSP allows scripts from `umami.homomorphicprivacy.com` and
  `'wasm-unsafe-eval'` (Pagefind). Adding any other third-party script means
  changing it.
