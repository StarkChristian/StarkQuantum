---
title: Hybrid key exchange and where to start
slug: hybrid-key-exchange-and-where-to-start
order: 7
level: Intermediate
published: 2026-11-08
reviewed: 2026-11-08
revisions:
  - date: 2026-11-08
    note: Published.
summary: >-
  A hybrid exchange combines a classical and a post-quantum one so that it holds
  if either holds. NIST treats it as a likely temporary step, and says to begin
  with an inventory.
check:
  - q: >-
      What property is a hybrid key exchange designed to have?
    a: >-
      The derived keys stay secure if at least one of the component schemes is
      secure. It is a hedge against a flaw in either one.
  - q: >-
      Why does NIST expect hybrid solutions to be temporary?
    a: >-
      They add complexity to implementations and architectures, which can raise
      risk and cost, so NIST expects them to lead to a second transition to
      post-quantum algorithms alone.
  - q: >-
      What does NIST say organisations should begin with?
    a: >-
      Cryptographic inventories, then migration planning and early deployments of
      products and services that support post-quantum cryptography.
sources:
  - name: 'NIST IR 8547, "Transition to Post-Quantum Cryptography Standards" (October 2026)'
    url: https://doi.org/10.6028/NIST.IR.8547
    note: Section 3.2 on hybrid protocols, section 3.2.1 on hybrid key establishment, and the introduction on inventories and cryptographic agility.
  - name: 'IETF, draft-ietf-tls-ecdhe-mlkem'
    url: https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/
    note: An Internet-Draft that specifies hybrid ECDHE and ML-KEM key exchange for TLS. The draft text was not read for this lesson; check the datatracker for its status.
further:
  - title: Harvest now, decrypt later
    url: /pqc/harvest-now-decrypt-later/
  - title: Are you already late?
    url: /pqc/are-you-already-late/
---

## What a hybrid is

A hybrid key exchange runs two exchanges and combines their results. In the
common case one is classical, such as X25519, and one is post-quantum, such as
ML-KEM-768. The TLS group named X25519MLKEM768 pairs those two. The combined key
is meant to stay secure if at least one of the components is secure.

NIST IR 8547 describes the reasons. A hybrid is a hedge against a cryptographic or
implementation flaw in one of the components. Early implementations of new
algorithms can contain errors or side-channel weaknesses, and the classical half
covers that risk. A hybrid can also be a path where a sector still requires a
legacy algorithm.

## What NIST allows

For key establishment, NIST currently allows a generic composite technique from
SP 800-56C: the two shared secrets are concatenated and the result is treated as
one secret, from which keys are derived. NIST says it intends to update that
document so the first secret may come from FIPS 203 as well. The technique is
allowed even if the second secret comes from an unapproved source. NIST also says
it will accommodate a hybrid key-establishment mode, and dual signatures, in FIPS
140 validation when suitably combined with an approved scheme.

## The costs

The same section is plain about the downsides. Hybrid solutions add complexity to
implementations and architectures, and that can raise security risks and costs
during the transition. Their security properties can be complex and need to be
analysed case by case. NIST therefore expects hybrids, when used, to be temporary
measures that lead to a second transition to post-quantum algorithms alone.

The practical reading is that a hybrid is a reasonable choice for key exchange
now, where a flaw in the new scheme would be costly and clients already offer it,
and that it should be treated as something to remove again, not as the end state.

## Where to start

NIST's introduction tells organisations to treat migration as a current
operational priority, beginning with cryptographic inventories, migration
planning and early deployments of post-quantum products and services. It also
asks for long-term cryptographic agility, so that updates can follow as standards
change.

Read together with the earlier lessons, that gives an order:

1. **Inventory first.** Find every use of public-key cryptography, including
   inside products you bought. You cannot plan what you have not found.
2. **Key exchange before signatures.** Data in transit can be recorded now. Start
   with whatever carries the longest-lived data.
3. **Signatures where the trust anchor outlives the migration.** Root
   certificates and firmware keys come first.
4. **Make the next change cheaper.** Prefer products where an algorithm is a
   setting, and keep certificate lifetimes short enough to roll naturally.

None of this needs a prediction about quantum hardware. It needs your own numbers
for how long data must stay secret and how long a migration takes, which the
[inequality in the last lesson](/pqc/are-you-already-late/) asks you to write down.
