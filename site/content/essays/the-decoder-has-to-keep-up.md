---
title: The decoder has to keep up
slug: the-decoder-has-to-keep-up
category: hardware-and-error
difficulty: Advanced
published: 2026-09-20
reviewed: 2026-09-20
living: false
summary: >-
  Error correction is usually described as a code. In operation it is a
  classical computing problem with a deadline, and the deadline is set by the
  measurement cycle rather than by the physics.
footer:
  claim: >-
    A quantum error-correcting code only works if a classical decoder consumes
    syndrome data at least as fast as the device produces it, for as long as
    the computation runs.
  evidence: >-
    The published below-threshold memory decoded in real time at distance 5
    with an average decoder latency of 63 microseconds against a 1.1
    microsecond cycle time, sustained to a million cycles, and reported rare
    correlated error events roughly once an hour.
  missing_piece: >-
    Sustained real-time decoding at larger code distances, where the syndrome
    volume per cycle grows, and a decoder whose error model survives the
    correlated events that the same experiment observed.
  so_what: >-
    When an error-correction result is announced, ask whether the decoding was
    done live or afterwards on recorded data. The second is a measurement of a
    code. Only the first is a measurement of a machine.
sources:
  - name: "Acharya et al., Quantum error correction below the surface code threshold (Nature 638, 920-926, 2025)"
    url: https://arxiv.org/abs/2408.13687
    note: Source of the hardware and real-time decoder figures quoted here.
  - name: "Fowler et al., Surface codes: towards practical large-scale quantum computation"
    url: https://arxiv.org/abs/1208.0928
    note: The overhead and threshold framing this essay assumes.
  - name: "Pineiro Orioli et al., Optimized Matrix-Product State Simulations of Quantum Error Correction Circuits"
    url: https://arxiv.org/abs/2609.03073
    note: Source of the simulation figures; on simulating these circuits rather than running them.
---

A quantum error-correcting code is usually introduced as mathematics: a
lattice, a set of parity checks, a distance. That description is tidy, and it
leaves out the part that decides whether a machine works. In operation,
error correction is a classical computing problem with a deadline.

The device measures its parity checks over and over. Each round produces a
block of classical bits, the syndrome, and a decoder has to turn that stream
into a statement about which errors most likely occurred. The stream does not
pause while the decoder thinks.

## Two different deadlines

There are two ways for the decoder to fail, and they are worth separating
because they have different fixes.

The first is throughput. If the decoder takes longer to process one round than
the device takes to produce the next one, work accumulates. The queue does not
settle at some larger constant; it grows for as long as the machine runs. This
is why decoding is not a problem you can solve by waiting a bit longer at the
end, and why it gets harder rather than easier as a computation gets longer.

The second is latency, and it binds in fewer places. Much of a fault-tolerant
computation can proceed while decoding lags behind, because Clifford
operations can be tracked as a frame in software and the accumulated
corrections applied later. That trick stops working at a non-Clifford gate,
where the next operation depends on a measurement outcome that has to be
resolved first. At that point the lag becomes a wait, and the machine idles
while the classical side catches up.

So a decoder that is fast enough on average can still be too slow at the
moments that make the computation universal.

## What has been measured

The below-threshold surface code memory reported in 2024 and published in
Nature in 2025 is the useful reference point, because it reports the classical
side rather than only the code.

That work presented two memories below threshold: a distance-7 code, and a
distance-5 code integrated with a real-time decoder. The logical error rate
was suppressed by a factor of 2.14, plus or minus 0.02, for each increase of
two in code distance, and the distance-7 memory reached 0.143 per cent error
per cycle on 101 qubits. It exceeded the lifetime of its best physical qubit
by a factor of 2.4.

The number that matters here is a different one. Decoding in real time, the
team reported an average decoder latency of 63 microseconds at distance 5,
sustained for up to a million cycles, against a cycle time of 1.1
microseconds.

Read those two figures together. The decoder was not keeping pace with each
individual round within that round; it was keeping pace on average across a
long run, with latency absorbed by the frame. A million cycles at 1.1
microseconds is a little over a second of continuous operation. That is a real
result and it is also the scale at which it was demonstrated.

## The mean is the wrong statistic

An average latency is a reassuring number and it is not the one that decides
whether a machine finishes a computation.

Take the throughput condition first, because it has a shape worth being
explicit about. Call the decoder's processing time for one round of syndrome
data t_d, and the device's measurement cycle t_c. If t_d exceeds t_c, then
each round adds t_d minus t_c to the backlog. There is no equilibrium: over a
run of n rounds the queue grows in proportion to n, and the wait before any
outcome can be resolved grows with it. A decoder that is five per cent too
slow does not degrade a computation by five per cent. It fails, eventually,
and the longer the computation the more surely.

Latency behaves differently, and this is where averages mislead. A
non-Clifford gate has to wait for a specific correction to be resolved, so
what matters at that point is not how long decoding usually takes but how long
it takes this time. A decoder with a good mean and a heavy tail will sail
through most of a circuit and stall at the gates that make it universal, which
are also the gates a fault-tolerant algorithm is full of.

So the interesting questions about a reported decoder are which statistic was
reported, and what the distribution looked like behind it. An average latency
with no tail figure describes a component that usually keeps up. Whether it
keeps up when it matters is a different measurement, and the two are easy to
confuse when only one is published.

## Why distance makes it worse

The overhead discussion around error correction usually stops at physical
qubits per logical qubit. The classical side scales too, and less visibly.

Increasing the code distance increases the number of parity checks measured
per round, so the syndrome volume per unit time grows. The decoder's work per
round grows with it, and the data has to be moved off the device and into
whatever is doing the decoding, through wiring that also has to grow. The
throughput deadline is unchanged, because the cycle time is set by the
hardware, not by the decoder's convenience.

This is the sense in which a decoder is part of a machine rather than an
analysis tool attached to one. It has a power budget, a physical location, and
a bandwidth to the device, and those are engineering constraints of the same
kind as coherence time.

## The error model is an assumption

Decoders infer the most likely error given the syndrome, which requires a
model of what errors are likely. The same experiment that reported
below-threshold operation also ran repetition codes to distance 29 and found
performance limited by rare correlated error events occurring roughly once an
hour, or about every three billion cycles.

An event of that kind is not in the independent-noise picture most decoders
assume. It is the sort of thing that sets a floor no amount of additional code
distance removes, because the code is being asked to correct something its
model does not describe. Watching whether that floor moves is more informative
than watching the headline logical error rate.

## Simulating the circuits instead

Running these circuits is expensive, so a good deal of the work happens in
simulation instead, and matrix-product state methods can handle surface code
memory and distillation circuits classically. A result described as a
simulation is a statement about circuits rather than about a device, and the
two get conflated in summary more often than they should.

## What to ask

When an error-correction result appears, three questions separate a code from
a machine.

Was decoding done live, or afterwards on recorded syndrome data? Offline
decoding is a legitimate way to characterise a code and tells you nothing
about whether a machine could run it.

What was the latency and the throughput, against what cycle time, and for how
many cycles? A second of sustained operation and an hour of sustained
operation are different claims.

What error model did the decoder assume, and did the experiment see anything
that model does not cover? The answer to that last one is where the honest
limits usually are.
