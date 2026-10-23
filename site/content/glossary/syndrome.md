---
term: Syndrome
slug: syndrome
---

The pattern of parity-check results from one round of error correction. Each
check reports whether a small group of qubits agrees, and together the answers
show where an error probably happened without revealing the information the
qubits store.

A decoder, which is a classical computer, reads the syndrome and infers the most
likely error. The syndrome arrives every cycle for the whole computation, which
is why the decoder has to keep up.
