---
title: What a qubit is
slug: what-a-qubit-is
order: 1
script: bloch.js
level: Intro
published: 2026-10-22
reviewed: 2026-10-22
revisions:
  - date: 2026-10-22
    note: Published.
  - date: 2026-10-22
    note: "Added sources and the Bloch sphere; stated that the 2^n growth holds in general."
summary: >-
  A qubit is not a bit that is both 0 and 1. It is a state with two amplitudes,
  and the only thing you ever get out of it is one ordinary bit.
check:
  - q: >-
      A qubit is in the state $(|0\rangle + |1\rangle)/\sqrt{2}$. What does a
      measurement return, and what state is the qubit in afterwards?
    a: >-
      It returns 0 or 1, each with probability one half. Afterwards the qubit is
      in the state that matches the result, so measuring it again gives the same
      answer.
  - q: >-
      Fifty qubits have a state with $2^{50}$ amplitudes. Why does that not mean
      a quantum computer tries $2^{50}$ answers at once?
    a: >-
      Measurement returns one outcome, not the amplitudes. An algorithm is only
      useful if it arranges the amplitudes so that interference makes the wanted
      answer likely when you look.
  - q: Why can you not make a backup copy of an unknown qubit state?
    a: >-
      The no-cloning theorem forbids it. This is the reason quantum error
      correction cannot work like classical redundancy, where you copy the bit.
sources:
  - name: 'Nielsen and Chuang, Quantum Computation and Quantum Information (Cambridge University Press, 2010)'
    note: Chapter 1 and section 2.2 for the state, measurement and entanglement.
  - name: 'Wootters and Zurek, "A single quantum cannot be cloned", Nature 299, 802 (1982)'
    note: The no-cloning theorem.
further:
  - title: A physical qubit is not a computer
    url: /articles/physical-qubit-is-not-a-computer/
    note: What the hardware is, and why the count alone tells you little.
  - title: Glossary, physical qubit
    url: /glossary/#physical-qubit
---

A classical bit is 0 or 1. A qubit is a physical system with two distinguishable
states, which we label $|0\rangle$ and $|1\rangle$, and it can be in a
combination of both.

## The state

The state of one qubit is written $\alpha|0\rangle + \beta|1\rangle$. The two
numbers $\alpha$ and $\beta$ are amplitudes. They can be negative or complex,
and they satisfy $|\alpha|^2 + |\beta|^2 = 1$.

That is the whole description. "Both 0 and 1 at once" is a loose way of
saying that neither amplitude is zero. It does not mean the qubit holds two
values you can read.

A single qubit's state can be drawn as a point on a sphere, the Bloch sphere. The
height of the point sets the two probabilities, and its direction around the
sphere sets the phase. Move the sliders, or pick a named state.

[figure:bloch]

## What measurement does

When you measure the qubit, you get one bit. You get 0 with probability
$|\alpha|^2$ and 1 with probability $|\beta|^2$. The amplitudes themselves are
never handed to you.

Measurement also changes the qubit. After it returns 0, the state is
$|0\rangle$. The superposition is gone. This is why reading a qubit in the
middle of a computation destroys what you were computing, and why quantum
hardware measures at the end, or measures in a carefully chosen way during
error correction.

## Why amplitudes are not probabilities

Probabilities are never negative, so they can only add up. Amplitudes can
cancel. Two routes to the same outcome can have opposite signs and leave
nothing. This is interference, and it is the resource a quantum algorithm uses.

A good algorithm sets up the amplitudes so that the wrong answers cancel and
the right one is left standing. A bad one just produces random bits.

## Many qubits

In general, describing $n$ qubits takes $2^n$ amplitudes. That growth is why
simulating a large quantum computer on a classical one is hard in general, and it
is the source of most of the excitement. Many particular states have a short
description, and those can be simulated cheaply.

It is also the source of the most common misunderstanding. A quantum computer
does not try every answer in parallel and report the best one. It holds a large
state, and you still read out a single bit string. Everything depends on whether
the interference was arranged well.

Qubits can also be entangled: the state of the pair cannot be written as a state
of the first and a separate state of the second. Measuring one then tells you
something about the other. Entanglement is a correlation with no classical
counterpart, and algorithms use it, but it does not carry a message faster than
light.

## What a qubit is made of

Any system with two states that can be prepared, controlled and measured can
serve. The main platforms are superconducting circuits, trapped ions, neutral
atoms held by light, photons, and spins in semiconductors. They differ in
speed, in how well they hold a state, and in how easily one qubit can be made to
interact with another. The field has not settled on one of them.

## One rule that matters later

An unknown quantum state cannot be copied. This is the no-cloning theorem, and
it has a direct consequence. The simplest classical defence against errors,
keeping several copies and taking a vote, is not available. Quantum error
correction needs a different method, and the lessons on noise and error
correction explain it.
