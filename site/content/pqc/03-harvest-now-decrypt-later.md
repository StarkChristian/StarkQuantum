---
title: Harvest now, decrypt later
slug: harvest-now-decrypt-later
order: 3
level: Intro
published: 2026-11-08
reviewed: 2026-11-08
revisions:
  - date: 2026-11-08
    note: Published.
summary: >-
  Encrypted traffic can be recorded today and read later. That makes key exchange
  urgent before any capable machine exists, and puts signatures on a different clock.
check:
  - q: >-
      Why does forward secrecy not protect a recorded TLS session against a
      future quantum computer?
    a: >-
      Forward secrecy protects against later theft of a long-term key. It does
      not help if the key exchange itself is solved. The ephemeral public values
      travel in the clear, so they are in the recording, and Shor's algorithm
      can recover the session secret from them.
  - q: >-
      Which is more exposed to harvest now, decrypt later: a session cookie that
      expires in an hour, or medical records that must stay confidential for
      decades?
    a: >-
      The medical records. The attack costs an adversary a wait of years, so it
      only pays against data whose secrecy outlives that wait.
  - q: >-
      Why do signatures face a different clock from encryption?
    a: >-
      A forgery made in the future cannot change a signature that a system has
      already verified. The urgency comes from trust anchors, such as root
      certificates and firmware keys, that must stay valid for many years.
sources:
  - name: 'NIST IR 8547, "Transition to Post-Quantum Cryptography Standards" (October 2026)'
    url: https://doi.org/10.6028/NIST.IR.8547
    note: Deprecation after 2030 and disallowance after 2035 for quantum-vulnerable signatures and key establishment. The report names harvest now, decrypt later as the reason key establishment may be required earlier.
  - name: 'Apple, "Prepare your network for quantum-secure encryption in TLS"'
    url: https://support.apple.com/122756
    note: States that TLS connections from iOS, iPadOS, macOS and visionOS 26 advertise hybrid key exchange, including X25519MLKEM768.
  - name: 'Mozilla, Firefox 132.0 release notes'
    url: https://www.firefox.com/en-US/firefox/132.0/releasenotes/
    note: Lists added support for a post-quantum key exchange for TLS 1.3. The note does not say whether it is on by default.
  - name: 'Cloudflare, "State of the post-quantum Internet in 2025"'
    url: https://blog.cloudflare.com/pq-2025/
    note: Vendor-reported. States that the majority of human-initiated traffic Cloudflare handles used post-quantum encryption in late October 2025.
  - name: 'IETF, draft-ietf-tls-ecdhe-mlkem'
    url: https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/
    note: An Internet-Draft that specifies hybrid ECDHE and ML-KEM key exchange for TLS. Check the datatracker for its current status.
further:
  - title: What a quantum computer breaks
    url: /pqc/what-a-quantum-computer-breaks/
---

## The attack that needs no quantum computer

The threat is usually described as beginning when a quantum computer is built.
For confidentiality that is wrong. Encrypted traffic can be recorded. Anyone with
access to a network path can store ciphertext today at low cost, and wait. If a
machine that can run Shor's algorithm arrives later, everything captured in the
meantime becomes readable then. The attack is called harvest now, decrypt later,
and its first half needs no quantum computer at all.

Recording leaves nothing to detect. You cannot tell whether your traffic has been
captured, so for long-lived secrets the safe assumption is that it has.

## What forward secrecy does not do

Modern TLS uses ephemeral Diffie–Hellman, usually over an elliptic curve, so
each session gets a fresh key that is discarded afterwards. Forward secrecy means
that stealing the server's long-term key later does not reveal past sessions.

It does not protect a session from someone who can break the key exchange. The
ephemeral public values are sent in the clear as part of the handshake, so they
are in the recording. Shor's algorithm applied to them recovers the session
secret, and the secret decrypts the session. Forward secrecy was designed against
key theft, not against the mathematics being solved.

## How long must it stay secret?

The question to ask of any data is how long it must remain secret. A session
cookie or a one-time password is of no use to an adversary who has to wait a
decade. Medical records, legal and financial archives with statutory retention,
research data and personal identity data are exposed now. If they cross a network
under classical key exchange, assume a copy may exist. You cannot un-send it.
The one control left is to stop adding to the pile.

## What has started to change

Key exchange is where migration has begun. A hybrid scheme combines a classical
exchange with a post-quantum one, so the result stays secure if either holds.
The combination X25519MLKEM768 is specified in an IETF Internet-Draft. Apple's
operating systems at version 26 advertise it in the TLS handshake, and Firefox
added support for a post-quantum exchange in version 132. Cloudflare, which
carries a large share of web traffic, reported in October 2025 that most human
traffic it handled used post-quantum encryption. That figure is the company's own.

A client offering a hybrid exchange protects a session only if the server also
supports it, so the limit is often the server, the load balancer or the CDN.

## Signatures run on another clock

A signature proves that something was authentic when it was verified. A forgery
made in twelve years does not falsify a software update installed and verified
today. There is no harvest-now equivalent for authentication.

Some signing keys are trusted for a very long time, though. A root certificate may
be valid for twenty years or more. A key burned into boot ROM cannot be changed;
the device has to be replaced. For those, replacements must be deployed and
trusted before forgery becomes possible. NIST IR 8547 sets the same dates for
quantum-vulnerable signatures as for key establishment: deprecated after 2030 and
disallowed after 2035. Those are policy deadlines, not predictions about hardware.

Key establishment is urgent because the damage is already accumulating.
Signatures are urgent where a trust anchor outlives the migration. The
[last lesson](/pqc/are-you-already-late/) turns this into one question.
