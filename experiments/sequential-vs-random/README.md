# Experiment 3: sequential vs random order

**Change:** the program, `sequential` or `random`.
**Keep:** 1,048,576 words (4 MB), 4 passes, caches on.
**Try also:** a third argument, `--arg write`, stores instead of reading (use a new label).

## Run

```bash
for program in sequential random; do
  ./run-se.sh $program sequential-vs-random/$program \
    --arg 1048576 --arg 4
done
```

## Find the counters

```bash
cd results/sequential-vs-random
grep "simInsts" */stats.txt
grep "l1dcaches.demandMissRate::total" */stats.txt
grep "dram.readBursts" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

## Compare

- Random runs more instructions (index arithmetic). How much more?
- How much of the time gap is L1 misses and DRAM reads?

Plot: `python3 scripts/plot_results.py sequential-vs-random` (needs matplotlib). See [experiment methods](../README.md) for caveats.
