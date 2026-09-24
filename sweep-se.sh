#!/usr/bin/env bash
# Run the examples and the exact parameter choices in slides 08, 09 and 10.
# Sequential runs keep the workshop easy to follow and light on host memory.
# No caches for DRAM strides: a stride alone does not guarantee row conflicts.
# These are whole-program measurements; random also executes extra arithmetic.
set -euo pipefail
cd "$(dirname "$0")"

# Every C example, with its default arguments.
for source in examples/*/*.c; do
    program=${source#examples/}
    program=${program%.c}
    ./run-se.sh "$program" "baseline/$program"
done

# 64 KiB array, 40 passes; change L1D tag/data latency together.
for cycles in 1 2 4 8; do
    ./run-se.sh sequential "cache-latency/$cycles" \
        --l1d-latency "$cycles" --arg 16384 --arg 40
done

# Same input, fixed latency and 256 kB L2; vary only L1D capacity.
for size in 16kB 32kB 64kB 128kB; do
    ./run-se.sh sequential "cache-size/$size" \
        --l1d-size "$size" --arg 16384 --arg 40
done

# 4 MiB arrays, four passes, identical sums.
for program in sequential random; do
    ./run-se.sh "$program" "sequential-vs-random/$program" \
        --arg 1048576 --arg 4
done

for order in ijk ikj; do
    ./run-se.sh matmul "matmul/$order" --arg 96 --arg "$order"
done

for stride in 1 1025 8191; do
    ./run-se.sh dram-patterns "dram-patterns/$stride" \
        --no-cache --arg 16384 --arg "$stride" --arg 5
done

# Restrict recursive grep to stats.txt, excluding config files and logs.
grep -irn "simSeconds" results/ --include=stats.txt
grep -irn "simInsts" results/ --include=stats.txt
grep -irn "l1dcaches.demandMissRate::total" results/ --include=stats.txt
grep -irn "dram.readBursts" results/dram-patterns/ --include=stats.txt
grep -irn "readRowHitRate" results/dram-patterns/ --include=stats.txt
