---
marp: true
theme: workshop
paginate: true
title: Experiment 5 - DRAM jump size
author: Workshop
---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 5: DRAM jump size.

**Change:** jump size = 1, 1025, 32769 words per step.
**Keep:** 1,048,576 words (4 MB), 1 pass, caches on.

```bash
for jump in 1 1025 32769; do
  ./run-se.sh dram-patterns dram-patterns/$jump \
    --cache --arg 1048576 --arg $jump --arg 1
done
```

**Predict:** which jump size gets the most DRAM row hits?

<!-- The 4 MB array is 16 times the 256 kB L2, so reads that miss the caches go to DRAM. A DRAM row holds 8 kB, and consecutive 8 kB pieces of memory go to different banks (2 ranks x 8 banks), so every 128 kB the walk comes back to the same bank, one row further. Jump 1 walks each row in order. Jump 1025 words (4,100 bytes) needs a new row about every second step. Jump 32769 words (128 kB + 4 bytes) lands in the same bank but a different row on every step. Odd jump sizes visit every word once. Each run takes 13 to 22 seconds of host time. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 5: find and compare.

```bash
cd results/dram-patterns
grep "dram.readRowHitRate" */stats.txt
grep "dram.readBursts" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

Fewer row hits, **more time**. Which jump also sends more reads to DRAM?

<!-- Our runs: row hit rate 93% (jump 1), 46% (1025), 5% (32769); DRAM reads 132 K, 133 K, 1.1 M; simulated time 9.7, 21.6, 94.5 ms. Jumps 1 and 1025 read each line from DRAM once and then reuse it from the caches, so they make the same number of DRAM reads; 1025 pays for row misses and for missing the L1 half the time. Jump 32769 misses the caches on almost every step, and nearly every DRAM read is a row conflict (close one row, open another): about 10 times slower than jump 1. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 5: turn the caches off.

```bash
for jump in 1 1025 32769; do
  ./run-se.sh dram-patterns dram-patterns-no-cache/$jump \
    --no-cache --arg 1048576 --arg $jump --arg 1
done
grep "dram.readBursts" results/dram-patterns*/*/stats.txt
```

Compare `--cache` with `--no-cache`: **what did the caches filter out?**

<!-- Our runs: with the caches off, every jump size makes about 17.8 M DRAM reads: 16.8 M instruction fetches plus 1.05 M data reads. Simulated time is about 0.85 s, 9 to 90 times slower than with caches. The row hit rate stays high (88-93%) because the instruction fetches walk the code in order and drown out the jump pattern. The caches do two jobs: they save time, and they filter what DRAM sees. Each run takes about 35 seconds of host time. -->
