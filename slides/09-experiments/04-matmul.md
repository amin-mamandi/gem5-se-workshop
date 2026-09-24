---
marp: true
theme: workshop
paginate: true
title: Experiment 4 - matrix loop order
author: Workshop
---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 4: matrix loop order.

**Change:** loop order `ijk` or `ikj`.
**Keep:** 96 × 96 matrices, caches on.

```bash
for order in ijk ikj; do
  ./run-se.sh matmul matmul/$order --arg 96 --arg $order
done
```

**Predict:** which order finishes first in gem5?

<!-- Both orders compute the same product; the checksum proves it. Each run takes about 6 to 8 seconds of host time. To try a bigger matrix, use a new label, for example matmul-128/$order with --arg 128. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Experiment 4: find and compare.

```bash
cd results/matmul
grep "checksum" */run.log
grep "l1dcaches.demandMissRate::total" */stats.txt
grep "simInsts" */stats.txt
grep "simSeconds" */stats.txt
cd ../..
```

Same checksum? Fewer misses, **but more instructions?** Which wins here?

<!-- Our 96 x 96 runs: same checksum (5306681). ikj has 6x fewer L1 data misses (0.05% vs 0.32%) but runs 12% more instructions (8.19 M vs 7.31 M) and finishes later (5.97 ms vs 4.68 ms). All three matrices (about 144 KiB) fit in the 256 kB L2, so misses are cheap here, and this simple CPU pays for every instruction. The host chart used 256 x 256 matrices on a real out-of-order CPU, where ikj won. Ask: what would change the winner in gem5? -->
