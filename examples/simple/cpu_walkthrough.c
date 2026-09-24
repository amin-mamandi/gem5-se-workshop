#include <stdio.h>

/* Volatile keeps the example's data reads and writes visible to the compiler.
 * They may still hit in cache rather than reaching physical DRAM. */
volatile int cells[3] = {10, 20, 0};

int main(void) {
    int a = cells[0];
    int b = cells[1];
    int sum = a + b;
    cells[2] = sum;

    if (cells[2] == 30)
        puts("sum = 30");
    else
        puts("unexpected result");
    return 0;
}
