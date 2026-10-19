---
title: Matrix-product states simulate a 15-to-1 distillation circuit in under 40 seconds
slug: matrix-product-states-simulate-qec-circuits
published: '2026-09-20'
source_name: arXiv:2609.03073 - Pineiro Orioli et al., Optimized Matrix-Product State
  Simulations of Quantum Error Correction Circuits
source_url: https://arxiv.org/abs/2609.03073
source_type: preprint
entity: ''
numbers:
- 15-to-1 magic state distillation with hundreds of QEC rounds, simulated on 11 logical
  qubits (187 physical qubits) at maximal bond dimension 64, in under 40 seconds
- Rotated surface code memory simulated up to distance 11
- Logical Bell-state preparation simulated up to distance 9
- Bond dimensions and simulation time reduced by several orders of magnitude against
  a naive implementation
limits:
- Classical simulation throughout. No part of this ran on quantum hardware.
- The speed comes from implementation choices the authors optimised, not from the
  method alone; a naive matrix-product-state implementation is reported orders of
  magnitude slower.
- The authors position the method as a complement to near-Clifford simulators, not
  a replacement for them.
example: false
approved_by: christian
corrections: []
---

A matrix-product-state simulator ran a 15-to-1 magic state distillation
circuit with hundreds of error-correction rounds using 11 logical qubits and
187 physical qubits, at a maximal bond dimension of 64, in under 40 seconds,
alongside rotated surface code memory to distance 11 and logical Bell-state
preparation to distance 9. The authors attribute several orders of magnitude
of that gain to implementation choices rather than to the method, which is
the useful part: the cost of simulating these circuits is not fixed, and
published resource estimates inherit whatever assumption was made about it.
None of this ran on hardware. It is a classical simulation of the circuits a
fault-tolerant machine would have to execute, so it constrains resource
estimates rather than saying anything about a device.
