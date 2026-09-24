# Slide sources and figures

The Bootcamp source conventions were checked against its
[2024 slide README](https://github.com/gem5bootcamp/2024/blob/main/slides/README.md),
[Marp theme](https://github.com/gem5bootcamp/2024/blob/main/slides/themes/gem5.css),
[source example](https://github.com/gem5bootcamp/2024/blob/main/slides/01-Introduction/00-introduction-to-bootcamp.md),
and [slide build workflow](https://github.com/gem5bootcamp/2024/blob/main/.github/workflows/build-slides.yml).
The workshop uses an original, simpler theme and diagrams; it does not bundle
Bootcamp artwork.

The unmodified [official gem5 logo files](https://github.com/gem5/website/tree/stable/assets/img/gem5logo)
also include the editable `assets/images/gem5-master.svg` source; the
[logo guide](https://www.gem5.org/assets/img/gem5logo/gem5styleguide.pdf)
describes spacing and permitted icon use.

## Figures and technical choices

The annotated die image credits its annotator inside the image. The 49% DRAM
cost chart lacks a system configuration, source, and date, so the slide labels
it as an illustrative cost mix rather than a general cost claim. The simulation
config uses upstream gem5.
The experiment config contains split L1 caches and a shared L2. Diagram
captions and notes mark conceptual examples and simplifications. The workshop
uses SE mode only.

DRAM timelines use the DDR3-1600 command parameters in the
[gem5 timing interface](https://gem5.googlesource.com/public/gem5/%2B/master/src/python/gem5/components/memory/dram_interfaces/ddr3.py)
and the [Micron DDR3 datasheet](https://www.alliancememory.com/wp-content/uploads/Micron_2Gb_DDR3_SDRAM_PartNo.MT41J128M16JT-107.pdf).
The 13.75/27.50/41.25 ns comparison is a calculation of idealized
READ-to-first-data paths for an already open row, a closed row, and a
different open row. It assumes PRE can issue immediately and omits the
controller queue, burst transfer, caches, and CPU delay. It is not a
simulated runtime result. The `dram-patterns` experiment measures actual
model behavior when gem5 is available.

The CPU walkthrough draws on [How a CPU Works](https://www.youtube.com/watch?v=cNN_tTXABUA),
especially its explanations of RAM address/read/data signals (03:00–04:00),
instruction types (05:25–06:40), control and the ALU (08:49–10:30), and the
next instruction address (15:36–17:15). The video's teaching CPU omits the
cache hierarchy; the last slide of the cache section adds our model's cache and
memory controller. The pseudoinstructions on slides are teaching labels, not
an exact disassembly of `cpu_walkthrough.c`.

The deck follows the computer hierarchy: CPU first, then caches, and memory
last. The hierarchy slide is adapted from the System Architecture slide in
GEA Presentation 2. The beginner CPU slides (transistors, bits, the
fetch-decode-execute loop, clock speed, cores, and what makes a CPU faster)
draw on [imec's transistor explainer](https://www.imec-int.com/en/semiconductor-education-and-workforce-development/microchips/history-microchips/transistors),
[Khan Academy's bits article](https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:bits-and-bytes/a/bits-binary-digits),
[Fetch, decode, execute (repeat!)](https://www.uvm.edu/~cbcafier/cs2210/content/02_basics_of_architecture/fetch_decode_execute.html),
[CSNewbs on CPU performance](https://www.csnewbs.com/ocr2020-1-2-cpuperformance),
and [Apple's M4 announcement](https://www.apple.com/newsroom/2024/05/apple-introduces-m4-chip/)
for the transistor and core counts.

The gem5 background and build slides use gem5's own
[about page](https://www.gem5.org/about/),
[building guide](https://www.gem5.org/documentation/general_docs/building), and
[standard library overview](https://www.gem5.org/documentation/gem5-stdlib/overview).
They come before the access-pattern results, so the audience meets gem5 before
seeing any measurements.
