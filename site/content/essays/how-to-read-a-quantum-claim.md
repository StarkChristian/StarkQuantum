---
title: How to read a quantum claim
slug: how-to-read-a-quantum-claim
category: foundations
difficulty: Intro
published: 2026-09-08
reviewed: 2026-09-08
living: true
summary: >-
  A procedure for taking any quantum announcement apart: find the number, find
  the comparison, find the conditions, and find out who checked. Most claims
  fail before the third step.
footer:
  claim: >-
    Most quantum announcements can be evaluated by a reader with no physics
    background, because most of them fail on structure rather than on physics.
  evidence: >-
    The recurring failure modes are few and identifiable: no number, no
    baseline, a baseline chosen by the claimant, conditions that make the task
    easy, and verification performed only by the people who built the device.
  missing_piece: >-
    Independent reproduction. Almost nothing in this field is confirmed by a
    group with no stake in the result, and where reproduction has happened it
    has repeatedly moved the goalposts back.
  so_what: >-
    Apply four questions in order. Anything that survives all four is worth
    your attention, and there will not be much of it in a given year.
sources:
  - name: arXiv, quant-ph
    url: https://arxiv.org/list/quant-ph/recent
    note: Where the primary sources appear, usually weeks before the coverage.
  - name: Aaronson, "The Limits of Quantum Computers"
    url: https://www.scottaaronson.com/papers/sciam.pdf
    note: On what these machines are and are not expected to be good at.
---

You do not need to understand the physics to evaluate most quantum
announcements. Most of them fail on structure long before physics becomes
relevant. What follows is a procedure that takes a few minutes and disposes of
the large majority of what gets published.

## One: find the number

Read the announcement and write down every quantitative claim in it. Not the
adjectives — the numbers, with their units.

A surprising fraction of quantum coverage survives this step with nothing
written down. Announcements about partnerships, national strategies, funding
rounds, roadmaps, and future availability contain no measurement. They may be
commercially significant. They are not evidence about a machine, and they cannot
be checked.

If there is no number, stop. You have finished reading.

If there is a number, note which kind it is. Qubit count is the weakest, and it
is the one most likely to appear alone. Gate fidelity, coherence time, logical
error rate, and circuit depth are stronger, because each of them constrains what
the device can actually do. A press release that gives a count and omits the
fidelity has chosen which of those to tell you.

## Two: find the comparison

A number without a baseline means nothing. Faster than what? Better than which
alternative, run by whom, with how much effort?

This is where advantage claims usually come apart. The claim is that a quantum
processor did something a classical computer could not do in reasonable time.
The strength of that claim rests entirely on the classical side of the
comparison, and the classical side is generally computed by the same team, using
the best classical algorithm they were aware of at the time.

That is not dishonest, but it is fragile. The history of this field is that
classical algorithms improve after the announcement, often sharply, once
specialists have a concrete target to attack. Simulations that were said to
require millennia have been brought down to days by better tensor-network
methods and more careful use of memory. The physical experiment stays valid; the
comparison it was measured against does not.

So the question is not "did the quantum device do it" but "what exactly was the
classical baseline, who produced it, and has anyone hostile to the claim tried
to beat it." If the answer to the last part is no, the claim is provisional
regardless of how careful the experiment was.

## Three: find the conditions

Every result was obtained under conditions somebody chose. List them.

Was the problem selected because it suits the hardware? Random circuit sampling
and similar tasks are chosen precisely because they are hard classically and
natural quantumly. That makes them good tests of a device and poor evidence
about applications. Nobody has this problem.

Was there post-selection? Discarding runs that failed a check is a legitimate
technique, and it also means the reported fidelity is conditional on a filter
that a real computation would not be allowed to apply.

How was the answer verified? There are three cases, and they carry very
different weight. The problem was classically simulable, so the answer could be
checked directly — reassuring about correctness, but then a classical computer
solved it too. The answer was checked statistically, by arguing that the output
distribution has the right shape — weaker, and dependent on the model used. Or
the answer was not verified at all, and the claim rests on the machine having
behaved as expected.

How many times did it run, and what happened on the runs that were not reported?
A result that holds on one device on one day, and has not been repeated, is a
data point rather than a finding.

## Four: find out who checked

Look at where the claim was published and who has examined it.

A preprint is the primary source and is usually the best available document; it
also has not been refereed. A peer-reviewed paper has passed a small number of
anonymous readers, which is a real filter but not a reproduction. A company blog
post describing internal work with no accompanying paper is an assertion.

The strongest signal, and the rarest, is an independent group reproducing the
result or failing to. Reproduction in this field is expensive, because the
apparatus is expensive, so the honest position on almost every recent result is
that it has not been independently confirmed.

Refutations deserve the same scrutiny as claims. A classical algorithm that
matches a quantum result is itself a result, and it should be read with the same
four questions.

## What survives

Applied consistently, this procedure discards most of what is published about
quantum computing. That is the correct outcome. The field produces a handful of
results a year that change what is known, and a very large volume of material
that changes only what is being said.

Three sentences summarise the whole procedure, and they are worth keeping
somewhere near the front of your mind.

A press release is not evidence. It is a description of evidence, written by a
party with an interest in how it is described, and the primary source is
generally available and generally more careful.

Laboratory advantage is not application. Doing something faster than a classical
computer on a task designed to be hard for classical computers is a measurement
of the device, not a use for it.

A demo is not a machine. The demonstration establishes that a thing happened
once, under chosen conditions, checked by the people who arranged them. That is
how progress is made, and it is not the same as a computer somebody can use.

None of this requires assuming bad faith. Researchers in this field are, on the
whole, careful about caveats, and the caveats are usually right there in the
abstract. They are removed in transit — by summaries, by headlines, by the need
to describe a slow technical process as an event. Reading the primary source
puts them back.
