---
title: A deadline in cryptography is not a deadline in hardware
slug: a-deadline-in-cryptography-is-not-a-deadline-in-hardware
category: foundations
difficulty: Intermediate
published: 2026-09-08
reviewed: 2026-09-08
living: true
summary: >-
  Migration deadlines for post-quantum cryptography are real and worth meeting.
  They are not predictions about when a quantum computer will exist, and
  reading them that way gets the whole subject backwards.
footer:
  claim: >-
    Post-quantum migration timelines are risk-management decisions driven by
    data lifetime and the cost of changing infrastructure. They are not
    forecasts of quantum hardware capability.
  evidence: >-
    Resource estimates for breaking widely deployed public-key cryptography sit
    in the millions of physical qubits with sustained error correction. No
    device within orders of magnitude of that exists, and the estimates move
    when algorithms or codes improve, not when qubit counts do.
  missing_piece: >-
    Any demonstration of factoring or discrete logarithms at cryptographically
    relevant scale on error-corrected hardware. Small-number factoring
    demonstrations do not extrapolate, because they rely on knowing the answer
    in advance.
  so_what: >-
    Migrate on the schedule your data lifetime requires, and ignore quantum
    hardware announcements while doing so. The two clocks are not connected in
    the way headlines imply.
sources:
  - name: NIST, Post-Quantum Cryptography standards
    url: https://csrc.nist.gov/projects/post-quantum-cryptography
    note: The standardised algorithms and the migration guidance built on them.
  - name: Gidney and Ekera, "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits"
    url: https://arxiv.org/abs/1905.09749
    note: The resource estimate that anchors most serious discussion of the threat.
---

Two clocks are routinely confused. One is a migration schedule: the dates by
which organisations are expected to move off cryptography that a large quantum
computer would break. The other is a hardware timeline: when such a computer
might exist. The first is published, specific, and enforceable. The second is
unknown. Treating the first as evidence about the second is the most common
error in this part of the field, and it runs in both directions — as alarm and
as dismissal.

## What the migration deadlines actually encode

A migration deadline is a decision about risk, made under uncertainty, using
three inputs.

**How long your data must stay confidential.** Encrypted traffic can be
recorded now and decrypted later, if a capable machine ever arrives. This is
usually called harvest now, decrypt later. For data with a ten- or twenty-year
sensitivity — medical records, state secrets, long-lived identity credentials —
the relevant question is not whether a quantum computer exists today but whether
one might exist within the confidentiality window.

**How long the migration takes.** Replacing public-key cryptography across a
large organisation is a multi-year programme touching protocols, certificates,
hardware security modules, embedded devices, and vendor dependencies. Some of
that hardware has a service life measured in decades and cannot be updated in
the field.

**How much uncertainty you are willing to carry.** Given a long data lifetime
and a long migration, a rational planner starts well before any credible threat
date, because starting late has no recovery path.

Add those together and you get a deadline that is early by construction. It is
early because migration is slow and data is long-lived, not because anyone
believes a cryptographically relevant machine is imminent. A deadline of this
kind is what prudent engineering looks like, and it would be justified even if
the hardware timeline were centuries.

## What the hardware would actually have to do

The threat to RSA and elliptic-curve cryptography is Shor's algorithm, and Shor's
algorithm needs a fault-tolerant machine. Not a large noisy one — a corrected
one, running deep circuits for hours without accumulating a single uncorrected
logical error.

Published resource estimates for factoring a 2048-bit RSA modulus have
consistently landed in the range of millions of physical qubits with error rates
well below threshold and error correction running throughout, with runtimes of
hours to days. The estimates have come down over time as algorithms and codes
improved, and they may come down further. They have not come down to anything
near what exists.

Note where the movement in those estimates comes from. It comes from better
arithmetic circuits, better error-correcting codes, and better magic state
distillation — algorithmic and architectural work, largely done on paper. It
does not come from qubit count announcements. This is why a headline about a new
processor with more qubits is, on its own, almost irrelevant to the threat.

There is also a category of result that looks relevant and is not. Small-number
factoring demonstrations — factoring 15, or 21, or a carefully chosen larger
number — generally rely on circuit simplifications that require knowing the
answer beforehand. They demonstrate control of the hardware. They do not
extrapolate, and a device that factors a small number is not a fraction of the
way to factoring a large one.

## What is actually at risk, and what is not

The exposure is uneven, and the difference matters for planning.

Public-key cryptography — RSA, Diffie-Hellman, elliptic curves — is broken by
Shor's algorithm, given the machine. That is what post-quantum standards
replace, and replacements are now standardised and deployable.

Symmetric cryptography is far less exposed. Grover's algorithm gives a quadratic
speedup on brute-force search, which is addressed by using longer keys. AES-256
remains comfortable. This is a parameter change, not a redesign.

Hash functions are in a similar position. The practical response is larger
outputs, not new constructions.

So "quantum breaks encryption" is wrong as stated. It breaks one family of
constructions, that family happens to underpin key exchange and signatures
across the internet, and the replacements exist.

## How this site treats the subject

Cryptographic threat is a downstream consequence of hardware, and it belongs on
this site only when a hardware result or a resource estimate moves it. That
means two kinds of thing get written up: a change in the resource estimates,
because those are the numbers that actually track the threat; and error
correction results that alter what a fault-tolerant machine would cost.

It also means a great deal does not get written up. Standardisation news,
migration guidance, vendor readiness claims, and warnings about a coming
cryptographic emergency are not hardware results. They may be important
operationally. They contain no information about whether a machine is closer.

The Reality Board has no cell for cryptographic threat, and that is deliberate.
The threat does not move on its own. It moves when logical qubits with useful
operations arrive, and again when a fault-tolerant machine at useful scale
arrives — cells two and four. Giving it a row of its own would imply an
independent variable where there is none.

## The practical position

Migrate on the schedule your data lifetime requires. Inventory where public-key
cryptography is used, prioritise long-lived secrets and long-lived hardware, and
move. That programme is justified by the cost and duration of migration alone.

While doing it, do not adjust the schedule in response to qubit count
announcements, and do not take comfort from the absence of them. A deadline in
cryptography is a statement about your data and your infrastructure. A deadline
in hardware does not exist, and nobody credible is offering one.
