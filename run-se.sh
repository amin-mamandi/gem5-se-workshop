#!/usr/bin/env bash
# Compile one example and run it on gem5.
#
# Usage:   ./run-se.sh <example> [label] [options]
# Example: ./run-se.sh sequential seq-64kB --l1d-size 64kB --arg 16384 --arg 40
#
# <example>  folder in examples/ (sequential), or a file (simple/cpu_walkthrough)
# [label]    output goes to results/<label>; defaults to <example>
# [options]  --arg X, --l1d-size, --l1d-latency, --no-cache
set -euo pipefail
cd "$(dirname "$0")"

example=${1:?Usage: ./run-se.sh <example> [label] [options]}
shift
label=$example
if [[ $# -gt 0 && $1 != --* ]]; then
    label=$1
    shift
fi

# "sequential" means examples/sequential/main.c
src=examples/$example.c
[[ -f $src ]] || src=examples/$example/main.c
[[ -f $src ]] || { echo "No such example: $example" >&2; exit 1; }

out=results/$label

riscv64-linux-gnu-gcc -O2 -std=c11 -Wall -Wextra -fno-tree-vectorize -static -no-pie \
    "$src" -o "${src%.c}-gem5"

mkdir -p "$out"
echo "Running $src -> $out"
./gem5/build/RISCV/gem5.fast --outdir="$out" configs/workshop.py --binary "${src%.c}-gem5" "$@" \
    2>&1 | tee "$out/run.log"

grep -E "^(simSeconds|simInsts) " "$out/stats.txt"
