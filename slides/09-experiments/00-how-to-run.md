---
marp: true
theme: workshop
paginate: true
title: Experiments
author: Workshop
---

<!-- _class: title -->

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Five experiments on one machine.

**Run** a loop. **Find** the counters. **Compare** the runs.

<!-- Each experiment has a folder under experiments/, and its results land in results/<experiment>/. ./sweep-se.sh runs every loop on these slides in one go. Load the RISC-V compiler and build gem5 first. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Every run is one command.

```bash
./run-se.sh <example> <label> [settings] --arg <value> ...
```

| Setting | What it changes |
| --- | --- |
| `--arg X` | one program argument (repeat it) |
| `--l1d-latency N` | L1 data hit time in cycles (default 1) |
| `--l1d-size S` | L1 data size, like `64kB` (default 32kB) |
| `--cache` / `--no-cache` | caches on (default) or off |

Results go to `results/<label>/stats.txt`.

<!-- run-se.sh compiles examples/<example>/main.c for RISC-V and runs it on gem5 with configs/workshop.py. Everything after the label goes to the config. Reusing a label replaces that run. --no-cache removes both L1 caches and the L2, so even instruction fetches go to DRAM. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Counters we read in stats.txt.

| Counter | What it means |
| --- | --- |
| `simSeconds` | simulated time |
| `simInsts` | instructions run |
| `l1dcaches.demandMissRate::total` | L1 data miss rate (0 to 1) |
| `l2cache.demandMissRate::total` | L2 miss rate (0 to 1) |
| `dram.readBursts` | DRAM reads |
| `dram.readRowHitRate` | DRAM row hit rate (%) |

**Compare in this order:** instructions → misses → DRAM reads → time.

<!-- The full names start with board.cache_hierarchy or board.memory.mem_ctrl; grep matches the end of the name, and each counter appears once per stats.txt. Miss rates are fractions: 0.8 means 80%. The row hit rate is already a percentage. Instructions come first: if the program runs more instructions, it takes longer even with a perfect memory. -->
