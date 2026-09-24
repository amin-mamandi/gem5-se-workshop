# Experiment 5: DRAM jump size

**Change:** jump size = 1, 1025, 32769 words per step.
**Keep:** 1,048,576 words (4 MB), 1 pass, caches on (`--cache`), then caches off (`--no-cache`).

The 4 MB array is 16 times the L2, so cache misses reach DRAM. A DRAM row holds
8 kB, and every 128 kB the addresses come back to the same bank one row further,
so a jump of 32769 words (128 kB + 4 bytes) opens a new row in the same bank on
every step.

## Run

```bash
for jump in 1 1025 32769; do
  ./run-se.sh dram-patterns dram-patterns/$jump \
    --cache --arg 1048576 --arg $jump --arg 1
done

for jump in 1 1025 32769; do
  ./run-se.sh dram-patterns dram-patterns-no-cache/$jump \
    --no-cache --arg 1048576 --arg $jump --arg 1
done
```

With caches on, each run takes about 13–22 seconds; with caches off, about 35 seconds.

## Find the counters

```bash
cd results/dram-patterns
grep "dram.readRowHitRate" */stats.txt
grep "dram.readBursts" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
grep "dram.readBursts" results/dram-patterns*/*/stats.txt
```

## Compare

- With caches on: which jump size gets the most row hits? Which one also sends more reads to DRAM?
- With caches off: why does the row hit rate barely change? What did the caches filter out?

Plot: `python3 scripts/plot_results.py dram-patterns` or `dram-patterns-no-cache` (needs matplotlib). See [experiment methods](../README.md) for caveats.
