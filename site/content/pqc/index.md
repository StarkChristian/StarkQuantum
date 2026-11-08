---
title: Post-quantum cryptography
summary: What a quantum computer would break, what replaces it, and how to judge your own exposure, written from the standards and the primary sources.
updated: 2026-11-08
status:
  - title: The first standards are final.
    text: NIST published FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) and FIPS 205 (SLH-DSA) on 13 August 2024.
    source: NIST, PQC standardization process
    url: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization
  - title: Two more are not.
    text: NIST lists FN-DSA (Falcon) as FIPS 206, in development, and selected HQC for standardization on 11 March 2025. The page was updated on 27 October 2026.
    source: NIST, PQC project
    url: https://csrc.nist.gov/projects/post-quantum-cryptography
  - title: The transition dates are published.
    text: NIST IR 8547, October 2026, says quantum-vulnerable signature and key-establishment algorithms will be deprecated after 2030 and disallowed under NIST standards after 2035.
    source: NIST IR 8547
    url: https://doi.org/10.6028/NIST.IR.8547
resources:
  - name: NIST Post-Quantum Cryptography project
    url: https://csrc.nist.gov/projects/post-quantum-cryptography
    note: The primary source for the status of each NIST selection and standard.
  - name: FIPS 203, ML-KEM
    url: https://csrc.nist.gov/pubs/fips/203/final
    note: The key-encapsulation standard, with its parameter sets and sizes.
  - name: FIPS 204, ML-DSA
    url: https://csrc.nist.gov/pubs/fips/204/final
    note: The lattice-based signature standard.
  - name: FIPS 205, SLH-DSA
    url: https://csrc.nist.gov/pubs/fips/205/final
    note: The stateless hash-based signature standard.
  - name: NIST IR 8547
    url: https://doi.org/10.6028/NIST.IR.8547
    note: NIST's transition report, with the deprecation and disallowance dates by algorithm.
  - name: draft-ietf-tls-ecdhe-mlkem
    url: https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/
    note: An Internet-Draft that specifies hybrid key exchange such as X25519MLKEM768 for TLS.
  - name: liboqs
    url: https://github.com/open-quantum-safe/liboqs
    note: A C library of post-quantum algorithms from the Open Quantum Safe project, used for prototyping and testing.
  - name: oqs-provider
    url: https://github.com/open-quantum-safe/oqs-provider
    note: A provider that brings liboqs algorithms into OpenSSL 3 for experiments.
  - name: noble-post-quantum
    url: https://github.com/paulmillr/noble-post-quantum
    note: JavaScript implementations of ML-KEM, ML-DSA and SLH-DSA. Read its own documentation for its audit and side-channel status before using it for anything real.
---

This section covers the part of the quantum story that reaches ordinary systems
first: the public-key cryptography that protects connections, software updates and
identities, and the standards that replace it. It follows the same rules as the
rest of the site. It reads primary sources, says what a claim shows and does not
show, and gives no dates for machines. The dates it gives are deadlines set by
standards bodies, which are policy, not prediction.

It is guidance for reading and planning, not a product, an audit or advice for a
particular system.
