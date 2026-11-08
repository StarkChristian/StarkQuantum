---
title: What a quantum computer breaks
slug: what-a-quantum-computer-breaks
order: 1
level: Intro
published: 2026-11-08
reviewed: 2026-11-08
revisions:
  - date: 2026-11-08
    note: Published.
summary: >-
  Shor's algorithm breaks the two problems under almost all public-key
  cryptography in use. It does not break everything, and the machine it needs
  has not been built.
check:
  - q: >-
      Why does doubling the size of an RSA key not protect it from Shor's
      algorithm?
    a: >-
      Shor's algorithm runs in polynomial time, so a larger key raises its cost
      only polynomially. Making the key long enough to matter would make it
      unusable, so the problem itself has to be replaced.
  - q: >-
      Besides the algorithm, what does an attack on a 2048-bit RSA key need?
    a: >-
      A large quantum computer that corrects its own errors. The circuit is far
      deeper than noisy physical qubits can run, so it needs logical qubits, and
      most of the cost in published estimates is error correction.
sources:
  - name: 'Shor, "Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer", arXiv:quant-ph/9508027'
    url: https://arxiv.org/abs/quant-ph/9508027
    note: The algorithm. The result is standard and is cited, not re-derived.
  - name: 'Gidney and Ekerå, "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits", arXiv:1905.09749 (2019)'
    url: https://arxiv.org/abs/1905.09749
    note: The 2019 estimate.
  - name: 'Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits", arXiv:2505.15917 (2025)'
    url: https://arxiv.org/abs/2505.15917
    note: Under one million noisy qubits and under a week, for the hardware assumptions stated in the paper.
  - name: 'Cain et al., "Shor''s algorithm is possible with as few as 10,000 reconfigurable atomic qubits", arXiv:2603.28627 (2026)'
    url: https://arxiv.org/abs/2603.28627
    note: A theoretical estimate and a preprint. The authors state that substantial engineering challenges remain.
further:
  - title: Error correction in one page
    url: /learn/error-correction-in-one-page/
    note: Why the machine in this lesson is hard to build.
  - title: Reality Board
    url: /reality/
    note: Where the hardware stands, by the site's written conditions.
---

## Two problems hold up public-key cryptography

Almost every secure connection today relies on one of two problems being hard.
The first is integer factoring: given the product of two large primes, find the
primes. RSA depends on it. The second is the discrete logarithm: given a group
element and a power of it, find the exponent. Diffie–Hellman, DSA and the
elliptic-curve family (ECDH, ECDSA, Ed25519) depend on that one.

Classically, both problems are believed to be infeasible at the sizes deployed.
The best known classical method for factoring, the general number field sieve,
takes sub-exponential but super-polynomial time. That is why a 2048-bit modulus
is out of reach.

## What Shor's algorithm changes

In 1994 Peter Shor showed that a quantum computer could solve both problems in
polynomial time. It does not try keys faster. It uses the quantum Fourier
transform to find the period of a function, and the period reveals the factors
or the exponent.

That is why larger keys do not rescue these schemes. Doubling an RSA modulus
raises the cost of Shor's algorithm only polynomially, and an algorithm that
runs in polynomial time absorbs that. The remedy is to replace the mathematical
problem, not to enlarge it.

Anything whose security reduces to factoring or discrete logarithms is on the
list: TLS handshakes, SSH, VPNs, signed software updates, certificate chains and
code-signing keys. Most of them use RSA or elliptic curves underneath.

## What the attack needs

Shor's algorithm needs a large machine that corrects its own errors. Physical
qubits are noisy, and a circuit deep enough to factor a 2048-bit number needs
logical qubits, each built from many physical ones with error correction running
throughout. Almost all of the cost in published estimates is error correction,
not the algorithm.

Those estimates have fallen. In 2019 Gidney and Ekerå estimated 20 million noisy
qubits and eight hours. In 2025 Gidney estimated fewer than one million noisy
qubits and under a week for a 2048-bit RSA number, under the same hardware
assumptions. A March 2026 preprint estimates that Shor's algorithm could run on
as few as 10,000 reconfigurable atomic qubits, with longer run times, under its
own assumptions.

These are estimates of what a machine would need. None says when one will
exist, and this site does not forecast it. The [Reality Board](/reality/) records
where error correction stands against its written conditions.

## What demonstrations show

Factoring tiny numbers such as 15 or 21 on quantum hardware shows that the
algorithm can be executed on a small instance. It does not show that the
error-correction problem behind a useful run is solved, and it is not a
countdown.

## What is not on the list

Symmetric ciphers and hash functions are not broken by Shor's algorithm. The
[next lesson](/pqc/symmetric-cryptography-survives/) explains why. The
replacement public-key schemes rest on other problems, for which no efficient
quantum algorithm is known. That is a weaker statement than a proof, and it is
the same statement that has always been made about factoring.
