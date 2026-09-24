# Experiment 5: DRAM jump size

**Change:** jump size = 1, 1025, 8191 words per step.
**Keep:** 16,384 words, 5 passes, caches off (`--no-cache`), then caches on (`--cache`).

## Run

```bash
for jump in 1 1025 8191; do
  ./run-se.sh dram-patterns dram-patterns/$jump \
    --no-cache --arg 16384 --arg $jump --arg 5
done

for jump in 1 1025 8191; do
  ./run-se.sh dram-patterns dram-patterns-cache/$jump \
    --cache --arg 16384 --arg $jump --arg 5
done
```

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

- Which jump size gets the most row hits with caches off? Why do the rates differ only a little?
- With caches on, how many DRAM reads are left? What did the caches hide?

Plot: `python3 scripts/plot_results.py dram-patterns` or `dram-patterns-cache` (needs matplotlib). See [experiment methods](../README.md) for caveats.
