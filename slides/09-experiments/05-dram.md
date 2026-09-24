---
marp: true
theme: workshop
paginate: true
title: Experiment 5 - DRAM jump size
author: Workshop
---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 5: DRAM jump size.

**Change:** jump size = 1, 1025, 8191 words per step.
**Keep:** 16,384 words, 5 passes, **caches off** (`--no-cache`).

```bash
for jump in 1 1025 8191; do
  ./run-se.sh dram-patterns dram-patterns/$jump \
    --no-cache --arg 16384 --arg $jump --arg 5
done
```

**Predict:** which jump size gets the most DRAM row hits?

<!-- With the caches off, every access goes to the memory controller, so the DRAM counters see the access pattern directly. Odd jump sizes visit every word once per pass. Each run takes about 2 seconds of host time. -->

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

The row hit rates differ only a little. **Why?** Count the DRAM reads.

<!-- Our runs: row hit rate 92.8% (jump 1), 89.2% (1025), 92.2% (8191); simulated time about 50.5 ms for all three; about 1.08 M DRAM reads each. Only 82 K of those reads are the array: with the caches off, every instruction fetch (730 K instructions) also goes to DRAM and dominates the traffic. Page and bank mapping also shape the row hits. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 5: turn the caches back on.

```bash
for jump in 1 1025 8191; do
  ./run-se.sh dram-patterns dram-patterns-cache/$jump \
    --cache --arg 16384 --arg $jump --arg 5
done
grep "dram.readBursts" results/dram-patterns*/*/stats.txt
```

Compare `--cache` with `--no-cache`: **what did the caches hide?**

<!-- Our runs: DRAM reads fall from about 1,077,000 to 1,635 with caches on: the 64 kB array fits in the 256 kB L2, and instructions hit in the L1 instruction cache. Simulated time falls from about 50 ms to 0.6-1.1 ms. With caches, jump 1025 takes about twice as long as jump 1 (1.11 ms vs 0.58 ms): it misses the L1 data cache 81% of the time vs 0.3%, so the jump pattern now shows up in the caches instead of in DRAM. -->
