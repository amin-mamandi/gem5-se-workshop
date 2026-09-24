---
marp: true
theme: workshop
paginate: true
title: 11 final challenge
author: Workshop
---

<!-- _class: title -->

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Can you make it faster?

**Choose one workload and change one setting.**

Predict. Run. Compare. Explain.

<!-- Participants choose cache size or latency; use the available sweep scripts and save the raw stats. Avoid optimizing for wall-clock gem5 runtime. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## A useful result has a reason.

```text
I changed __________.
The measured __________ changed.
That matters because the CPU __________.
```

<!-- Ask for one sentence that connects a parameter, a statistic, and the CPU wait. Unexpected null result is still a result. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Trace one request for A[5].

![CPU asks the cache for A[5]; a miss reaches DRAM width:970px](../../assets/diagrams/cache-miss.svg)

**Did L1D have it? Did L2? Did the request reach DRAM?**

<!-- A concrete request replaces the old abstract box chain. The picture collapses intermediate levels for legibility; the actual configuration has L1D, then L2. Ask the audience which statistics would help distinguish a hit from a miss. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Take this lab home.

**Edit a module. Change a diagram. Rerun one experiment.**

The source is the presentation.

<!-- Point to the README for Marp, the local RISC-V gem5.opt build, and refreshing SVGs and plots. Ask participants to state the next question they want to test. -->
