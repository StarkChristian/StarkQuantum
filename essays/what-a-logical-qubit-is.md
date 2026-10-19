# What a logical qubit actually is

*Part of [StarkQuantum](../README.md). Independent notes, no vendor affiliation.*

"Logical qubit" is one of the most used and most loosely used terms in the field. This essay gives a working definition and a checklist for when a claim deserves the name.

## The idea

Physical qubits are noisy. Error correction spreads one unit of quantum information across many physical qubits, so that errors can be detected and fixed without measuring, and destroying, the stored information. The protected unit is called a **logical qubit**.

A logical qubit is therefore not a better physical qubit. It is an encoded object made of many physical qubits, plus the repeated measurement and classical processing that keep it alive.

## How it works, briefly

- **Encoding.** The state is stored in a code, for example the surface code, in which many data qubits are arranged in a grid with extra measurement qubits between them.
- **Syndrome measurement.** The measurement qubits are read out again and again, in rounds. The results, called syndromes, indicate where errors probably happened without revealing the stored state.
- **Decoding.** A classical computer reads the syndromes and decides which corrections to apply. It has to do this fast enough to keep up with the quantum hardware.
- **Distance.** Larger codes have a larger code distance *d*. If the physical error rate is low enough, increasing *d* suppresses the logical error rate exponentially. This is the whole point.

## The threshold

Error correction only helps if physical errors are below a **threshold**. Below it, a bigger code gives a lower logical error rate. Above it, a bigger code makes things worse, because more qubits means more places for errors to occur.

For the surface code the threshold is commonly quoted at around 1% per operation under simplified noise models. Real devices have messier noise, so the practical margin is smaller than that figure suggests.

## What a convincing claim looks like

Experiments have shown that increasing the code distance can reduce the logical error rate, which is the "below threshold" behaviour. This is real and important. It is also one result, on one kind of operation, at small sizes. Read any logical qubit claim against these questions:

1. **Does the error rate fall as the code grows?** Showing one code size is not enough. Look for at least three code distances and a trend.
2. **Is it measured per round, and over how many rounds?** A logical qubit that survives a few rounds is not a memory.
3. **Is decoding done in real time?** Offline decoding of stored data is a weaker result than correcting errors while the experiment runs.
4. **Are operations performed, or only storage?** A logical memory keeps a state alive. A computer must also apply gates to logical qubits. Logical gates, including the non-Clifford ones needed for universal computation, are a separate and harder problem.
5. **Is post-selection used?** Discarding runs where errors were detected can make results look better. It is sometimes legitimate, but it must be stated, and it does not scale to long computations.
6. **What is the logical error rate in absolute terms?** Useful algorithms need logical error rates far lower than anything demonstrated so far.
7. **How many physical qubits per logical qubit?** Estimates vary with the physical error rate, but often fall in the hundreds to thousands of physical qubits per logical qubit for useful workloads.

## Common ways the term is stretched

- Calling a small error-detecting code, which can only flag errors and discard the run, a logical qubit.
- Counting "logical qubits" that are not simultaneously protected, or that were never operated together.
- Reporting a logical error rate that is still worse than the best physical qubit in the same device.
- Quoting a "logical qubit count" without saying what code, what distance, and what operations.

None of these are necessarily dishonest. They are different things from a fault-tolerant logical qubit, and the difference should be stated.

## Summary

- A logical qubit is an encoded, actively maintained object, not a single device.
- The test is whether errors fall as the code grows, below threshold, measured over many rounds.
- Storage is not computation: logical operations are the next hurdle.
- The number of logical qubits is meaningless without code, distance, error rate and operations.

*Previous: [A physical qubit is not a computer](physical-qubit-is-not-a-computer.md). Next: [How to read a quantum claim](how-to-read-a-quantum-claim.md).*
