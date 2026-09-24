---
marp: true
theme: workshop
paginate: true
title: Waiting for memory
author: Workshop
---

<!-- _class: title -->

## The CPU needs A[5]. It may have to wait.

![Illustrative work and wait timeline width:970px](../../assets/diagrams/cpu-wait.svg)

**The value must arrive before the CPU can use it.**

<!-- The timeline is schematic, not to scale. A request may hit in cache or travel farther; this asks what waiting feels like before we introduce the cache. -->

---

## Can we keep useful data closer?

**Imagine your desk and a library.**

Desk: frequently used books nearby.
Library: more books, farther away.

<!-- Call this an analogy. The actual hardware uses cache lines and a request hierarchy. Let the next section reveal what the nearby place is called. -->
