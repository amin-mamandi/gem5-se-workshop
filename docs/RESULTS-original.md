# Historical results from the original instructor environment

These measurements used a modified gem5 build and a Buildroot compiler before
the standalone repository was created. They are preserved for provenance only.

Measured on 2026-09-23 with `../build/RISCV/gem5.opt` (gem5 25.1.0.0,
local project build) and `./sweep-se.sh`. All **21 runs completed**: the six
C examples with their default arguments, followed by the 15 slide cases below.
Every run has one complete statistics dump, a normal simulator exit, and output
matching the corresponding native C program. Every saved `config.ini` has
`full_system=false`.

The configuration is one RISC-V TimingSimpleCPU at 2 GHz, 256 MiB of addressable
memory, and single-channel DDR3-1600. Cached runs use 32 KiB L1I, 32 KiB L1D
(unless varied), and 256 KiB L2. L1D tag/data latency starts at one cycle;
response latency stays at one cycle. Cache prefetchers retain their defaults.
The DRAM-stride cases bypass all caches. Programs are static RISC-V binaries
compiled with `-O2 -fno-tree-vectorize` using the repository's Buildroot compiler.

These are **whole-program measurements**, including libc, initialization,
the loops, and output. Times below are simulated milliseconds, converted from
`simSeconds`; they are not the host time spent running gem5. Compare settings
within an experiment, which holds the program's input and useful work fixed.

| Experiment | Setting | Simulated ms | Instructions | L1D miss rate | DRAM read bursts |
| --- | --- | ---: | ---: | ---: | ---: |
| L1D tag/data latency | 1 cycle | 1.869 | 2,694,686 | 3.1726% | 1,674 |
| L1D tag/data latency | 2 cycles | 2.236 | 2,694,686 | 3.1721% | 1,670 |
| L1D tag/data latency | 4 cycles | 2.922 | 2,694,686 | 3.1721% | 1,670 |
| L1D tag/data latency | 8 cycles | 4.261 | 2,694,686 | 3.1721% | 1,670 |
| L1D capacity | 16 KiB | 1.869 | 2,694,686 | 3.1726% | 1,674 |
| L1D capacity | 32 KiB | 1.869 | 2,694,686 | 3.1726% | 1,674 |
| L1D capacity | 64 KiB | 1.735 | 2,694,686 | 0.1124% | 1,674 |
| L1D capacity | 128 KiB | 1.734 | 2,694,686 | 0.1072% | 1,674 |
| Access order | sequential | 15.626 | 20,979,163 | 2.7682% | 328,281 |
| Access order | random permutation | 359.094 | 54,533,575 | 80.5244% | 4,241,176 |
| Matrix loop order | ijk | 4.854 | 7,299,743 | 2.0465% | 2,964 |
| Matrix loop order | ikj | 5.687 | 8,175,274 | 1.1405% | 2,964 |

The cache sweeps use 16,384 words × 40 passes (a 64 KiB array); access-order
runs use 1,048,576 words × 4 passes (4 MiB); matrices are 96 × 96.

| DRAM word stride | Simulated ms | Instructions | DRAM read bursts | DRAM row-hit rate |
| --- | ---: | ---: | ---: | ---: |
| 1 | 38.037 | 728,989 | 812,108 | 92.85% |
| 1025 | 38.564 | 729,064 | 812,172 | 88.92% |
| 8191 | 38.044 | 729,064 | 812,184 | 92.84% |

These uncached runs use 16,384 words × 5 passes. The DRAM counters include
instruction fetches and stack accesses as well as array accesses.

What the measurements show:

- Raising L1D tag/data latency from 1 to 8 cycles makes the same work take
  **2.28× longer**, with unchanged instruction count and almost unchanged miss
  rate. Whole-program time does not grow by 8×.
- Increasing L1D from 32 to 64 KiB lowers its miss rate from 3.17% to 0.11%,
  but improves completed-work throughput by only **about 7.7%**. DRAM read
  bursts remain unchanged; the 256 KiB L2 already absorbs much of the traffic.
- Random access takes **22.98× longer**, but it also executes **2.60× as many
  instructions**. The extra index arithmetic and memory behavior both matter.
- **`ikj` is slower in this particular SE experiment**, despite its lower L1D
  miss rate: time is 1.17× higher and instruction count is 1.12× higher. Both
  produce checksum `5306681`, and their DRAM read counts are equal. The host
  charts in the slides use a different machine and input; they do not predict
  this small-matrix TimingSimpleCPU result.
- Stride 1025 has the lowest measured row-hit rate; stride 8191 behaves much
  like stride 1. A large stride alone does not establish row conflicts.

Reproduce from `workshop/`:

```bash
./sweep-se.sh
grep -irn "simSeconds" results/ --include=stats.txt
grep -irn "simInsts" results/ --include=stats.txt
grep -irn "l1dcaches.demandMissRate::total" results/ --include=stats.txt
grep -irn "dram.readBursts" results/ --include=stats.txt
grep -irn "readRowHitRate" results/dram-patterns/ --include=stats.txt
```

The raw outputs are under `results/<experiment>/<setting>/`, and
`results/sweep.log` contains this batch's console output and grep results.
`results/summary.csv` contains the 21-case validation snapshot, including the
baseline examples. This document and CSV record this validation run; the simple
Bash scripts regenerate raw run outputs, not the summary document or CSV.

Use the exact names observed in these stats: a single core produces
`l1dcaches`, without a trailing `0`. `dram.readBursts` selects the DRAM
interface rather than the separate memory-controller counters. Cache miss
rates in `stats.txt` are fractions; `readRowHitRate` is already a percentage.
