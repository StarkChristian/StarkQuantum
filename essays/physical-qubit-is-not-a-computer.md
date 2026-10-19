# A physical qubit is not a computer

*Part of [StarkQuantum](../README.md). Independent notes, no vendor affiliation.*

A headline that says "a new chip with N qubits" describes a component count. It does not describe a computer. This essay explains the gap, so that the next qubit announcement can be read for what it actually shows.

## What a physical qubit is

A physical qubit is a two-level quantum system that can be prepared, manipulated and measured. It can be a superconducting circuit, a trapped ion, a neutral atom held in an optical tweezer, a spin in silicon, or a photon. Each platform has real strengths and real problems.

A single physical qubit can hold a superposition of two states. That is the raw material. It is not yet a unit of reliable computation.

## Why a qubit count says little

The number of qubits on a device is the easiest figure to print and the least informative one. A computer is defined by what it can do correctly, not by how many parts it has. Several other quantities matter at least as much:

- **Error rates.** How often a gate, a measurement or a reset goes wrong. Typical two-qubit gate errors on leading platforms are around 0.1% to 1%, and that is often the best pair on the chip, not the average.
- **Coherence time.** How long the quantum state survives before noise destroys it, compared with how long a gate takes.
- **Connectivity.** Which qubits can interact directly. Poor connectivity forces extra operations, and each extra operation adds error.
- **Crosstalk and drift.** Operating one qubit disturbs its neighbours, and calibrations change over hours and days.
- **Readout quality.** Measurement is often the noisiest operation on the device.
- **Speed.** How many operations per second the whole system can run, including classical control and decoding.

Two devices with the same qubit count can differ by orders of magnitude in what they can compute.

## Noise compounds

A circuit with many gates multiplies the chances of error. If each operation succeeds with probability 99.9%, a circuit of 1,000 operations succeeds with probability of roughly 37% (0.999^1000 ≈ 0.37), before any other error source is counted. Useful algorithms are expected to need millions to trillions of operations. Physical error rates of about 10^-3 are many orders of magnitude away from what that requires.

This is the central problem. It is why error correction exists, and why the next essay, [What a logical qubit is](what-a-logical-qubit-is.md), matters.

## A demo is not a machine

Many published results run a specific circuit on a specific device, once or a few times, and compare the output with a classical computation. This is a legitimate scientific demonstration. It is not the same as a machine that people can use to solve their own problems repeatedly and reliably.

Some questions to separate the two:

1. Was the result repeated on different days and different devices, or shown once?
2. Is the device available to independent users, or only to its builders?
3. Was the benchmark chosen because it is useful, or because it is hard for classical computers and easy to verify?
4. Has the classical baseline been seriously optimised? Several earlier "advantage" claims were later narrowed or removed by better classical algorithms.

## What would count as progress

For physical qubits, real progress looks like:

- Lower two-qubit error rates **across the whole device**, not just the best pair.
- Stable performance over time without constant recalibration.
- Higher speed and better connectivity at the same quality.
- Manufacturing and control that scale without the error rates getting worse.

These are engineering results. They are less exciting than a record qubit count, and they matter more.

## Summary

- A physical qubit is a component.
- A qubit count is not a measure of capability.
- Quality, stability, connectivity and speed decide what a device can do.
- Noise at the physical level is far above what useful algorithms tolerate, which is why error correction is required.

*Next: [What a logical qubit is](what-a-logical-qubit-is.md).*
