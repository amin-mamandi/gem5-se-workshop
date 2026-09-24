# gem5 SE workshop — follow the data

A beginner's workshop about CPUs, caches, and memory, with slides and small C examples.

## 1. Get the workshop

```bash
# Clone and enter repo
git clone https://github.com/amin-mamandi/gem5-se-workshop.git
cd gem5-se-workshop
```

## 2. Show the slides

Needs Node.js 22+.

```bash
# Install the slide tool
npm ci

# Build and serve slides
./show-slides.sh
```

Open http://127.0.0.1:8000/dist/index.html in your browser.

```bash
# Optional: build a PDF
npm run pdf
```

## 3. Install tools (Ubuntu)

```bash
# Install build tools and compiler
sudo apt update
sudo apt install -y build-essential git m4 scons python3-dev python3-venv \
    pkg-config zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev \
    libboost-all-dev libgoogle-perftools-dev \
    gcc-riscv64-linux-gnu libc6-dev-riscv64-cross
```

## 4. Build gem5

Do this before the workshop — it takes a while.

```bash
# Build the simulator once
./build-gem5.sh

# Use fewer jobs if low memory
JOBS=2 ./build-gem5.sh
```

## 5. Run one example

```bash
# Should print 10 + 20 = 30
./run-se.sh simple baseline/simple
```

More examples:

```bash
# Try a few other programs
./run-se.sh simple/cpu_walkthrough walkthrough
./run-se.sh sequential size-64kB --l1d-size 64kB --arg 16384 --arg 40
./run-se.sh matmul matmul/ijk --arg 96 --arg ijk
./run-se.sh matmul matmul/ikj --arg 96 --arg ikj
```

Results go to `results/<name>/`.

## 6. Run all experiments

```bash
# Run every slide experiment
./sweep-se.sh
```

## 7. Look at the results

```bash
# Pull key numbers from stats
grep -irn "simSeconds" results/ --include=stats.txt
grep -irn "simInsts" results/ --include=stats.txt
grep -irn "l1dcaches.demandMissRate::total" results/cache-size/ --include=stats.txt
grep -irn "l2cache.demandMissRate::total" results/ --include=stats.txt
grep -irn "dram.readBursts" results/ --include=stats.txt
grep -irn "readRowHitRate" results/dram-patterns/ --include=stats.txt
```

## 8. Optional: plots

```bash
# Set up plotting environment
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install matplotlib

# Plot one experiment
python3 scripts/plot_results.py cache-size
```

Run `./sweep-se.sh` first. Other experiments: `cache-latency`, `sequential-vs-random`, `matmul`, `dram-patterns`.

## 9. Optional: run on your own machine

```bash
# Build and check native programs
make check
./examples/simple/main
```

## Folders

```text
slides/        slides
examples/      C programs
configs/       simulator setup
scripts/       helper scripts
experiments/   experiment notes
results/       your run outputs
```
