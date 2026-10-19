---
title: What a logical qubit actually is
slug: what-a-logical-qubit-actually-is
category: foundations
difficulty: Intermediate
published: 2026-09-08
reviewed: 2026-09-08
living: true
summary: >-
  The word “logical qubit” is now used for at least four different things,
  only one of which is the thing that matters. This is how to tell which one an
  announcement means.
footer:
  claim: >-
    A logical qubit is one unit of protected quantum information encoded across
    many physical qubits, with errors detected and corrected continuously while
    the computation runs.
  evidence: >-
    Codes such as the surface code have known thresholds and known overheads.
    Below threshold, adding physical qubits to a logical qubit lowers the
    logical error rate; above it, the same addition raises it.
  missing_piece: >-
    Sustained operation. A logical qubit that survives idle is not the same as
    one that survives a long sequence of logical gates, including the
    non-Clifford operations that make a computation universal.
  so_what: >-
    When a company reports logical qubits, ask three questions: what is the
    logical error rate, does it fall as the code grows, and did the qubits do
    anything besides exist.
sources:
  - name: Fowler et al., "Surface codes - towards practical large-scale quantum computation"
    url: https://arxiv.org/abs/1208.0928
    note: The standard reference on the surface code, its threshold, and its cost.
  - name: Gottesman, "An Introduction to Quantum Error Correction"
    url: https://arxiv.org/abs/quant-ph/0004072
    note: How you measure an error without measuring the data.
---

"Logical qubit" has become the field's most abused phrase. It appears in
roadmaps, in funding announcements, and in headlines, attached to numbers that
are not comparable with each other. Some of those numbers describe a genuine
piece of protected memory. Some describe an encoded state that was prepared,
looked at, and discarded. The word is the same in both cases.

The distinction is worth learning, because it is the difference between
hardware that is on the path to a machine and hardware that is demonstrating a
component of one.

## The problem error correction solves

Classical error correction is straightforward: copy the bit three times, read
all three, take the majority. Quantum information forbids both halves of that.
You cannot copy an unknown quantum state, and reading a qubit destroys the
superposition you were trying to protect.

The way around it is indirect. Encode one logical qubit across many physical
qubits so that the information lives in the correlations between them rather
than in any single one. Then measure not the data but a set of parities
— whether neighbouring qubits agree — chosen so that the answers reveal where
an error occurred without revealing what state is stored. Those answers are the
syndrome. A decoder reads the syndrome, infers which error most likely occurred,
and applies the correction.

This has to happen repeatedly, faster than errors accumulate, for the entire
duration of the computation. Error correction is not a step you run at the end.
It is a process the machine performs continuously, in the background, forever,
while also doing the actual computation.

## The threshold, and why it is the whole game

Codes have a threshold: a physical error rate below which the scheme works.
Below threshold, making the code larger — adding more physical qubits per
logical qubit — makes the logical error rate fall, and it falls fast, roughly
exponentially in the code distance. Above threshold, making the code larger
makes things worse, because you have added more places for errors to appear
than the code can fix.

The threshold is therefore a sign change, not a gradient. It is the reason
"below threshold" is the phrase to look for in any error-correction result and
"we added more qubits" is not.

For the surface code, the most studied family, the threshold sits around one per
cent per operation, with the exact figure depending on the noise model and the
decoder. Real hardware has to be comfortably below that, not marginally, because
the overhead required to reach a useful logical error rate grows sharply as you
approach the threshold from below.

That overhead is large. Reaching logical error rates low enough for a long
computation typically requires something on the order of a thousand physical
qubits per logical qubit, and under pessimistic assumptions considerably more.
This is why a chip with a few thousand physical qubits does not correspond to a
few thousand logical ones, and why the ratio, rather than either number alone,
is the thing to track.

Newer code families, particularly quantum low-density parity-check codes,
promise better ratios by giving up the surface code's convenient
nearest-neighbour layout. They require connectivity that most hardware does not
have. Whether that trade is winnable on real machines is one of the open
questions this site follows.

## Four things called a logical qubit

When an announcement reports logical qubits, it is usually reporting one of
these, and they are not equivalent.

**An encoded state that was prepared and measured.** The team encoded a logical
state, verified it looked right, and stopped. This shows the encoding works. It
says nothing about whether the state survives.

**A logical memory that beat its physical parts.** The encoded qubit held
information longer, or with lower error, than the best single physical qubit in
the same device. This is a real milestone and the first genuine evidence that
correction is doing work.

**A logical memory that improves as the code grows.** Increasing the code
distance lowered the logical error rate. This is the below-threshold result, and
it is the one that matters most, because it is the only one that implies the
approach scales.

**Logical qubits performing logical operations.** Entangling gates between
logical qubits, error correction running throughout, with the logical error rate
holding up across the sequence. This is where useful computation begins, and it
is the hardest of the four.

The gap between the third and the fourth is the current frontier, and it is
wider than it looks. Some logical operations are comparatively cheap: the
Clifford gates, which can often be performed by rearranging the code rather than
acting on it directly. But Clifford gates alone are classically simulable, so a
machine that can only do them cannot outperform a laptop. Universality requires
at least one non-Clifford gate, and in most schemes that is supplied through
magic state distillation, which consumes a large number of additional physical
qubits and a great deal of time to produce a single usable resource state.

In many resource estimates, distillation dominates the cost of the machine. The
memory is not the expensive part. Doing something with it is.

## How to read the next announcement

Three questions cut through most of the ambiguity.

What is the logical error rate per cycle, and what is it compared against? A
logical qubit that is worse than the best physical qubit in the same device has
not yet demonstrated protection.

Does the logical error rate fall when the code distance increases? If the
result covers only one code size, it is a demonstration of encoding, not of
correction that scales.

Did the logical qubits do anything? Idle memory, Clifford operations, and a
universal gate set are three different achievements, and only the third is on
the path to a computation.

A physical qubit is not a logical qubit. A logical qubit that sits still is not
a logical qubit that computes. Both distinctions get flattened in summary, and
both are where the real state of the field is hiding.
