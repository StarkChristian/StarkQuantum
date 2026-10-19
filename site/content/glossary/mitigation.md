---
term: Error mitigation
slug: mitigation
---

Post-processing techniques that reduce the bias noise introduces into an
expectation value, without correcting the underlying errors.

Mitigation is not error correction. It does not protect a computation, and its
sampling cost generally grows exponentially with circuit size, which limits it
to shallow circuits. It is a way to extract more from noisy hardware, not a path
to fault tolerance.
