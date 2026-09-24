---
marp: true
theme: workshop
paginate: true
title: A virtual computer lab
author: Workshop
---

<!-- _class: title -->

<img class="gem5-brand gem5-brand-feature" src="../../assets/images/gem5-logo.png" alt="gem5 logo" />

## What if we could change the machine?

![A program and hardware settings separately feed gem5, which writes statistics width:1000px](../../assets/diagrams/gem5-workflow.svg)

**gem5 runs the program on a model we choose.**

<!-- Point to two separate inputs: the program runs, while the settings describe the modeled CPU, cache, and DRAM. stats.txt reports what happened in that model. No laptop hardware was changed. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## What is gem5?

**An open-source computer simulator**, used in universities and industry.

It models a whole computer in software: CPU, caches, and memory.

It began in 2011 by joining two simulators: **M5** (University of Michigan) and **GEMS** (University of Wisconsin).

<!-- gem5 describes itself as "a modular platform for computer-system architecture research, encompassing system-level architecture as well as processor microarchitecture." The name joins GEMS and M5. It uses a Berkeley-style open-source license. Source: https://www.gem5.org/about/ . This workshop was tested with gem5 v25.1. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## gem5 can model many machines.

**ISAs:** x86, Arm, RISC-V, and more.

**CPU models:** from simple to very detailed.

**Memory:** caches and many kinds of DRAM.

**Two modes:** Syscall Emulation (SE) runs one program. Full System (FS) boots an operating system.

<!-- CPU models range from a simple one-instruction-per-cycle model to detailed in-order and out-of-order cores. The DRAM controller supports DDR3/4, LPDDR, GDDR, and HBM families. This workshop uses SE mode only: no operating system to boot, so runs are short. Source: https://www.gem5.org/about/ . -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## A Python script describes the machine.

```python
board = SimpleBoard(
    clk_freq="2GHz",
    processor=SimpleProcessor(
        cpu_type=CPUTypes.TIMING, isa=ISA.RISCV, num_cores=1),
    memory=SingleChannelDDR3_1600(size="256MiB"),
    cache_hierarchy=cache,
)
```

We pick the parts in **Python**. gem5's **C++** core simulates them.

<!-- This is the actual board in configs/workshop.py; cache is the private-L1/shared-L2 hierarchy, or no cache for the DRAM experiment. The gem5 standard library provides ready-made boards, processors, cache hierarchies, and memory, so "users can build complex systems from simple components which connect together using standardized APIs." Source: https://www.gem5.org/documentation/gem5-stdlib/overview . -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Build gem5 once.

```bash
git clone https://github.com/gem5/gem5.git
cd gem5
scons build/RISCV/gem5.fast -j 4
```

**RISCV** picks the ISA. **fast** runs quickest. **-j 4** compiles 4 files at a time.

Or run `./build-gem5.sh`. Result: `gem5/build/RISCV/gem5.fast`

<!-- gem5 has three build variants: debug (no optimizations; easiest in gdb, much slower), opt (optimized, keeps asserts and debug prints), and fast (optimized, debugging compiled out). Building takes a long time: "a single-threaded compilation from scratch can take up to 2 hours on some systems", and more jobs use more memory. Build before the workshop. Requirements include git, gcc 10 or newer (or Clang), SCons, Python 3, protobuf, and Boost. build-gem5.sh installs the Ubuntu packages and the RISC-V compiler, builds the example programs, clones gem5, and runs this scons command. Source: https://www.gem5.org/documentation/general_docs/building . -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Our one modeled computer.

- **CPU:** one RISC-V core at 2 GHz (TimingSimpleCPU)
- **Caches:** L1 instruction and L1 data (32 kB each), shared L2 (256 kB)
- **Memory:** DDR3 DRAM
- **Mode:** Syscall Emulation (SE)

We will vary one part at a time.

<!-- This is the actual structure in configs/workshop.py. TimingSimpleCPU is gem5's simple CPU model that waits for each memory access to finish, so memory delays show up directly in the time. The separate L1 instruction cache exists but the visual request path elsewhere follows data through L1D. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Simulation has limits.

**A model can explain a trend. It is not a physical benchmark.**

We compare like-for-like runs within this configuration.

<!-- Model fidelity, workload, ISA target, and calibration matter. Simulated seconds differ from the wall time taken by gem5 itself. -->
