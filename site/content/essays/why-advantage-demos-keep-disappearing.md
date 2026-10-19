---
title: Why advantage demos keep disappearing
slug: why-advantage-demos-keep-disappearing
category: applications-and-limits
difficulty: Intermediate
published: 2026-09-08
reviewed: 2026-09-08
living: true
summary: >-
  Quantum advantage claims have a habit of shrinking after publication. The
  reason is structural, not scandalous, and understanding it tells you how much
  weight any new claim can carry.
footer:
  claim: >-
    Quantum advantage claims erode because the classical baseline they are
    measured against is an estimate of what is currently known, not a proof of
    what is possible.
  evidence: >-
    Repeatedly, classical simulation costs presented as astronomical have been
    reduced by orders of magnitude once specialists had a concrete target,
    through better tensor-network contraction, smarter use of memory, and
    exploitation of noise in the original experiment.
  missing_piece: >-
    A hardness result. There is no proof that these sampling tasks are
    classically intractable, so every advantage claim is an empirical statement
    about the state of classical algorithms on the day it was made.
  so_what: >-
    Treat an advantage claim as a standing invitation to the classical
    community, and read it again in eighteen months. Advantage on a problem
    somebody actually has would be a different kind of claim entirely.
sources:
  - name: Arute et al., "Quantum supremacy using a programmable superconducting processor"
    url: https://www.nature.com/articles/s41586-019-1666-5
    note: The result that set the pattern for everything since.
  - name: Pan, Chen and Zhang, "Solving the sampling problem of the Sycamore quantum circuits"
    url: https://arxiv.org/abs/2111.03011
    note: One of several classical responses that cut the estimated cost sharply.
---

A pattern has repeated often enough in this field to be worth stating as a
general rule. A laboratory announces that a quantum processor has performed a
task that would take a classical supercomputer an implausible length of time.
Within a year or two, somebody demonstrates the same task classically in far
less time than the announcement estimated. The quantum experiment is not
retracted and was not wrong. The claim built on top of it quietly deflates.

This is not a story about dishonesty. It is a story about what kind of claim an
advantage claim is.

## The claim has two halves, and only one is measured

An advantage result consists of a quantum measurement and a classical estimate.

The quantum half is an experiment. A processor sampled from the output
distribution of a random circuit, or an equivalent task, and the team
characterised how faithfully it did so. That part is measured, on hardware, and
it is generally solid.

The classical half is a projection. Somebody worked out how long the best known
classical algorithm would take on the largest available classical machine, and
extrapolated. This half is not measured. It is a statement about the state of
classical algorithm design at the moment of publication, made by people whose
expertise is in the quantum half.

The advantage is the ratio between those two things. One is an observation, the
other is a forecast about a research community that is about to be given a
target. Ratios of that kind do not age well.

## Why the classical side keeps improving

Three effects show up again and again.

**A concrete target concentrates effort.** Before the announcement, nobody was
optimising a simulator for that exact circuit topology at that exact depth.
Afterwards, a number of very capable groups are. Algorithmic work that was
worth nobody's time becomes worth several people's time, and the constants
improve quickly.

**The simulation problem is usually easier than the general case.** The estimate
often assumes a method that computes the entire output state. But the task is
only to sample from the distribution, or to compute a limited set of
amplitudes, and those are cheaper. Tensor-network contraction with a
well-chosen ordering, slicing the computation to fit in memory, and trading
fidelity for speed all attack the estimate rather than the physics.

**Noise helps the classical side.** A real device's output is not the ideal
distribution but a noisy version of it. A classical simulator only needs to
match the fidelity the hardware actually achieved, not the ideal, and matching a
degraded target is substantially cheaper. The lower the experiment's fidelity,
the more room this leaves.

## Why there is no proof underneath

The deeper issue is that no one has proved these sampling problems are
classically hard. The complexity-theoretic arguments in this area are
conditional: they establish that efficient classical simulation would imply
consequences most theorists believe are false, under assumptions about average-
case hardness that remain conjectural.

So the honest form of an advantage claim is: on this task, with this circuit, at
this fidelity, no classical method known today comes close. That is a real and
interesting statement. It is not a statement about what classical computers can
do, and it is certainly not a permanent one.

The word "supremacy" was chosen to mean something narrow and technical, and it
has been read as something broad and final. The narrow version is defensible.
The broad version was never claimed by the people who did the work.

## What would be different

Advantage on a problem somebody actually has would not have this structure. If a
quantum processor produced a result that a chemist, a materials scientist, or an
engineer wanted for reasons unconnected to quantum computing — a ground state
energy at chemical accuracy for a molecule beyond classical reach, a
correlation function nobody could otherwise obtain — the claim would rest on
usefulness rather than on a comparison. The classical community could still find
a faster route, but the result would remain valuable if they did, because
somebody wanted the answer.

That is the third cell of the Reality Board, and it is why it is written the way
it is: advantage on a scientific or industrial problem someone actually has. The
qualifier is doing all the work. Sampling tasks are chosen for hardness, not
usefulness. Nobody needs the output of a random circuit.

The demonstrations that have been reported are real experiments and they moved
the field. They established that these devices can be characterised at scale and
that their noise behaves roughly as modelled. Those are worth having. But they
established a capability of the hardware, not a use for it.

## How to read the next one

When the next advantage claim appears, note four things and then wait.

Which task, and was it chosen because it is hard classically rather than because
anyone wants the answer. What fidelity was achieved, since a low fidelity gives
the classical side more room. What the classical baseline assumed — which
algorithm, which hardware, and whether it targeted the ideal distribution or the
noisy one. And whether the authors published enough detail for somebody to try
to beat it, which is the strongest signal of confidence available.

Then wait eighteen months. The claims that survive that wait are the ones worth
building an understanding on. Laboratory advantage is not application, and an
advantage that is still standing after the specialists have had a go at it is a
much rarer thing than the announcement volume suggests.
