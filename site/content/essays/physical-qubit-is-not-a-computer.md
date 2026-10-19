---
title: A physical qubit is not a computer
slug: physical-qubit-is-not-a-computer
category: foundations
difficulty: Intro
published: 2026-09-08
reviewed: 2026-09-08
living: true
summary: >-
  Qubit count is the number a manufacturer can most easily make go up, and the
  number that tells you least. Here is what the other numbers are, and why
  errors compound faster than registers grow.
footer:
  claim: >-
    A processor holding a large number of physical qubits is a large quantum
    processor. It is not, on that basis, a quantum computer.
  evidence: >-
    Circuit fidelity falls off exponentially with the number of operations.
    At a two-qubit gate error of one in a thousand, a circuit of a few thousand
    gates has already lost most of its signal, regardless of how many qubits
    sit idle on the chip.
  missing_piece: >-
    Error correction that runs continuously and keeps the logical error rate
    falling as the machine grows. Without it, adding qubits adds error faster
    than it adds capability.
  so_what: >-
    Read the fidelity, the coherence time, and the circuit depth before you
    read the qubit count. If an announcement gives you only the count, it has
    told you almost nothing.
sources:
  - name: Preskill, "Quantum Computing in the NISQ era and beyond"
    url: https://arxiv.org/abs/1801.00862
    note: The paper that named the current era and set out its limits.
  - name: DiVincenzo, "The Physical Implementation of Quantum Computation"
    url: https://arxiv.org/abs/quant-ph/0002077
    note: The criteria a physical system must meet to compute at all.
---

Every few months a company announces a processor with more qubits than the last
one. The number goes up, the headline repeats the number, and the reader is
left to assume that capability went up with it. It usually did not.

Qubit count is the easiest number in this field to increase and the least
informative to read. It is a measure of how much hardware exists, not of what
that hardware can do. A processor with a thousand physical qubits and poor gate
fidelity is not more capable than one with fifty good ones. Depending on the
task, it is less capable, because a larger register gives errors more places to
enter.

## What a physical qubit actually is

A physical qubit is a two-level quantum system that a laboratory has learned to
control: a superconducting circuit, a trapped ion, a neutral atom held in an
optical tweezer, a photon, a spin in silicon. It has two states you can call 0
and 1, it can be placed in a superposition of them, and it can be entangled
with its neighbours.

It is also, and this is the part that matters, an object that is trying to stop
being a qubit. It couples to stray fields, to thermal noise, to vibration, to
its own control wiring. Left alone, it decoheres: the quantum information it
held leaks into the environment and becomes classical noise. Coherence time is
how long you have before that happens. Gate fidelity is how accurately you can
manipulate it in the meantime.

So a physical qubit is not a bit. A bit is stable by default and you have to
work to corrupt it. A physical qubit is unstable by default and you have to
work continuously to preserve it.

## The arithmetic that decides everything

Errors in a quantum circuit compound. If each two-qubit gate has a probability
*p* of going wrong, and a circuit uses *n* of them, the chance that nothing went
wrong is roughly (1 − *p*) raised to the power *n*. Multiplication, not
addition.

Take a two-qubit gate error of one in a thousand, which is a good number by the
standards of current hardware and better than much of what is deployed. Run a
circuit with a thousand such gates, and the probability of a clean run is about
0.999 to the power of 1000, which is roughly 37 per cent. Run ten thousand
gates and it is about 0.00005. The circuit still executes. It simply returns
noise.

This is why circuit depth, not qubit count, sets the boundary of what a
processor can do. And it is why the interesting question about any new chip is
not how many qubits it has but what the two-qubit gate error is, how it behaves
when many gates run at once, and how deep a circuit the machine can complete
before its output becomes indistinguishable from a random sample.

Adding qubits does not help with this. It widens the register without extending
how long the register survives. A machine that can hold more information for
the same short window has more room to be wrong in.

## What a demonstration establishes, and what it does not

A demonstration shows that a particular circuit ran on a particular machine on
a particular day and produced a distribution the experimenters could argue was
correct. That is a real result and worth reading. It is not the same as a
computer.

The gap has a specific shape. Demonstrations are usually chosen so that the
hardware's strengths line up with the problem's structure. They frequently rely
on post-selection, discarding runs that failed a check. They are verified by
comparison against a classical simulation, which means the problem was one you
could already solve classically, or by a statistical argument about the shape of
the output rather than a check of an answer. And they are run by the people who
built the machine, who know its quirks.

A computer is different in a way that is easy to state and hard to build. You
hand it to somebody who did not build it. They bring a problem you did not
choose. They get an answer they can trust without knowing the answer in
advance. Nothing available today does that for a problem anyone actually has.

This is a demo, not a machine. The sentence is not dismissive. It is a
description of which of those two things has been produced.

## The number that would change the picture

The way out of the arithmetic above is error correction: spreading one unit of
logical information across many physical qubits, measuring the errors without
measuring the data, and correcting faster than errors accumulate. That is what
a logical qubit is, and it is the subject of the next essay in this series.

The point for now is that error correction changes the exponent. Below a
certain physical error rate — the threshold — adding more physical qubits to a
logical qubit makes the logical error rate fall rather than rise. Above that
threshold, adding qubits makes things worse, and no amount of engineering
enthusiasm changes the sign.

That is the reason qubit count on its own means so little. The same number
means opposite things on either side of the threshold. Ten thousand physical
qubits below threshold is the beginning of a machine. Ten thousand above
threshold is a very expensive noise generator.

## What to read first

When a new processor is announced, the useful order is roughly this. Two-qubit
gate error, measured in a full circuit rather than in isolation. Single-qubit
error. Coherence time relative to gate time, which tells you how many
operations fit inside the window. Connectivity, because gates between distant
qubits cost extra operations and therefore extra error. Measurement fidelity
and reset time, which decide whether error correction can run at all. And then,
last, the qubit count.

If the announcement supplies only the last of those, that is itself the
information: the rest of the numbers were not the story the manufacturer wanted
to tell.
