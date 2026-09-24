#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* Power-of-two words; odd stride visits every word exactly once. */
int main(int argc, char **argv) {
    size_t n = argc > 1 ? strtoull(argv[1], 0, 10) : 16384;
    size_t step = argc > 2 ? strtoull(argv[2], 0, 10) : 1;
    int rounds = argc > 3 ? atoi(argv[3]) : 40;
    if (!n || (n & (n - 1)) || !(step & 1) || rounds < 1)
        return 2;
    uint32_t *a = malloc(n * sizeof(*a));
    if (!a) return 3;
    for (size_t i = 0; i < n; ++i) a[i] = (uint32_t)i;
    uint64_t sum = 0;
    for (int r = 0; r < rounds; ++r) {
        size_t i = 0;
        for (size_t count = 0; count < n; ++count) {
            sum += a[i];
            i = (i + step) & (n - 1);
        }
    }
    printf("sum=%llu stride=%zu\n", (unsigned long long)sum,
           step);
    free(a);
}
