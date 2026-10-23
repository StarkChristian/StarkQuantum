---
term: Code distance
slug: code-distance
---

The smallest number of physical errors that can change a logical state without
being detected. A code of odd distance $d$ is guaranteed to correct any $(d-1)/2$
errors or fewer.

A larger distance protects better and costs more qubits: a rotated surface-code
patch of distance $d$ uses $2d^2-1$ physical qubits. Whether a larger distance
helps at all depends on the physical error rate being below the threshold.
