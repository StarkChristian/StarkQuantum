---
title: Error correction in one page
slug: error-correction-in-one-page
order: 4
script: qec.js
level: Intermediate
published: 2026-10-22
reviewed: 2026-10-22
summary: >-
  Quantum error correction measures a pattern of agreements between qubits, not
  the qubits themselves. If the hardware is good enough, adding more qubits makes
  the protected information better.
check:
  - q: >-
      In the three-qubit bit-flip code, the check on qubits 1 and 2 reports
      "disagree" and the check on qubits 2 and 3 also reports "disagree". Which
      qubit most likely flipped?
    a: >-
      Qubit 2. A flip on qubit 1 would trip only the first check, a flip on
      qubit 3 only the second, and a flip on qubit 2 trips both.
  - q: How many errors is a distance-5 code guaranteed to correct?
    a: >-
      Two. A code of distance $d$ corrects up to $(d-1)/2$ errors.
  - q: >-
      The physical error rate is above the threshold. What happens to the
      logical error rate if you increase the code distance?
    a: >-
      It gets worse. Above threshold, more qubits add more places for errors than
      the code can repair.
sources:
  - name: 'Nielsen and Chuang, Quantum Computation and Quantum Information (Cambridge University Press, 2010)'
    note: Chapter 10 for the three-qubit code and for stabilizer codes.
  - name: 'Gottesman, "An Introduction to Quantum Error Correction", arXiv:quant-ph/0004072'
    url: https://arxiv.org/abs/quant-ph/0004072
    note: How an error is measured without measuring the data.
  - name: 'Fowler, Mariantoni, Martinis and Cleland, "Surface codes: Towards practical large-scale quantum computation", arXiv:1208.0928'
    url: https://arxiv.org/abs/1208.0928
    note: The empirical fit for the logical error rate (equation 11) and a circuit-level threshold of 0.57%.
  - name: 'Wang, Fowler, Stephens and Hollenberg, "Threshold error rates for the toric and surface codes", arXiv:0905.0531'
    url: https://arxiv.org/abs/0905.0531
    note: About 0.78% with imperfect syndrome extraction, for matching-based decoding.
further:
  - title: Overhead calculator
    url: /overhead/
    note: Set an error rate and a target, and see how many qubits one logical qubit costs.
  - title: What a logical qubit actually is
    url: /articles/what-a-logical-qubit-actually-is/
  - title: The decoder has to keep up
    url: /articles/the-decoder-has-to-keep-up/
    note: The classical half of error correction, and its deadline.
  - title: Glossary, surface code
    url: /glossary/#surface-code
---

Classical error correction copies a bit and takes a vote. Quantum information
cannot be copied, and reading a qubit collapses its state. Error correction still
works, by measuring something other than the data.

## A three-qubit example

Take the state $\alpha|0\rangle + \beta|1\rangle$ and encode it across three
qubits as $\alpha|000\rangle + \beta|111\rangle$. This is not three copies. It
is one state spread over three qubits.

Suppose a bit-flip error hits one of them. We do not look at the qubits. We
measure two parities: whether qubits 1 and 2 agree, and whether qubits 2 and 3
agree. Each answer is a single bit, and neither reveals $\alpha$ or $\beta$.

The pair of answers is the syndrome. If only the first check reports a
disagreement, qubit 1 flipped. If only the second does, qubit 3 flipped. If both
do, qubit 2 did. If neither does, nothing is assumed to have happened. The
correction is then a flip of the guilty qubit, and the superposition is
untouched. The code assumes that at most one qubit flipped. If two flipped, the
syndrome points at the wrong qubit and the correction makes the state wrong.

This code handles flips only. Qubits also suffer phase errors, which need a
second set of checks in a different basis. A full code protects against both.

## The surface code

The surface code arranges data qubits on a grid with check qubits between them.
In every round the check qubits measure parities of their neighbours.
The stream of results is the syndrome. A decoder, which is a classical computer,
reads it and decides which errors most likely occurred.

[figure:surface-code]

Try it yourself. Click a data qubit to flip it, and watch which checks light up and which
qubits the decoder flips back. Add random errors until the decoder fails, then run
many trials to see how often each size of code fails.

[figure:playground]

The size of the grid sets the code distance $d$: the smallest number of physical
errors that can change the logical state without being detected. A code of odd
distance $d$ is guaranteed to correct any $(d-1)/2$ errors or fewer. A rotated surface-code patch uses $2d^2-1$ physical qubits:
$d^2$ for data and $d^2-1$ for checks.

## The threshold

Below a threshold error rate, a bigger code is better. The logical error rate
per round is well described by

$$p_L \approx A \left(\frac{p}{p_{\mathrm{th}}}\right)^{(d+1)/2}$$

where $p$ is the physical error rate, $p_{\mathrm{th}}$ is the threshold and $A$ is
a constant found by fitting simulations. Fowler and colleagues fitted
$A \approx 0.03$ with a threshold of 0.57% for their circuit model. The
threshold depends on the noise model and the decoder. The simulation on the
[threshold page](/threshold/) finds about 0.7% for a different noise model, and a
earlier study of matching-based decoding found about 0.78%.

Each step up in distance multiplies the logical error rate by a constant factor
less than one, so it falls exponentially. If $p$ is above the threshold, the same
step makes it worse. The threshold is a sign change.

## The cost

The closer $p$ is to the threshold, the larger $d$ must be to reach a given
target, so the overhead is steep. For a target many orders of magnitude below the
physical rate, the number of physical qubits per logical qubit is of order
a thousand. The [overhead calculator](/overhead/) shows how quickly it climbs
under three published or simulated assumptions.

Two further costs are absent from that formula. The decoder must finish each
round before the next arrives, or the backlog grows. And operations beyond the
cheap gates need magic states, covered in the previous lesson.

## What this tells you

An error-correction result is worth reading for three things: whether the logical
error rate fell as the code grew, how long the run lasted, and what the logical
qubits did. A physical qubit is not a logical qubit, and a logical memory that sits
still is not a computer.
