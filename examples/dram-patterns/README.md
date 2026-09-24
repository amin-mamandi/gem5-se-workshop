# dram-patterns

Reads an array by jumping a fixed number of words each step.
Every word is still read once per pass.

| Arg | Default | What it does |
| --- | --- | --- |
| 1 | 16384 | Array size in words (4 bytes each). Must be a power of two. |
| 2 | 1 | Jump size in words. Must be odd. `1` reads in order. |
| 3 | 40 | How many times to read the whole array. |

```bash
# 4 MB array, one pass
./run-se.sh dram-patterns dram/1     --arg 1048576 --arg 1     --arg 1
./run-se.sh dram-patterns dram/32769 --arg 1048576 --arg 32769 --arg 1
```

Jump `32769` (128 kB + 4 bytes) lands in the same DRAM bank but a new row every step.
Add `--no-cache` to skip the caches, so every read goes to memory.
