---
title: What quantum computers are believed to be for
slug: what-quantum-computers-are-for
order: 6
level: Intermediate
published: 2026-10-22
reviewed: 2026-10-22
summary: >-
  A short list of tasks with a real argument for a quantum speedup, and a longer
  list of claims without one. The word to hold on to is believed.
check:
  - q: >-
      Grover search gives a quadratic speedup. If a classical search needs
      $10^{12}$ steps, roughly how many does Grover's algorithm need?
    a: >-
      About $10^{6}$ queries, the square root. Each one is a fault-tolerant
      operation far more expensive than a classical step, which can erase much
      of the gain in practice.
  - q: Why is the speedup for factoring believed rather than proved?
    a: >-
      Shor's algorithm runs in polynomial time, but nobody has proved that no
      fast classical algorithm exists. The best known classical method is faster
      than brute force and still sub-exponential rather than polynomial.
  - q: >-
      A team reports an experiment that no classical method they tried could
      reproduce. What three things do you ask before calling it an advantage?
    a: >-
      Which classical methods were tried, and how well tuned. Whether the task
      was chosen to suit the hardware or is one someone needs solved. And whether
      anyone with no stake in the result has checked it, since improved classical
      algorithms have narrowed earlier claims.
sources:
  - name: 'Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits", arXiv:2505.15917 (21 May 2025)'
    url: https://arxiv.org/abs/2505.15917
    note: Under one million noisy qubits and under a week, for the hardware assumptions stated in the paper.
  - name: 'Babbush, McClean, Newman, Gidney, Boixo and Neven, "Focus beyond quadratic speedups for error-corrected quantum advantage", PRX Quantum (2021), arXiv:2011.04149'
    url: https://arxiv.org/abs/2011.04149
    note: Estimates that small quadratic speedups are unlikely to give a practical advantage on early fault-tolerant machines.
  - name: 'Tang, "A quantum-inspired classical algorithm for recommendation systems", arXiv:1807.04271'
    url: https://arxiv.org/abs/1807.04271
    note: A classical algorithm that removes the claimed exponential speedup for a quantum recommendation algorithm.
  - name: 'Martiel et al., "Sampling hard circuits with verifiably high fidelity", arXiv:2607.25941 (28 July 2026)'
    url: https://arxiv.org/abs/2607.25941
    note: One of the IBM-linked preprints of July 2026 that claim results beyond tested classical methods.
further:
  - title: A deadline in cryptography is not a deadline in hardware
    url: /articles/a-deadline-in-cryptography-is-not-a-deadline-in-hardware/
  - title: Why advantage demos keep disappearing
    url: /articles/why-advantage-demos-keep-disappearing/
    note: What happens when a classical method catches up.
  - title: Glossary, quantum advantage
    url: /glossary/#quantum-advantage
---

A quantum computer is not a faster computer. It is a different one, and for a
few kinds of problem the structure of the problem lets it do something a
classical machine cannot do as cheaply. The honest list is short.

## Simulating quantum systems

Simulating a quantum system on a classical computer gets expensive quickly,
because the description grows exponentially with the size of the system in
general. A quantum computer represents it directly. Chemistry and materials,
where electrons interact strongly, are the standard targets.

The caveat is that classical methods for these problems are also very good and
keep improving. The case for quantum is strongest for strongly correlated
systems that those methods handle badly. Sizes that matter for industry are
expected to need error-corrected machines of a scale that no device has today.

## Factoring and discrete logarithms

Shor's algorithm factors integers in polynomial time. The best known classical
algorithm is much faster than brute force and still sub-exponential. This is the
application that threatens public-key cryptography built on factoring and on
elliptic curves.

Two things keep this in proportion. First, the speedup is believed, not proved:
no one has shown that a fast classical factoring algorithm cannot exist. Second,
running it at cryptographic sizes needs error correction at scale. A 2025
estimate by Craig Gidney put factoring a 2048-bit RSA number at fewer than one
million noisy physical qubits and less than a week of running, under the hardware
assumptions in that paper. That is far below earlier estimates, and far above any
machine that exists.

## Searching

Grover's algorithm searches an unstructured collection of $N$ items in about
$\sqrt{N}$ steps instead of $N$. The speedup is quadratic, which helps less than
it sounds. Each quantum step is a fault-tolerant operation, much slower and more
expensive than a classical one. A 2021 analysis estimated that quadratic
speedups are unlikely to give a practical advantage on early fault-tolerant
machines.

## Claims made in 2026

In July 2026, IBM and collaborators posted preprints reporting experiments for
which they say no known classical method reproduces the results. One of them
describes a structured circuit on 64 qubits, encoded in 76 physical qubits, with
a certified lower bound on its fidelity. These are claims about sampling and
about simulating quantum systems, on tasks chosen to suit the hardware, and the
authors' evidence is limited to the classical methods that were tried. Earlier
claims of this kind have been narrowed when better classical algorithms
appeared. Treat them as candidates until others have tested them.

## Optimisation and machine learning

There are heuristics, and demonstrations on problems chosen for the hardware.
Claims here have been measured against selected classical baselines, and whether
any holds against the best classical method on a problem someone needs solved is
unsettled.

Loading classical data into a quantum state is itself a bottleneck. In 2018, Ewin
Tang gave a classical algorithm that matched a quantum recommendation algorithm
and removed its claimed exponential speedup. That does not mean no machine-learning
speedup exists. It means the burden is on the claim.

## What "believed" means

For most items above, the speedup rests on an argument, not on a proof that no
classical method can match it. A confident headline usually leaves out which kind
of claim it is.

## Three questions for any claimed use

What is the best classical method for the same problem, and how much effort went
into it? What size of problem, and how many error-corrected qubits does it need?
And has a team with no stake in the result checked it? A demonstration that fails
the first question is the kind that tends to disappear.
