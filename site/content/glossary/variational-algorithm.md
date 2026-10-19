---
term: Variational algorithm
slug: variational-algorithm
aka:
  - "VQE"
  - "QAOA"
---

A hybrid method in which a shallow quantum circuit prepares a state, a classical
optimiser adjusts the circuit's parameters, and the loop repeats.

These were the main hope for useful work on noisy hardware. In practice they are
limited by measurement cost, by optimisation landscapes that flatten as systems
grow, and by noise that biases the result. They remain worth watching and have
not yet beaten good classical methods on a problem anyone has.
