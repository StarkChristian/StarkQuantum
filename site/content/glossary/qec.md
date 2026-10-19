---
term: QEC
slug: qec
aka:
  - "Quantum error correction"
---

The set of techniques for protecting quantum information without copying it and
without reading it.

Information is spread across many physical qubits so it lives in their
correlations. Parity checks are measured, chosen to reveal where an error
occurred without revealing the stored state. A decoder infers the most likely
error and corrects it. This repeats continuously for the whole computation.
