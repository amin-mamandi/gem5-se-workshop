---
marp: true
theme: workshop
paginate: true
title: Experiment 2 - cache size
author: Workshop
---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 2: a bigger L1 cache.

**Change:** `--l1d-size` = 16, 32, 64, 128 kB.
**Keep:** `sequential`, 16,384 words (64 kB), 40 passes, caches on.

```bash
for size in 16kB 32kB 64kB 128kB; do
  ./run-se.sh sequential cache-size/$size \
    --l1d-size $size --arg 16384 --arg 40
done
```

**Predict:** at which size does the 64 kB array fit?

<!-- The array is 64 kB, but the program also uses a stack and other data, so the threshold is not exact. The L2 stays at 256 kB. gem5 reads 64kB as 64 KiB. Each run takes about 4 seconds of host time. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 2: find and compare.

```bash
cd results/cache-size
grep "l1dcaches.demandMissRate::total" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

Did the miss rate drop? **Did the time drop too?**
If not, what else was already hiding the misses?

<!-- Our runs: L1 data miss rate 0.14% (16 and 32 kB), 0.09% (64 kB), 0.03% (128 kB). Simulated time barely moves: 3.372 ms to 3.367 ms. The array is read in order, so the L1 prefetcher and the 256 kB L2 already hide most misses; a bigger L1 barely helps this program. A bigger cache is a hypothesis, not a guarantee. grep lists the sizes in text order: 128kB comes first. -->
