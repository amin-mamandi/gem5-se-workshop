# gem5 SE experiments

Local build: **`./gem5/build/RISCV/gem5.fast`**, RISC-V, classic cache hierarchy,
TimingSimpleCPU, SimpleBoard, DDR3_1600_8x8 single channel, 2 GHz.
The config is `configs/workshop.py`; it uses `BinaryResource` and
`set_se_binary_workload`. `./build-gem5.sh` clones the latest upstream source on first
use.
Build native C programs with `make`; `make gem5` builds static RISC-V SE binaries.
The cross compiler is `riscv64-linux-gnu-gcc`. Confirm the ISA with
`file examples/simple/main-gem5`.

```bash
./run-se.sh simple baseline/simple
./sweep-se.sh
grep -irn "simSeconds" results/ --include=stats.txt
grep -irn "readRowHitRate" results/dram-patterns/ --include=stats.txt
```

Run these commands from the repository root. The two Bash scripts compile and run the
examples and save raw outputs under `results/`. Build instructions and VS Code
slide preview steps are in the [workshop README](../README.md).

| Sweep | One change | Workload | Main measurements |
| --- | --- | --- | --- |
| baseline | none | `simple` | `simSeconds` |
| cache-latency | L1D tag/data latency 1, 2, 4, 8 cycles | sequential 16K words × 40 | seconds, L1D misses |
| cache-size | L1D size 16, 32, 64, 128 kB | sequential 16K words × 40 | seconds, L1D misses/accesses |
| sequential-vs-random | access order and index arithmetic | 1M words × 4 | seconds, L1D misses, DRAM reads |
| matmul | `ijk` vs `ikj` loop order | 96 × 96 | seconds, L1D misses |
| dram-patterns | jump size 1, 1025, 8191 words | 16K words × 5, `--no-cache` | seconds, read bursts, row hit rate |
| dram-patterns-cache | same jump sizes | 16K words × 5, `--cache` | read bursts, L1D misses, seconds |

The two access programs perform the same sums. The random order in `random/main.c` is repeatable: it visits
every element exactly once per round but performs extra index arithmetic.
Compare instruction counts alongside misses and time. The `ijk` and
`ikj` matrix loops yield the same checksum; accumulator placement differs.
Both use the same binary architecture, simulated CPU, clock, and DRAM.
Cache experiment results are model observations, not measurements of your
physical CPU. The `dram-patterns` sweep bypasses caches to expose the memory
controller. A stride does **not** promise a row hit or row conflict:
page mapping, channel/bank decoding, open-page policy, request queues, and
initialization affect the outcome. Check measured `readRowHits`, `readBursts`
and `readRowHitRate` before interpreting a bar chart as a row locality effect.
With caches bypassed, these DRAM counters include instruction fetches, stack
accesses, and initialization as well as the array loads.

`scripts/plot_results.py <experiment>` plots the `stats.txt` files that
`sweep-se.sh` saves under `results/<experiment>/`.

All runs finish the program and include initialization and libc. There is no
warmup/reset region. Cache prefetching remains at the upstream hierarchy's defaults;
miss rates therefore reflect its behavior as well as demand locality. Use
`config.ini` to confirm sizes, tag/data timing, response latency, and prefetchers.

The workshop config models split L1 instruction/data and shared L2;
**there is no separate L3; L2 is the last-level cache**. The cache circuitry slides are a simplified
hardware illustration, not a gate-level diagram of gem5's Cache object.
