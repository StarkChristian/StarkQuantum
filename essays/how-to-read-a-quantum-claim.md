# How to read a quantum claim

*Part of [StarkQuantum](../README.md). Independent notes, no vendor affiliation.*

Quantum computing news arrives as press releases, preprints, peer-reviewed papers and conference talks. They carry very different weight. This essay is a practical method for reading any of them.

## Step 1: Find the primary source

Start from the paper, preprint, or technical document, not the article about it. If a claim has no linked primary source, note that. If the source is a company blog post, treat it as a summary written by an interested party, and look for the underlying paper.

Check:

- Is it peer reviewed, a preprint, or neither?
- Are the data and analysis code available?
- Who are the authors, and what are their affiliations and interests?

A preprint is not worse than a journal paper by default, and a journal paper is not automatically right. The point is to know which one you are reading.

## Step 2: State the claim in one plain sentence

Strip the adjectives. "Breakthrough", "revolutionary" and "quantum supremacy" are not claims. A claim looks like: "On device X, a distance-5 surface code had a lower logical error rate per round than a distance-3 code."

If you cannot reduce it to a sentence like that, the claim may not be specific enough to evaluate.

## Step 3: Sort the claim by type

| Type | What it says | What to check |
|------|--------------|---------------|
| Hardware | A device parameter improved | Is it the average or the best case? Over how many qubits and how long? |
| Error correction | Logical error behaviour | Distance trend, rounds, decoder, post-selection |
| Algorithm | A circuit gives a useful result | What is the classical baseline, and was it optimised? |
| Advantage | The quantum device beats classical | On what task, against which classical method, with what verification? |
| Roadmap | A future capability | Is there a dated milestone with measurable criteria? |

Roadmaps are plans, not results. They belong in a different column from experiments.

## Step 4: Check the numbers that are usually missing

- Physical error rates: single-qubit, two-qubit, readout, averaged and worst.
- Number of runs, and the uncertainty. Are there error bars?
- What was discarded or post-selected?
- Circuit depth and number of operations.
- For advantage claims: the best classical algorithm tried, the hardware it ran on, and how long it took.

If a number that a careful reader would need is absent, the absence is information.

## Step 5: Ask what would falsify it

A strong claim can be checked by others. Ask:

- Has it been reproduced independently, or only by the group that made it?
- Could a classical simulation or a cleverer algorithm reproduce the result?
- Is the benchmark relevant to anyone's actual problem, or only designed to be hard?

Earlier advantage claims have been narrowed after improved classical methods appeared. That is normal science working as intended, and it is a reason to wait for scrutiny before calling something settled.

## Step 6: Separate the layers

A single announcement often mixes four different things:

1. **What was measured.** The data.
2. **What it means.** The authors' interpretation.
3. **What it enables.** Speculation about applications.
4. **What will happen.** A forecast.

Reliability falls from the first to the last. Give credit for layer 1, discount layer 2 appropriately, and treat layers 3 and 4 as opinion unless they come with a concrete, checkable plan.

## Red flags

- No primary source, or only a link to another news article.
- A qubit count presented as the headline metric.
- "Logical qubit" used without a code, a distance, or an error rate.
- Comparison with a weak or outdated classical baseline.
- Results shown for the best qubits only.
- Language about "revolutionising" an industry with no problem statement.
- Dates for fault-tolerant machines without milestones that can be checked.

## Green flags

- Clear definition of every term used.
- Scaling trends across several sizes, with uncertainties.
- Data and methods released.
- Honest limitations section.
- Independent replication, or an invitation to it.
- Statements of what was *not* shown.

## Where this fits in StarkQuantum

The [Reality Board](../reality-board/status.md) tracks four plain questions. Each [brief](../briefs/) applies the method above to a single new result. When a claim cannot be placed on the board with evidence, it stays off it.

*Previous: [What a logical qubit is](what-a-logical-qubit-is.md).*
