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
quantum character. It happens in two ways. Energy leaks out, so an excited state
decays; the time scale is $T_1$. Or the phase between the two components
drifts, which erases interference without changing which state is more likely;
the time scale is $T_2$. A qubit is useful only for a time comparable to or
shorter than these.

**Imperfect gates.** A gate is a control pulse of a particular shape and length.
The pulse is never exact, so every gate leaves a small error. Gates that act on
two qubits are harder than gates on one, and are usually the worst operations on
a device.

**Measurement errors.** Reading out a qubit sometimes reports the wrong bit.

**Crosstalk.** Driving one qubit disturbs its neighbours.

## The size of the numbers

The error per two-qubit gate on current devices is typically somewhere between
a tenth of a percent and a few percent. The best results on small systems are
lower. These figures differ by platform, by device and by date, so a number
quoted without those three is not comparable with anything.

Fidelity is the usual way to quote it. A two-qubit gate fidelity of 99.9% is an
error of $10^{-3}$.

## Why small errors are not small

Errors multiply. If every operation fails with probability $\epsilon$, a circuit
of $N$ operations runs without any failure with probability about
$(1-\epsilon)^N$.

At $\epsilon = 10^{-3}$ and $N = 1{,}000$ that is about 37%. At $N = 10{,}000$
it is about $0.005\%$. The algorithms that matter for chemistry or cryptography
need numbers of operations in the millions to the trillions, and the error rate
would have to be many orders of magnitude lower than any physical qubit
achieves.

Better hardware lowers $\epsilon$. It does not come close to what a long
computation requires.

## Two ways to respond

**Error mitigation** runs the circuit many times, perhaps with deliberately
altered noise, and combines the results to estimate what a noiseless run would
have given. It needs no extra qubits. It works for averages, such as an energy,
and its cost grows quickly with circuit size. It does not make any single run
correct.

**Error correction** encodes each logical qubit across many physical ones and
detects and repairs errors while the computation runs. It does protect the
computation, and it costs a large overhead. The next lesson sets out how it
works.

## What to take from this

When an announcement quotes qubit numbers, the useful question is how many
operations the device can perform before the result is no better than noise.
That depends on the error rate and the circuit, and it is the number that
separates a demonstration from a machine.
