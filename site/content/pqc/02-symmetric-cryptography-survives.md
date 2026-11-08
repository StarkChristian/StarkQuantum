---
title: Why symmetric cryptography mostly survives
slug: symmetric-cryptography-survives
order: 2
level: Intro
published: 2026-11-08
reviewed: 2026-11-08
revisions:
  - date: 2026-11-08
    note: Published.
summary: >-
  Grover's algorithm speeds up key search only quadratically. Larger keys restore
  the margin, so the urgent work is in key exchange and signatures.
check:
  - q: >-
      What kind of speed-up does Grover's algorithm give against a symmetric key
      search?
    a: >-
      Quadratic. It searches a space of size N in about the square root of N
      steps, so a 128-bit key search costs about 2^64 quantum steps, and a
      256-bit one about 2^128.
  - q: >-
      A session is encrypted with AES-256, but the key was agreed with elliptic-curve
      Diffie–Hellman. Is the recording safe against a future quantum computer?
    a: >-
      No. Shor's algorithm applied to the recorded key exchange recovers the AES
      key. The cipher is only as strong as the key agreement that produced its key.
sources:
  - name: 'Grover, "A fast quantum mechanical algorithm for database search", arXiv:quant-ph/9605043'
    url: https://arxiv.org/abs/quant-ph/9605043
    note: The algorithm. The result is standard and is cited, not re-derived.
  - name: 'Zalka, "Grover''s quantum searching algorithm is optimal", arXiv:quant-ph/9711070'
    url: https://arxiv.org/abs/quant-ph/9711070
    note: The square-root speed-up cannot be improved for unstructured search, including when the work is spread over many machines.
further:
  - title: What a quantum computer breaks
    url: /pqc/what-a-quantum-computer-breaks/
    note: The previous lesson.
---

## Grover's algorithm

Symmetric cryptography covers block ciphers such as AES, hash functions such as
SHA-2 and SHA-3, and the message authentication codes built from them. The
relevant quantum result for it is Grover's algorithm, which searches an
unstructured space of size N in about the square root of N steps.

Applied to a key search, that turns a 2^128 problem into about 2^64 quantum
steps. You will often see this summarised as "quantum computers halve your key
length". As a statement about the best possible speed-up, that is right. It is
not an exponential speed-up, which is what separates it from Shor's algorithm.

## Why the effect is smaller in practice

The speed-up is also hard to parallelise. Grover's algorithm works by rotating a
quantum state through many iterations in sequence. Spreading the search over
many machines divides the number of iterations only by the square root of the
number of machines, and Zalka showed that no better scheme exists for
unstructured search. A classical key search can be split across a data centre
with no such loss.

How costly each error-corrected step would be, and so whether a Grover attack on
a 128-bit key is ever worth mounting, depends on hardware that does not exist.
This site does not rely on the answer. The usual response is simply to use a key
long enough that the square root is still comfortable.

## What would change the picture

The conclusion rests on the speed-up being only quadratic. A different quantum
algorithm for symmetric primitives with a larger advantage would change it, and
none is known. That is the same kind of statement as for the lattice problems in
the new public-key standards: absence of a known attack, not a proof. It is why
the standard response is a margin rather than a bet.

## The response is larger parameters

A 256-bit key leaves about 2^128 quantum steps, so the standard remedy is a
longer key, not a new design. Hash functions are in a similar position: use an
output long enough that a square-root speed-up on pre-image search leaves a
comfortable margin. Key derivation and message authentication built on those
hashes inherit the same position.

If your systems use AES-256, you have very little symmetric work to do. If they
use 128-bit keys, moving up is routine hygiene with a known cost. The places
worth checking are the ones where sizes were chosen years ago and never
revisited: TLS cipher policy, disk and database encryption, backup archives,
and VPN settings.

## Why this does not let anyone off

A symmetric key protects data only once both ends share it. The mechanism that
gets the key to both ends is a key exchange, and that is exactly what Shor's
algorithm breaks. A recorded session encrypted under AES-256 is not safe if the
handshake that produced the AES key used elliptic-curve Diffie–Hellman.

So the urgent work is on the public-key side, in key exchange and signatures.
The [next lesson](/pqc/harvest-now-decrypt-later/) explains why key exchange
cannot wait for the machine.
