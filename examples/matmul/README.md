# matmul

Multiplies two square matrices. Two loop orders give the same answer,
but touch memory in a different order.

| Arg | Default | What it does |
| --- | --- | --- |
| 1 | 64 | Matrix size N (N × N). Must be 1–512. |
| 2 | ijk | Loop order: `ijk` (slower) or `ikj` (faster). |

```bash
# Compare the two loop orders
./run-se.sh matmul/main matmul/ijk --arg 96 --arg ijk
./run-se.sh matmul/main matmul/ikj --arg 96 --arg ikj
```
