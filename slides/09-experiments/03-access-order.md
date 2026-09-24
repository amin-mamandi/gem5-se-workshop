---
marp: true
theme: workshop
paginate: true
title: Experiment 3 - access order
author: Workshop
---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 3: sequential vs random order.

**Change:** the program: `sequential` or `random`.
**Keep:** 1,048,576 words (4 MB), 4 passes, caches on.

```bash
for program in sequential random; do
  ./run-se.sh $program sequential-vs-random/$program \
    --arg 1048576 --arg 4
done
```

**Try also:** a third argument, `--arg write`, stores instead of reading.

<!-- The 4 MB array is much bigger than the 256 kB L2, so misses reach DRAM. Both programs visit every element once per pass and compute the same sum. The random run takes about 1.5 minutes of host time, so start it early. For the write version, use a new label so the read runs are kept. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 3: find and compare.

```bash
cd results/sequential-vs-random
grep "simInsts" */stats.txt
grep "l1dcaches.demandMissRate::total" */stats.txt
grep "dram.readBursts" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

Random runs **more instructions**. How much of the gap is misses and DRAM reads?

<!-- Our runs: random executes 62.9 M instructions vs 33.6 M (1.9x, extra index arithmetic). L1 data miss rate 80% vs 0.1%; DRAM reads 4.24 M vs 0.33 M (13x); DRAM row hit rate 1.5% vs 92.7%; simulated time 369 ms vs 24.7 ms (15x). The extra instructions explain about 2x; the rest is waiting for memory. -->
