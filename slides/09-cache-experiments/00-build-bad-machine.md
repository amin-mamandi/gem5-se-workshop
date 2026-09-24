---
marp: true
theme: workshop
paginate: true
title: 09 cache experiments
author: Workshop
---

<!-- _class: title -->

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Let us make the cache slower.

**L1D hit timing:** `1 → 2 → 4 → 8` cycles

Predict the direction before running.

<!-- The script changes both tag and data latencies. Response latency stays at the gem5 default. Other parameters stay fixed. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## One setting changes each run.

```python
cache.tag_latency = cycles
cache.data_latency = cycles
```

`./sweep-se.sh` — open the script and find the latency loop.

<!-- The script runs all slide experiments. Its first parameter loop changes L1D tag/data timing through workshop.py. Avoid promising a linear total runtime effect. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## What does a larger cache change?

**L1D capacity:** `16 → 32 → 64 → 128 kB`

Our sequential array has **64 KiB** of elements.

<!-- Ask at which size the working set might fit. Other data and mapping complicate the threshold. L2 remains at 256 kB. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## A bigger cache is a hypothesis.

```bash
grep -irn "demandMissRate" results/cache-size/ \
  --include=stats.txt
grep -irn "simSeconds" results/cache-size/
```

Compare **miss rate and time**.

<!-- Run sweep-se.sh first. Focus on l1dcaches.demandMissRate::total; the grep also shows L1I and L2 rates. If miss rate changes but time barely changes, look at reuse, L2 behavior, and instruction overhead. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Access order is our third knob.

```bash
grep -irn "dram.readBursts" results/sequential-vs-random/
grep -irn "simInsts" results/sequential-vs-random/
```

Which misses travel to DRAM?

<!-- The arrays are 4 MiB and the same number of accesses occurs in both programs. Check raw stats for the actual memory burst count. -->
