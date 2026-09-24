#!/usr/bin/env bash
# Compile and run ONE example in syscall-emulation (SE) mode on RISC-V gem5.opt.
# Usage: ./run-se.sh simple/main baseline/simple [workshop.py options]
# The first argument is a source path below examples/, without .c.
# The second names a directory below results/; repeating it replaces that run.
# No instruction/tick limit: these small programs run to completion, including
# initialization and libc. Each parameter comparison must use the same input.
set -euo pipefail
cd "$(dirname "$0")"

program=${1:?Usage: ./run-se.sh simple/main baseline/simple [config options]}
label=${2:?Supply a result name, for example baseline/simple}
shift 2

GEM5_CC=${GEM5_CC:-riscv64-linux-gnu-gcc}
GEM5_BIN=${GEM5_BIN:-./build/RISCV/gem5.opt}
if ! command -v "$GEM5_CC" >/dev/null; then
    echo "Install gcc-riscv64-linux-gnu and libc6-dev-riscv64-cross (see README.md)." >&2
    exit 1
fi
if [[ ! -x "$GEM5_BIN" ]]; then
    echo "Simulator missing: $GEM5_BIN. Run ./build-gem5.sh first." >&2
    exit 1
fi

"$GEM5_CC" \
    -O2 -std=c11 -Wall -Wextra -fno-tree-vectorize -static -no-pie \
    "examples/$program.c" -o "examples/$program-gem5"

mkdir -p "results/$label"
echo "Running $program -> results/$label"
"$GEM5_BIN" --outdir="results/$label" \
    configs/workshop.py --binary "examples/$program-gem5" "$@" \
    2>&1 | tee "results/$label/run.log"

grep -irn "simSeconds" "results/$label/stats.txt"
grep -irn "simInsts" "results/$label/stats.txt"
