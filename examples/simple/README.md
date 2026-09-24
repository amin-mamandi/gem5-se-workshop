# simple

Two tiny programs to check that everything works.

- `main.c` adds 10 + 20 and prints the result.
- `cpu_walkthrough.c` does the same add through memory, for the CPU slides.

No arguments.

```bash
# Prints 10 + 20 = 30
./run-se.sh simple baseline/simple

# Prints sum = 30
./run-se.sh simple/cpu_walkthrough walkthrough
```
