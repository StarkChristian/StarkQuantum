---
title: "Signatures: ML-DSA and SLH-DSA"
slug: signatures-ml-dsa-and-slh-dsa
order: 6
level: Intermediate
published: 2026-11-08
reviewed: 2026-11-08
revisions:
  - date: 2026-11-08
    note: Published.
summary: >-
  NIST has standardised two post-quantum signature schemes that rest on different
  assumptions. Both have much larger signatures than the ones they replace.
check:
  - q: >-
      Why does NIST standardise a hash-based signature scheme alongside a
      lattice-based one?
    a: >-
      They rest on different assumptions. A hash-based scheme depends only on the
      security of a hash function, so a flaw found in lattice problems would not
      take it down. The price is much larger signatures.
  - q: >-
      An ML-DSA-65 signature is 3309 bytes and an Ed25519 signature is 64 bytes.
      Why does that matter more for a certificate chain than for one signed file?
    a: >-
      A chain carries a signature and a public key for every certificate in it,
      and they are sent in every connection that presents the chain, so the extra
      bytes are multiplied.
sources:
  - name: 'NIST, FIPS 204, "Module-Lattice-Based Digital Signature Standard" (13 August 2024)'
    url: https://doi.org/10.6028/NIST.FIPS.204
    note: The standard. The abstract, the size table, the security categories and the passage on hedged signing were read.
  - name: 'NIST, FIPS 205, "Stateless Hash-Based Digital Signature Standard" (13 August 2024)'
    url: https://doi.org/10.6028/NIST.FIPS.205
    note: The standard. The abstract and the table of the twelve parameter sets were read.
  - name: 'NIST, Post-Quantum Cryptography project'
    url: https://csrc.nist.gov/projects/post-quantum-cryptography
    note: Lists FN-DSA (Falcon) as FIPS 206, in development. The page was updated on 27 October 2026.
  - name: 'Josefsson and Liusvaara, RFC 8032, "Edwards-Curve Digital Signature Algorithm (EdDSA)"'
    url: https://www.rfc-editor.org/rfc/rfc8032
    note: States that Ed25519 public keys are 32 octets and signatures 64 octets. The standard was read for that statement.
further:
  - title: Key encapsulation and ML-KEM
    url: /pqc/key-encapsulation-and-ml-kem/
  - title: Are you already late?
    url: /pqc/are-you-already-late/
---

## What a signature has to do

A digital signature lets a recipient detect a change to data and check who
signed it. Shor's algorithm breaks the signature schemes in use today, RSA and the
elliptic-curve family, so they need replacements as well as key exchange does.
The urgency differs, as the lesson on harvest now, decrypt later explained, but
the standards were published together on 13 August 2024.

## ML-DSA

FIPS 204 specifies ML-DSA, a lattice-based scheme derived from CRYSTALS-Dilithium.
The standard says ML-DSA is believed to be secure even against an adversary with a
large quantum computer. It has three parameter sets. Sizes are in bytes.

| Parameter set | Category | Public key | Signature |
|---|---|---|---|
| ML-DSA-44 | 2 | 1312 | 2420 |
| ML-DSA-65 | 3 | 1952 | 3309 |
| ML-DSA-87 | 5 | 2592 | 4627 |

By default ML-DSA signs in a "hedged" way: each signature mixes in fresh
randomness. The standard says the main purpose is to help against side-channel and
fault attacks on deterministic signing.

## SLH-DSA

FIPS 205 specifies SLH-DSA, a stateless hash-based scheme based on SPHINCS+. Its
security rests on hash functions alone. It has twelve parameter sets. Public keys
are 32, 48 or 64 bytes, and signatures are much larger than ML-DSA's.

| Parameter sets | Category | Public key | Signature |
|---|---|---|---|
| 128s and 128f | 1 | 32 | 7,856 and 17,088 |
| 192s and 192f | 3 | 48 | 16,224 and 35,664 |
| 256s and 256f | 5 | 64 | 29,792 and 49,856 |

Each row covers two variants that differ in the trade between signature size and
the rest of the cost. In the table the "s" variants have the smaller signatures.
Each parameter set also exists with SHA-2 or with SHAKE, which is why there are
twelve in all.

## Why there are two

The two schemes rest on different assumptions: lattice problems for ML-DSA, and
only the security of hash functions for SLH-DSA. Having both means a break in one
family would not remove every standardised signature. SLH-DSA pays for that with
signatures several times larger and, in the larger sets, tens of kilobytes.

NIST also lists a third, FN-DSA, based on Falcon, as FIPS 206 and in development.
No standard text for it is cited here.

## The cost in bytes

An Ed25519 public key is 32 bytes and its signature is 64 bytes. An ML-DSA-65
signature is 3309 bytes, about 52 times larger, and its public key is 1952 bytes,
about 61 times larger. These figures are derived from the sizes above.

That matters most where signatures are repeated. A certificate chain carries a
signature and a public key for each certificate, and it is sent whenever a
connection presents it. Firmware images and software updates are signed once but
read by many devices, some with little room. For those, the size of the signature
is a design constraint from the start, not a detail to check at the end.
