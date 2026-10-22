---
title: Why qubits go wrong
slug: why-qubits-go-wrong
order: 2
level: Intro
published: 2026-10-22
reviewed: 2026-10-22
summary: >-
  Every operation on a qubit has a small chance of failing, and a useful
  computation has an enormous number of operations. That arithmetic is the whole
  problem.
check:
  - q: >-
      Each gate fails with probability $10^{-3}$, independently. Roughly how
      likely is a 1,000-gate circuit to run with no error at all?
    a: >-
      About $(1 - 0.001)^{1000} \approx 0.37$, so a little over a third. A
      circuit of ten thousand gates would almost never run clean.
  - q: What do $T_1$ and $T_2$ measure?
    a: >-
      $T_1$ is how long an excited qubit takes to relax to its ground state.
      $T_2$ is how long the phase relationship between $|0\rangle$ and
      $|1\rangle$ survives, and it cannot exceed $2T_1$.
  - q: How does error mitigation differ from error correction?
    a: >-
      Mitigation uses extra runs and post-processing to estimate an average
      result more accurately. It needs no extra qubits and does not protect any
      single run. Correction protects the computation itself, and costs many
      physical qubits per logical qubit.
sources:
  - name: 'Nielsen and Chuang, Quantum Computation and Quantum Information (Cambridge University Press, 2010)'
    note: Chapter 8 for decoherence, and for the definitions of T1 and T2.
  - name: 'Temme, Bravyi and Gambetta, "Error mitigation for short-depth quantum circuits", arXiv:1612.02058'
    url: https://arxiv.org/abs/1612.02058
    note: Zero-noise extrapolation and probabilistic error cancellation, two forms of error mitigation.
  - name: 'IonQ, "Trapped-ion two-qubit gates with >99.99% fidelity without ground-state cooling", arXiv:2510.17286'
    url: https://arxiv.org/abs/2510.17286
    note: A vendor-reported two-qubit gate error of 8.4(7)e-5 on a laboratory prototype, October 2025. Not independently verified.
further:
  - title: When a tooling release is actually news
    url: /articles/when-a-release-is-actually-news/
    note: Why a better compiler changes fidelity without changing the machine.
  - title: Glossary, fidelity
    url: /glossary/#fidelity
  - title: Glossary, error mitigation
    url: /glossary/#mitigation
---

A qubit is a delicate physical system. Anything that disturbs it, even slightly,
changes the state that was meant to carry information.

## Where errors come from

**Decoherence.** The qubit interacts with its surroundings and loses its
quantum character. This happens in two ways. Energy leaks out, so an excited
state decays; the time scale is $T_1$. Or the phase between the two components
drifts, which erases interference without changing which outcome is more likely;
the time scale is $T_2$. A qubit holds its state usefully only for times that are
short compared with $T_1$ and $T_2$.

**Imperfect gates.** A gate is a control pulse of a particular shape and length.
The pulse is never exact, so every gate leaves a small error. Gates that act on
two qubits are harder than gates on one, and are usually the worst operations on
a device.

**Measurement errors.** Reading out a qubit sometimes reports the wrong bit.

**Crosstalk.** Driving one qubit disturbs its neighbours.

## The size of the numbers

Reported error rates for a two-qubit gate differ by platform, by device and by
day, so a number quoted without those three is not comparable with anything. At
the good end, one vendor reported an error of $8.4 \times 10^{-5}$ for a
trapped-ion gate on a laboratory prototype in October 2025. That is the vendor's
own estimate for one gate, not a figure for a commercial machine. For a
commercial device, read the vendor's current calibration data.

Fidelity is the usual way to quote an error. A two-qubit gate fidelity of 99.9%
is usually written as an error of $10^{-3}$, although the exact definition of
fidelity differs between groups. The worked examples in this lesson use
$10^{-3}$ as an illustration. It is not a statement about any particular device.

## Why small errors are not small

Errors multiply. If every operation fails with probability $\epsilon$,
independently, a circuit of $N$ operations runs without any failure with
probability about $(1-\epsilon)^N$.

At $\epsilon = 10^{-3}$ and $N = 1{,}000$ that is about 37%. At $N = 10{,}000$
it is about $0.005\%$. Algorithms for chemistry or cryptography need numbers of
operations in the millions to the trillions. To run them without error, the error
per operation would have to be about one in $N$ or lower, which no physical
qubit achieves.

Better hardware lowers $\epsilon$. Even the best reported rates are far from what
a computation of millions to trillions of operations would need without error
correction.

## Two ways to respond

**Error mitigation** runs the circuit many times, perhaps with deliberately
altered noise, and combines the results to estimate what a noiseless run would
have given. It needs no extra qubits. It works for averages, such as an energy.
For several well-known methods the number of runs needed grows exponentially with
the amount of noise in the circuit. It does not make any single run correct.

**Error correction** encodes each logical qubit across many physical ones and
detects and repairs errors while the computation runs. It does protect the
computation, and it costs a large overhead. The lesson on error correction sets
out how it works.

## What to take from this

When an announcement quotes qubit numbers, the useful question is how many
operations the device can perform before the result is no better than noise.
That depends on the error rate and the circuit, and it is the number that
separates a demonstration from a machine.
