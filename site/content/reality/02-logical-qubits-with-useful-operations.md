---
order: 2
question: Logical qubits with useful operations
status: early
status_label: Early
reviewed: 2026-11-08
changes:
  - date: 2026-11-08
    note: "Reviewed 8 November, not applied. Three experiments ran non-Clifford operations on logical qubits: fault-tolerant execution of small algorithms with a logical T gate on trapped ions (arXiv:2603.04584), magic state distillation at distances 3 and 5 on neutral atoms (arXiv:2412.15165), and magic state cultivation at distance 3 on a superconducting processor (arXiv:2611.00404). The first is near break-even against unencoded circuits, and the third discards most attempts. None shows error rates that stay flat across deep circuits, or distillation at the cost in published resource estimates. The answer stays Early."
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
