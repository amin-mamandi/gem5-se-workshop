# Experiment 2: a bigger L1 cache

**Change:** `--l1d-size` = 16, 32, 64, 128 kB.
**Keep:** `sequential`, 16,384 words (64 kB), 40 passes, caches on.

## Run

```bash
for size in 16kB 32kB 64kB 128kB; do
  ./run-se.sh sequential cache-size/$size \
    --l1d-size $size --arg 16384 --arg 40
done
```

## Find the counters

```bash
cd results/cache-size
grep "l1dcaches.demandMissRate::total" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

## Compare

- At which size does the miss rate drop?
- Does the time drop too? If not, what else was already hiding the misses?

Plot: `python3 scripts/plot_results.py cache-size` (needs matplotlib). See [experiment methods](../README.md) for caveats.
