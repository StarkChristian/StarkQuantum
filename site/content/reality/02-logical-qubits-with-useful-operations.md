---
order: 2
question: Logical qubits with useful operations
status: early
status_label: Early
reviewed: 2026-09-08
would_change_it:
  - "A universal logical gate set, including non-Clifford operations, running with error correction active throughout."
  - "Logical error rates that stay flat across a deep sequence of logical gates rather than degrading with circuit depth."
  - "Magic state distillation demonstrated at a cost consistent with published resource estimates rather than far above them."
---

Encoding a logical qubit is not the same as computing with one. This cell asks
whether logical qubits can be entangled, operated on, and kept correct while a
sequence of logical gates runs.

Small numbers of logical qubits have been prepared and operated on, and
entangling operations between them have been demonstrated. The logical error
rates involved are still high, the circuits are short, and the number of logical
qubits is in the tens at most.

The hard part is universality. Clifford operations alone are classically
simulable, so a machine restricted to them cannot outperform a laptop. Getting
past that requires non-Clifford gates, which in most architectures means magic
state distillation, and distillation is where the physical qubit budget goes.
No system has demonstrated a universal logical gate set running under continuous
error correction at a useful error rate.
