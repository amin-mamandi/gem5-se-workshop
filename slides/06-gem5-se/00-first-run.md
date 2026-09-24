---
marp: true
theme: workshop
paginate: true
title: gem5 SE
author: Workshop
---

<!-- _class: title -->

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Let us run one program.

**Syscall Emulation (SE)** runs a user program with modeled CPU and memory.

No operating system boot is required.

<!-- Define syscall in plain language as asking the host to perform some OS services. This workshop uses SE only. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## First compile the tiny program.

```bash
make all
./examples/simple/main
```

Expected output: **10 + 20 = 30**

<!-- Start in the workshop repository root. This first command runs a native host binary. The next slide's Bash script compiles a separate static RISC-V binary with riscv64-linux-gnu-gcc. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Then run it through gem5.

```bash
./run-se.sh simple baseline/simple
```

Result: `results/baseline/simple/stats.txt`

<!-- Uses ./gem5/build/RISCV/gem5.fast. Run build-gem5.sh once first. The run script compiles examples/simple/main.c, runs it in SE, and saves run.log plus config.ini and stats.txt. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Find one number: simulated time.

```bash
grep -irn "simSeconds" results/ --include=stats.txt
```

Find it in `stats.txt`. What does it measure?

<!-- Explain that this is elapsed time in the simulated machine, distinct from the wall time spent waiting for gem5. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Ask why before opening more stats.

**Why is the next version slower or faster?**

Check instruction count, cache misses, DRAM reads, then time.

<!-- This evidence sequence guards against attributing an instruction-count change solely to memory. -->
