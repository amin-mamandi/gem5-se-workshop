# Experiment 4: matrix loop order

**Change:** loop order, `ijk` or `ikj`.
**Keep:** 96 × 96 matrices, caches on.

## Run

```bash
for order in ijk ikj; do
  ./run-se.sh matmul matmul/$order --arg 96 --arg $order
done
```

## Find the counters

```bash
cd results/matmul
grep "checksum" */run.log
grep "l1dcaches.demandMissRate::total" */stats.txt
grep "simInsts" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

## Compare

- The checksum must match: same answer.
- Which order has fewer misses? Which runs fewer instructions? Which finishes first, and why?

Plot: `python3 scripts/plot_results.py matmul` (needs matplotlib). See [experiment methods](../README.md) for caveats.
