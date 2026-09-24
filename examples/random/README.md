# random

Same as `sequential`, but goes over the array in a scrambled order.
Each word is still visited once per pass, so the sum matches `sequential`.

| Arg | Default | What it does |
| --- | --- | --- |
| 1 | 16384 | Array size in words (4 bytes each). Must be a power of two. |
| 2 | 40 | How many times to go over the whole array. |
| 3 | read | `read` sums the array, `write` fills it with new values. |

```bash
# 4 MB array, 4 passes
./run-se.sh random/main rand-read  --arg 1048576 --arg 4 --arg read
./run-se.sh random/main rand-write --arg 1048576 --arg 4 --arg write
```
