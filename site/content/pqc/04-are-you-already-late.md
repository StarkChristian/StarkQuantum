---
title: Are you already late?
slug: are-you-already-late
order: 4
level: Intro
published: 2026-11-08
reviewed: 2026-11-08
revisions:
  - date: 2026-11-08
    note: Published.
summary: >-
  Mosca's inequality turns the migration question into three numbers: how long
  data must stay secret, how long migration takes, and how long you have.
check:
  - q: >-
      In Mosca's inequality, what does x + y > z mean?
    a: >-
      The time data must stay secret plus the time the migration takes is longer
      than the time until a machine that can break the cryptography. Data sent
      today can then be exposed before it is protected, if the estimate for z
      holds.
  - q: >-
      Data must stay secret for 15 years and migration will take 5. What must be
      true for you not to be late?
    a: >-
      z must exceed 20 years, because x + y is 20. If you cannot say with
      confidence that a capable machine will not exist within 20 years, the
      lever you can pull is y.
sources:
  - name: 'Mosca, "Cybersecurity in an era with quantum computers: will we be ready?", IACR ePrint 2015/1075'
    url: https://eprint.iacr.org/2015/1075
    note: The framing. The abstract was read; the paper also gives a probability estimate for the hardware, which this site does not repeat.
  - name: 'NIST IR 8547, "Transition to Post-Quantum Cryptography Standards" (October 2026)'
    url: https://doi.org/10.6028/NIST.IR.8547
    note: Deprecation after 2030 and disallowance after 2035, and the earlier requirement for high-value federal systems stated in the report.
further:
  - title: What a quantum computer breaks
    url: /pqc/what-a-quantum-computer-breaks/
  - title: Harvest now, decrypt later
    url: /pqc/harvest-now-decrypt-later/
---

## Three numbers

Michele Mosca proposed a way to turn the migration question into one you can
answer. Define three quantities. Let x be how long your data must stay
confidential. Let y be how long your migration to post-quantum cryptography will
take, from the decision to the last system cut over. Let z be how long until a
machine exists that can break the cryptography you use.

If x + y > z, you are already late. Data you send today stays sensitive for x
more years, and you will not finish protecting it for another y. Anything sent in
that window is exposed if the machine arrives within x + y. The inequality does
not say disaster is certain. It says whether your plan has any margin.

## x is the one you know

x is usually larger than the first answer. Ask what the data is, not how long a
database keeps it. A diagnosis is sensitive for a lifetime. A contract is
sensitive for its enforcement period and the limitation period after it. A key
matters for as long as the systems that trust it remain in service. Retention
rules set a floor, not a ceiling.

## y is the one you control

y is consistently underestimated. A realistic migration starts with a
cryptographic inventory: every place public-key cryptography is used, including
inside products you bought and cannot see into. Then come vendor timelines you
do not control, certificate and key lifecycles you have to wait out, embedded
devices that may need replacing, and protocols pinned by partners or standards.

The lever worth pulling is crypto-agility, because it shortens y once and for
all. An organisation that can change an algorithm through configuration, keeps
certificate lifetimes short, and knows where its cryptography lives will migrate
faster now and will not repeat the inventory for the next transition.

## z is the one nobody knows

This site does not give a date for z. Estimates of what a machine would need have
changed a great deal in a few years (see the [first lesson](/pqc/what-a-quantum-computer-breaks/)),
and estimates of when it will exist depend on engineering that has not been shown.

You do not need a date. You need a judgement about whether the machine could
plausibly exist before x + y has passed. Regulators have already set deadlines
that do not depend on that judgement. NIST IR 8547 says quantum-vulnerable
signature and key-establishment algorithms will be deprecated after 2030 and
disallowed under NIST standards after 2035. For federal high-value assets and
other prioritised systems, the report points to earlier deadlines set by the US
Office of Management and Budget, including quantum-resistant key establishment by
31 December 2030. Where such rules apply, the compliance deadline binds before
any machine does.

## A worked example

Suppose your data must stay confidential for 15 years and you estimate a
five-year migration. Then x + y is 20, and the question is whether a capable
machine could exist within 20 years. Many people willing to say "not within ten"
are not willing to say "not within twenty". If you are one of them, you are not
safe, and y is the number you can change.

## Two common mistakes

The first is scoping the inventory to systems you built. That leaves out
purchased software, appliances and anything with an embedded trust anchor, which
is usually the hardest part and has the longest vendor lead times. The second is
treating a dated deadline as provisional. Procurement cycles and hardware refresh
schedules mean the decisions that decide whether you meet 2030 or 2035 are being
made now.
