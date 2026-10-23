---
title: What entanglement is, and is not
slug: entanglement
order: 7
level: Intro
script: bell.js
published: 2026-10-23
reviewed: 2026-10-23
revisions:
  - date: 2026-10-23
    note: Published.
summary: >-
  Entangled qubits share one state that cannot be split into a state for each.
  Measuring them gives results that agree in a way nothing classical explains,
  and yet no message travels between them.
check:
  - q: >-
      Alice and Bob share the pair $(|00\rangle + |11\rangle)/\sqrt{2}$ and both
      measure in the same basis. Alice gets 0. What does Bob get?
    a: >-
      0. In the same basis the two results always agree, and each result alone is
      0 or 1 with probability one half.
  - q: >-
      Can Alice use the pair to send Bob a message faster than light, by choosing
      how to measure?
    a: >-
      No. Whatever Alice chooses, Bob's results on their own are 0 or 1 with
      probability one half. The agreement only appears when the two compare their
      records over an ordinary channel, which is no faster than light.
  - q: >-
      Why can the agreement not be explained by each particle carrying a pre-set
      answer, like a pair of gloves sent to two cities?
    a: >-
      With pre-set answers, a combination of correlations (the CHSH quantity)
      cannot exceed 2. Entangled pairs measured at suitable angles give about
      2.83, and experiments have observed values above 2.
sources:
  - name: 'Nielsen and Chuang, Quantum Computation and Quantum Information (Cambridge University Press, 2010)'
    note: Section 1.3.7 and chapter 2 for the Bell state, and section 2.6 for Bell's inequality.
  - name: 'Bell, "On the Einstein Podolsky Rosen paradox", Physics 1, 195 (1964)'
    note: The inequality that a pre-set-answer theory must satisfy.
  - name: 'Clauser, Horne, Shimony and Holt, "Proposed experiment to test local hidden-variable theories", Phys. Rev. Lett. 23, 880 (1969)'
    note: The CHSH form of the inequality, with bound 2.
  - name: 'The Nobel Prize in Physics 2022 (Aspect, Clauser and Zeilinger), nobelprize.org'
    url: https://www.nobelprize.org/prizes/physics/2022/summary/
    note: Awarded for experiments with entangled photons that established the violation of Bell inequalities.
further:
  - title: What a qubit is
    url: /learn/what-a-qubit-is/
  - title: Glossary, no-cloning
    url: /glossary/#no-cloning
  - title: Claims register
    url: /claims/
---

Two qubits can be in a joint state that cannot be written as a state of the first
and a separate state of the second. They are then entangled. The standard example
is the Bell pair, $(|00\rangle + |11\rangle)/\sqrt{2}$.

## What a Bell pair does

Measure both qubits in the same way. Each result on its own is 0 or 1 with
probability one half, so each looks like a fair coin. Yet the two results always
agree: both 0 or both 1. This stays true however far apart the qubits are when
they are measured.

Measure them in different ways, and the agreement weakens in a precise manner. If
the two measurement axes differ by an angle $\theta$, the results agree with
probability $\cos^2(\theta/2)$.

[figure:bell]

## It does not carry a message

The agreement can look like a signal. It is not one. Suppose Alice chooses how to
measure her qubit. Bob's results, looked at alone, are fair coin flips whatever she
chose. The pattern only appears when the two put their records side by side, and
that needs an ordinary message, which cannot go faster than light.

This is why entanglement is not a telegraph or a portal. It is a correlation that
only shows up in a comparison.

## It is not a pair of gloves

A natural explanation is that the particles agreed on answers in advance, like a
pair of gloves sent to two cities: open one box and you know what is in the other.
In 1964 John Bell showed this explanation makes a testable prediction. If each
particle carries pre-set answers, a certain combination of correlations, measured
with four choices of axes, cannot exceed 2. That is the CHSH inequality.

Quantum mechanics predicts up to $2\sqrt{2} \approx 2.83$ for an entangled pair.
Experiments with entangled photons found values above 2, and the 2022 Nobel Prize
in Physics went to Aspect, Clauser and Zeilinger for this work. The simulation
above samples from the quantum prediction, so it can show the number, but it
cannot show that pre-set answers are impossible. Only the experiments do.

## What it is used for

Entanglement is a resource that quantum algorithms and quantum communication
protocols consume. In a quantum computer, two-qubit gates such as CNOT create it,
and many algorithms rely on it. It must also be protected: the noise described in
the lesson on errors tends to destroy it.

An unknown quantum state cannot be copied, which is a separate fact, the
no-cloning theorem. Together these two facts are why some cryptographic tasks have
no classical equivalent. They are also why entanglement is easy to oversell, so ask
what a claim actually does with it.
