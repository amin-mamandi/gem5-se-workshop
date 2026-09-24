---
marp: true
theme: workshop
paginate: true
title: 02 cpu and isa
author: Workshop
---

<!-- _class: title -->

## The CPU follows an instruction vocabulary.

Loads get data. Stores save it. Arithmetic changes it. Branches choose what comes next.

<!-- Use a cooking analogy: each instruction is a very small kitchen action; the exact mix depends on compiler and ISA. -->

---

## A clock is a rhythm, not a finish time.

**3 GHz ≈ 3 billion cycles each second.**

One instruction can need multiple cycles; memory can make the CPU wait.

<!-- Avoid saying cycles equal instructions. Approximation is dimensional: GHz means cycles per second. -->

---

## Processors understand different languages.

![isa width:970px](../../assets/diagrams/isa.svg)

x86, Arm, and RISC-V are **instruction set architectures**.

<!-- Explain ISA as the visible contract: the code a processor knows how to execute. Recompile C for a different target ISA. -->

---

## Same language, different designs.

**Two CPUs can run the same x86 program and finish at different times.**

The ISA tells us *what* an instruction means, not how a chip implements it.

<!-- Analogize two people following the same recipe with different kitchens. Do not introduce microarchitecture yet. -->

---

## More instructions per second can mislead.

**MIPS = millions of instructions per second.**

Finishing a job matters more than the rate of counting steps.

<!-- One walker takes five steps, another ten. Ask whether step rate alone settles which arrives first. Compare a fixed task and simulated seconds later. -->
