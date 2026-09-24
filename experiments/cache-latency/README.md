# Experiment 1: a slower L1 cache

**Change:** `--l1d-latency` = 1, 2, 4, 8 cycles (L1 data hit time).
**Keep:** `sequential`, 16,384 words (64 kB), 40 passes, caches on.

## Run

```bash
for cycles in 1 2 4 8; do
  ./run-se.sh sequential cache-latency/$cycles \
    --l1d-latency $cycles --arg 16384 --arg 40
done
```

## Find the counters

```bash
cd results/cache-latency
grep "simInsts" */stats.txt
grep "l1dcaches.demandMissRate::total" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

## Compare

- Instructions and miss rate should be the same in every run: only the hit time changed.
- Does time grow by the same amount at each step?

Plot: `python3 scripts/plot_results.py cache-latency` (needs matplotlib). See [experiment methods](../README.md) for caveats.
