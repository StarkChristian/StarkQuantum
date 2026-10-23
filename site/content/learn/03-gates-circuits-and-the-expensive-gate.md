---
title: Gates, circuits and the expensive gate
slug: gates-circuits-and-the-expensive-gate
order: 3
level: Intro
published: 2026-10-22
reviewed: 2026-10-22
revisions:
  - date: 2026-10-22
    note: Published.
  - date: 2026-10-22
    note: "Added sources; reflected magic state cultivation; tightened the statements about Clifford circuits and T gates."
summary: >-
  A quantum program is a circuit of gates. Most gates are cheap to run and cheap
  to simulate. The one you need to go beyond that is the one that costs the
  most.
check:
  - q: >-
      A machine can only run Clifford gates, with Pauli measurements. Why can it
      not show an advantage over a classical computer?
    a: >-
      The Gottesman-Knill theorem says such circuits can be simulated
      efficiently on a classical computer, so they cannot do anything a laptop
      cannot.
  - q: What does a transpiler do, and why can it change the quality of a result?
    a: >-
      It rewrites a circuit for a particular device: its native gates and its
      qubit connectivity, adding swaps where qubits are not adjacent. Extra
      two-qubit gates add error, so a better routing gives a better result on
      the same hardware.
  - q: >-
      In a fault-tolerant machine, which kind of gate usually dominates the cost,
      and how is it supplied?
    a: >-
      A non-Clifford gate, such as the T gate. It is usually supplied by
      consuming magic states, which are produced by distillation.
sources:
  - name: 'Nielsen and Chuang, Quantum Computation and Quantum Information (Cambridge University Press, 2010)'
    note: Chapter 4 for the gate set and universality, chapter 10 for fault tolerance.
  - name: 'Gottesman, "The Heisenberg Representation of Quantum Computers", arXiv:quant-ph/9807006'
    url: https://arxiv.org/abs/quant-ph/9807006
    note: The stabilizer formalism behind the Gottesman-Knill theorem.
  - name: 'Bravyi and Gosset, "Improved classical simulation of quantum circuits dominated by Clifford gates", Phys. Rev. Lett. 116, 250501 (2016)'
    url: https://arxiv.org/abs/1601.07601
    note: Classical simulation cost grows exponentially with the number of T gates.
  - name: 'Gidney, Shutty and Jones, "Magic state cultivation: growing T states as cheap as CNOT gates", arXiv:2409.17595'
    url: https://arxiv.org/abs/2409.17595
    note: A 2024 method that reports about an order of magnitude fewer qubit-rounds than distillation for the same quality.
further:
  - title: When a tooling release is actually news
    url: /articles/when-a-release-is-actually-news/
  - title: Glossary, magic state
    url: /glossary/#magic-state
  - title: What a logical qubit actually is
    url: /articles/what-a-logical-qubit-actually-is/
    note: Why universality, not memory, is where the cost sits.
---

A quantum program is a circuit: qubits start in a known state, a sequence of
gates acts on them, and measurements at the end return bits.

## Gates

A gate is a fixed operation on one or two qubits.

- **X** flips $|0\rangle$ and $|1\rangle$, the quantum version of NOT.
- **H**, the Hadamard gate, turns $|0\rangle$ into an equal mix of both
  states. It is how superposition is made.
- **CNOT** flips a second qubit if a first one is $|1\rangle$. Combined with H,
  it creates entanglement.
- **S** and **T** rotate the phase by a quarter and an eighth of a turn.

The circuit has a width, the number of qubits, and a depth, the number of
sequential layers of gates. Depth matters because every layer is another chance
for an error, as the previous lesson showed.

## Compiling

A real device is not a blank slate. It supports a small set of native gates, and
only certain pairs of qubits can interact directly. A compiler, often called a
transpiler, rewrites the circuit to fit. When two qubits that need to interact
are not neighbours, it inserts swaps to move the information.

Each added two-qubit gate carries error. Two compilers can therefore give the
same program different quality on the same machine, and a release that improves
routing is a real change even though the hardware did not move.

## The cheap gates

X, H, S and CNOT belong to a family called the Clifford gates. They have a
useful property: a circuit built only from Clifford gates, starting from simple
states and ending in simple measurements, can be simulated efficiently on an
ordinary computer. This is the Gottesman-Knill theorem.

The consequence is blunt. A machine restricted to these operations cannot show a
computational advantage over a classical computer, however many qubits it has.

## The gate that makes it universal

Adding one more gate, such as T, makes the set universal: with enough gates, any
quantum computation can be approximated to any accuracy. It also removes the
shortcut. The cost of the best known classical simulation methods grows
exponentially with the number of T gates, so circuits with many T gates are
hard to simulate, and that is the regime in which quantum computing might offer
something.

## Why the T gate is expensive

In an error-corrected machine using the surface code, Clifford gates can be
carried out by changing which parities are measured, which needs no special
resource. The T gate has no such shortcut.

The usual method is to prepare a special resource, a magic state, and consume it
to apply the gate. A single good magic state is made by distillation: many
noisy copies go in, one cleaner copy comes out, and the process can be repeated.

In resource estimates made before 2024, distillation factories took up much of
the machine, in qubits and in time. A 2024 method called magic state
cultivation reports about an order of magnitude fewer qubit-rounds for the same
quality, so recent estimates give the factories a smaller share. The T gate is
still the costly operation, and the cost depends on the method assumed. When a
result reports logical qubits doing Clifford operations, it has done the cheap
part.

## What to look for

A claim about a circuit should say how many gates it had, how many were
two-qubit gates, whether it used non-Clifford gates, and how it was compiled.
Without those the claim cannot be compared with another.
