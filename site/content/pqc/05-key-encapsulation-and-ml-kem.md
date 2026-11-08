---
title: Key encapsulation and ML-KEM
slug: key-encapsulation-and-ml-kem
order: 5
level: Intermediate
published: 2026-11-08
reviewed: 2026-11-08
revisions:
  - date: 2026-11-08
    note: Published.
summary: >-
  A key-encapsulation mechanism produces a fresh shared secret rather than
  encrypting a message. ML-KEM is the NIST standard for it, and its keys and
  ciphertexts are far larger than the elliptic-curve values they replace.
check:
  - q: >-
      In a key-encapsulation mechanism, what does the sender transmit to the
      holder of the decapsulation key?
    a: >-
      A ciphertext. The shared secret itself is never sent. The holder of the
      decapsulation key recovers it from the ciphertext.
  - q: >-
      ML-KEM-768 has a 1184-byte encapsulation key and an X25519 public value is
      32 bytes. Roughly how many times larger is the first?
    a: >-
      About 37 times (1184 divided by 32). The ciphertext of 1088 bytes against
      32 bytes is about 34 times. That is the cost paid in every handshake.
  - q: >-
      Does ML-KEM tell you who you are talking to?
    a: >-
      No. It establishes a shared secret between whoever ran the exchange.
      Authentication comes from signatures, covered in the next lesson.
sources:
  - name: 'NIST, FIPS 203, "Module-Lattice-Based Key-Encapsulation Mechanism Standard" (13 August 2024)'
    url: https://doi.org/10.6028/NIST.FIPS.203
    note: The standard. Sections 1 to 8 were read for the description of a KEM, the three parameter sets, the decapsulation failure rates and the size table.
  - name: 'Langley, Hamburg and Turner, RFC 7748, "Elliptic Curves for Security"'
    url: https://www.rfc-editor.org/rfc/rfc7748
    note: States that X25519 takes and produces 32-byte strings. The standard was read for that statement.
further:
  - title: Harvest now, decrypt later
    url: /pqc/harvest-now-decrypt-later/
    note: Why key exchange is the first thing to migrate.
  - title: Module-LWE
    url: /glossary/#mlwe
---

## A narrower tool than encryption

Public-key encryption encrypts a message under a public key. A key-encapsulation
mechanism, or KEM, does something narrower: it produces a fresh shared secret,
and nothing else. That is all a secure connection needs, because the secret is
then used with a symmetric cipher for the data.

FIPS 203 describes the steps. One party generates a pair of keys, an
encapsulation key and a decapsulation key, and keeps the decapsulation key
private. The other party uses the encapsulation key to produce a shared secret
and a ciphertext, and sends only the ciphertext. The first party runs
decapsulation on the ciphertext and recovers the same secret. An eavesdropper
sees the encapsulation key and the ciphertext, and should not be able to compute
the secret.

## ML-KEM

ML-KEM is the KEM that NIST published as FIPS 203 on 13 August 2024. It is based
on CRYSTALS-Kyber, which NIST selected in its standardization process. The
standard says its security is related to the difficulty of the Module Learning
With Errors problem, and that ML-KEM is believed to be secure even against
adversaries with a quantum computer. The word is "believed". There is no proof,
and this is the same position that factoring has always been in.

The standard approves three parameter sets, in order of increasing strength and
decreasing speed: ML-KEM-512 for security category 1, ML-KEM-768 for category 3
and ML-KEM-1024 for category 5.

## What it costs in bytes

All sizes below are in bytes and come from the standard.

| Parameter set | Category | Encapsulation key | Ciphertext | Shared secret |
|---|---|---|---|---|
| ML-KEM-512 | 1 | 800 | 768 | 32 |
| ML-KEM-768 | 3 | 1184 | 1088 | 32 |
| ML-KEM-1024 | 5 | 1568 | 1568 | 32 |

An X25519 public value is 32 bytes. In a handshake that sends one value each way,
ML-KEM-768 therefore sends about 37 times the data in one direction and about 34
times in the other. These sizes are the main practical cost, and they matter most
where a packet budget is tight: embedded devices, small UDP messages, and
protocols that were built around 32-byte values.

The shared secret is 32 bytes for every parameter set, so the symmetric side of
the connection does not change.

## Failure that is designed away

For well-formed inputs and working randomness, ML-KEM never reports an error: both
sides always end with a 256-bit value. The two sides can still disagree, with a
probability the standard calls the decapsulation failure rate. It is 2^-138.8 for
ML-KEM-512, 2^-164.8 for ML-KEM-768 and 2^-174.8 for ML-KEM-1024, which is small
enough to ignore in practice.

## What a KEM does not do

A KEM gives two parties a shared secret. It does not say who they are. Without
authentication, someone in the middle could run one exchange with each side. That
job belongs to signatures, and it is why the [next lesson](/pqc/signatures-ml-dsa-and-slh-dsa/)
is about them.
