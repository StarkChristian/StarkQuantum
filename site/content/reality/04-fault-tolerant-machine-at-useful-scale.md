---
order: 4
question: Fault-tolerant machine at useful scale
status: not-yet
status_label: Not yet
reviewed: 2026-09-08
would_change_it:
  - "A machine executing a user-chosen algorithm of real depth, with error correction active for the full run and a verifiable answer."
  - "Resource estimates and delivered hardware converging, rather than estimates falling while hardware stays flat."
  - "An outside party running their own workload on the machine and getting a correct answer they did not know in advance."
---

A machine that runs an arbitrary algorithm of the user's choosing, long enough
to finish, with error correction holding for the whole run, at a scale where the
algorithm does something worth doing.

This is the end state. Published resource estimates for the canonical
applications — factoring at cryptographic scale, simulating industrially
relevant chemistry — sit in the range of millions of physical qubits with
sustained correction. Current devices are three to four orders of magnitude
short, and the gap is not only in count: it is in error rate, in connectivity,
in classical decoding throughput, and in the cryogenic and control engineering
required to run that many channels at once.

This cell will read not yet for a long time. Watching it change is not the
point; watching cells one and two is. This one moves last.
