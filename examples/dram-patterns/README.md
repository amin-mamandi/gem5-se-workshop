# dram-patterns

Reads an array by jumping a fixed number of words each step.
Every word is still read once per pass.

| Arg | Default | What it does |
| --- | --- | --- |
| 1 | 16384 | Array size in words (4 bytes each). Must be a power of two. |
| 2 | 1 | Jump size in words. Must be odd. `1` reads in order. |
| 3 | 40 | How many times to read the whole array. |

```bash
# Try different jump sizes
./run-se.sh dram-patterns dram/1    --no-cache --arg 16384 --arg 1    --arg 5
./run-se.sh dram-patterns dram/8191 --no-cache --arg 16384 --arg 8191 --arg 5
```

`--no-cache` skips the caches so every read goes to memory.
