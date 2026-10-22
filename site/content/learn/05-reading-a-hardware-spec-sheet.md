---
title: Reading a hardware spec sheet
slug: reading-a-hardware-spec-sheet
order: 5
level: Intermediate
published: 2026-10-22
reviewed: 2026-10-22
summary: >-
  A spec sheet is a list of numbers that look comparable and mostly are not.
  Each one needs a second question about what it was measured on.
check:
  - q: >-
      A spec sheet gives a two-qubit gate fidelity of 99.9%. Name two things that
      number might hide.
    a: >-
      Whether it is the best pair or the median over all pairs, and whether it was
      measured on one gate in isolation or with the whole device running. It may
      also be an average over a particular set of circuits.
  - q: >-
      Why does the ratio of coherence time to gate time matter more than either
      number alone?
    a: >-
      It roughly counts how many operations fit before the qubit loses its state.
      A long coherence time with slow gates can allow fewer operations than a
      shorter one with fast gates.
  - q: >-
      A device is listed as having nearest-neighbour connectivity. What does that
      do to the cost of a circuit?
    a: >-
      Two-qubit gates act only between adjacent qubits, so distant interactions
      need swaps. Each swap is several more two-qubit gates, each carrying error,
      so the same circuit is less accurate than on a fully connected device.
sources:
  - name: 'Google Quantum AI, "Quantum error correction below the surface code threshold", Nature 638, 920 (2025), arXiv:2408.13687'
    url: https://arxiv.org/abs/2408.13687
    note: Reports a mean T1 of 68 microseconds, T2 (CPMG) of 89 microseconds and a CZ gate duration of 42 nanoseconds for its 105-qubit processor.
  - name: 'IBM Quantum documentation, "Processor types"'
    url: https://quantum.cloud.ibm.com/docs/guides/processor-types
    note: Describes IBM's processor families; current error rates are in the backend calibration data.
further:
  - title: How to read a quantum claim
    url: /articles/how-to-read-a-quantum-claim/
    note: The same discipline applied to announcements rather than data sheets.
  - title: Why qubits go wrong
    url: /learn/why-qubits-go-wrong/
  - title: Glossary, fidelity
    url: /glossary/#fidelity
---

A data sheet puts a few headline numbers next to each other. To compare two
machines you need to know what each number means and how it was obtained. The
list below is the one to run down.

## Qubit count

How many qubits does the device have, and how many work? A figure for the chip
is not a figure for the qubits you can use at the quoted quality. Ask how many
meet the stated error rates at the same time. And remember that physical qubits
are not logical qubits.

## Connectivity

Which pairs of qubits can interact directly? Superconducting chips usually connect each qubit only to its
neighbours on a grid. Some trapped-ion devices let any pair in a chain interact,
and neutral-atom arrays can move atoms to bring a pair together. Limited
connectivity means swap gates, and swaps cost accuracy, as the previous lessons
explained.

## Gate error rates

Look for the single-qubit and two-qubit figures separately, because the two-qubit
number is the one that limits you. Then check:

- **Which statistic?** Best pair, median, mean, or worst. A best-pair figure and a median
  figure for the same device can differ, so ask which one is quoted.
- **How measured?** One gate alone, or all gates at once. Gates run together
  disturb each other, so the two figures can differ.
- **Which circuits?** Randomized benchmarking and a full application circuit can
  give different answers.

## Coherence against gate time

$T_1$ and $T_2$ are meaningful only relative to how fast the gates are. The
useful number is roughly $T_2$ divided by the two-qubit gate time: about how many
operations fit before the state is gone. For example, a 2024 paper from Google
Quantum AI reports a mean $T_2$ of 89 microseconds and a controlled-Z gate
duration of 42 nanoseconds on its 105-qubit processor, a ratio of about 2,000.
That is a ratio of two averages, not a count of gates you can run. Platforms
differ by orders of magnitude in both quantities, so neither one compares across
platforms by itself.

## Readout and reset

How often is a measurement wrong, and how long does it take? Error correction
needs fast, accurate readout in the middle of a circuit, and a fast reset. A
device that can only measure at the end of a circuit cannot run an
error-correcting code, because the code has to be measured during the
computation.

## Benchmarks that summarise the device

Several single-number benchmarks exist. Each measures something specific, on
circuits chosen by whoever defined it, and none of them substitutes for the
items above. A benchmark is most useful when two devices are compared under the
same rules and least useful when one number is quoted alone.

## For error correction results

The questions change. How many rounds did it run, and for how long in real time?
What was the code distance, and did the logical error rate fall as the distance
rose? Was the decoder running in real time or applied afterwards? A reader who
asks only about qubit count will miss all of these.

## The habit

For every number, write down what it was measured on, with which statistic, and
whether the same figure is given for the whole device. Most of the time the
answer shows that two apparently equal figures are not.
