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
- [x] Security headers; Content-Security-Policy in report-only mode
- [x] `llms.txt` and a plain Markdown copy of every essay and brief
- [x] schema.org `Article` data and Google Scholar meta tags on essays
- [x] Cross-document view transitions and hover prefetch

## Next

- [ ] **Enforce the CSP.** Load a preview, open the console, confirm there are
      no violations (search, theme toggle, analytics, MathML), then rename
      `Content-Security-Policy-Report-Only` to `Content-Security-Policy` in
      `pages-config/_headers`.
- [ ] Glossary exclusion list, for common words such as "threshold" that are
      sometimes used in their ordinary sense.
- [ ] A real threshold chart: logical error rate against code distance,
      simulated with Stim and sinter at build time, seed and script in the repo.
- [ ] Overhead calculator: physical error rate and distance in, physical qubits
      per logical qubit out. One small script, no dependencies.
- [ ] Surface-code diagram for "The decoder has to keep up": a patch, one
      error, the syndrome, the decoder's answer.
- [ ] Reality Board history: show each cell's dated changes as a timeline.

## Needs a doctrine decision

- [ ] Replace the copper-and-neon mark with a plain one. Doctrine section 6
      rules out futurist artwork.
- [ ] Learn pages and quizzes. Doctrine section 7 defers them past Wave 1.

## Notes

- Build: `pip install -r requirements.txt && python build.py`, output in `public/`.
- `og/` holds the fonts used to draw link-preview cards. It is read at build
  time and is not published.
- The CSP allows scripts from `umami.homomorphicprivacy.com` and
  `'wasm-unsafe-eval'` (Pagefind). Adding any other third-party script means
  changing it.
