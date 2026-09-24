# sequential

Goes over an array from start to end, over and over.

| Arg | Default | What it does |
| --- | --- | --- |
| 1 | 16384 | Array size in words (4 bytes each). Must be a power of two. |
| 2 | 40 | How many times to go over the whole array. |
| 3 | read | `read` sums the array, `write` fills it with new values. |

```bash
# 64 KB array, 40 passes
./run-se.sh sequential seq-read  --arg 16384 --arg 40 --arg read
./run-se.sh sequential seq-write --arg 16384 --arg 40 --arg write
```
