# Brief: Logical memory with a growing code distance (SAMPLE)

> **This is a fictional sample brief.** The group, device, paper and numbers below are invented to show the format. It does not describe a real result. Real briefs will cite a real primary source.

| Field | Entry |
|-------|-------|
| Date | 2026-10-19 |
| Source | *(fictional)* Preprint, "Repeated logical memory in a surface code up to distance 7" |
| Source type | Preprint, not peer reviewed |
| Platform | Superconducting qubits |
| Claim type | Error correction |
| Reality Board question | Stable, repeated error correction below threshold |

## The claim in one sentence

On one device, the logical error rate per round of a surface-code memory fell as the code distance grew from 3 to 5 to 7.

## What was measured

- Logical memory only. No logical gates were applied.
- Repeated syndrome measurement for 25 rounds.
- Decoding was done offline, after the runs.
- Logical error per round was reported for three code distances, with uncertainties.

## What was not shown

- Real-time decoding.
- Logical operations such as a gate or a state injection.
- Results on more than one device or on more than one day.
- Any computation that gives a useful answer.

## Questions to check against the paper

1. Is the trend across distances consistent, with error bars that do not overlap?
2. Was post-selection used, and how many runs were discarded?
3. How does the logical error per round compare with the best physical qubit on the same chip?
4. Are data and analysis code available?
5. Has another group reproduced it?

## Assessment

A clean trend across three distances is the right kind of evidence for below-threshold behaviour. It supports the "Early" status on the Reality Board. It does not move the other three rows: storage is not computation, offline decoding is not real-time correction, and one device is not a repeated result.

**Board impact:** None. Status stays *Early*.

**What would change the assessment:** a repeat on a second device, real-time decoding, and a logical operation performed within the same code.

---

*Method: [How to read a quantum claim](../essays/how-to-read-a-quantum-claim.md). Board: [Reality Board](../reality-board/status.md).*
