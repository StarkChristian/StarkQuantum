---
order: 1
question: Stable, repeated error correction below threshold
status: early
status_label: Early
reviewed: 2026-11-08
changes:
  - date: 2026-11-08
    note: "Raised 8 November, reviewed 8 November, not applied. A preprint (arXiv:2610.24077) reports below-threshold color-code operation on a trapped-ion processor at distances 3, 5 and 7, with error suppression of about 12 per distance step. That is a second platform, with a suppression factor of about 12 against 2.14 for the earlier surface-code memory (arXiv:2408.13687), but it is a preprint, it uses a different code from the surface code, and the abstract does not report operation over hours. The answer stays Early."
  - date: 2026-09-24
    note: "Raised 20 September, reviewed 24 September, not applied. The published
      below-threshold memory (arXiv:2408.13687) decodes in real time for a million cycles at
      a 1.1 microsecond cycle time, which is about one second of operation on one platform.
      The condition below asks for hours and for a second platform, so the answer stays
      Early."
would_change_it:
  - "Below-threshold operation sustained over hours rather than seconds, with the logical error rate stable throughout."
  - "The same scaling reproduced on a second hardware platform by a group with no stake in the first result."
  - "A margin below threshold wide enough that the physical-to-logical overhead falls substantially rather than marginally."
---

Below threshold means that making an error-correcting code larger makes the
encoded information *better*, not worse. It is the sign change that decides
whether any of this scales.

There is now published work in which increasing the code distance lowered the
logical error rate, on real hardware, over repeated correction cycles. That is
a genuine result and it is why this cell reads early rather than not yet.

What it is not is a solved problem. The demonstrations are short relative to the
duration of a real computation, they run on a small number of logical qubits,
and the margin below threshold is thin enough that the overhead required for a
useful logical error rate remains very large. Sustained operation over the
timescale of an actual algorithm has not been shown.
