---
marp: true
theme: workshop
paginate: true
title: Experiment 1 - cache latency
author: Workshop
---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 1: a slower L1 cache.

**Change:** `--l1d-latency` = 1, 2, 4, 8 cycles (L1 data hit time).
**Keep:** `sequential`, 16,384 words (64 kB), 40 passes, caches on.

```bash
for cycles in 1 2 4 8; do
  ./run-se.sh sequential cache-latency/$cycles \
    --l1d-latency $cycles --arg 16384 --arg 40
done
```

**Predict:** what happens to time? To misses?

<!-- --l1d-latency sets both the tag and the data latency of the L1 data cache in configs/workshop.py; the response latency stays at the gem5 default. The program and its input are the same in every run. Each run takes about 4 seconds of host time. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 1: find and compare.

```bash
cd results/cache-latency
grep "simInsts" */stats.txt
grep "l1dcaches.demandMissRate::total" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

Same instructions and misses in every run: **only the hit time changed.**
Does time grow by the same amount at each step?

<!-- Our runs: 4,662,071 instructions and a 0.14% L1 data miss rate in all four. Simulated time: 3.37 ms (1 cycle), 3.71 ms (2), 4.39 ms (4), 5.74 ms (8). Time grows linearly: each extra cycle adds 0.34 ms, one cycle for each of the 674,832 L1 data accesses (x 0.5 ns at 2 GHz). The steps double (1, 2, 4), so the increases double: +0.34, +0.68, +1.35 ms. The simple CPU waits for every access, so nothing hides the extra latency. -->
