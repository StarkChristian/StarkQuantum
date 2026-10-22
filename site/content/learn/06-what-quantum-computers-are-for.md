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
      What do you ask of a claimed advantage in optimisation or machine
      learning?
    a: >-
      Against which classical method, how well tuned, and on what problem size.
      No advantage of this kind has been shown on a problem someone needs
      solved.
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
because the description grows exponentially with the size of the system. A
quantum computer represents it directly. Chemistry and materials, where
electrons interact strongly, are the standard targets.

The caveat is that classical methods for these problems are also very good and
keep improving. The case for quantum is strongest for strongly correlated
systems that those methods handle badly. The machines needed for useful sizes
are fault-tolerant, which is years of hardware work away from today's devices.

## Factoring and discrete logarithms

Shor's algorithm factors integers in polynomial time. The best known classical
algorithm is much faster than brute force and still sub-exponential. This is
the application that threatens public-key cryptography built on factoring and
on elliptic curves.

Two things keep this in proportion. First, the speedup is believed, not proved:
no one has shown that a fast classical factoring algorithm cannot exist. Second,
running it at cryptographic sizes needs error correction at scale. A 2025
estimate put factoring a 2048-bit RSA number at under a million noisy physical
qubits and about a week of running. That is far below earlier estimates, and far
above any machine that exists.

## Searching

Grover's algorithm searches an unstructured collection of $N$ items in about
$\sqrt{N}$ steps instead of $N$. The speedup is quadratic, which helps less than
it sounds. Each quantum step is a fault-tolerant operation, much slower and more
expensive than a classical one, and for many problems the quadratic gain does not
survive that overhead.

## What has no established argument

**Optimisation.** There are heuristics, and demonstrations on problems chosen for
the hardware. There is no accepted case that a quantum method beats the best
classical one on a problem someone needs.

**Machine learning.** Loading classical data into a quantum state is itself a
bottleneck, and several proposed speedups have been matched by classical
algorithms once someone looked. This does not mean none exist. It means the
burden is on the claim.

## What "believed" means

For every item above, the speedup rests on an argument, not on a proof that no
classical method can match it. The exceptions are results in restricted models
that do not transfer directly to real problems. A confident headline usually
leaves out which kind of claim it is.

## Three questions for any claimed use

What is the best classical method for the same problem, and how much effort went
into it? What size of problem, and how many error-corrected qubits does it
need? And has a team with no stake in the result checked it? A demonstration that
fails the first question is the kind that tends to disappear.
