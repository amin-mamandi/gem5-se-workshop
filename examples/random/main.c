#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Invertible mixing permutes indices without an index array. */
int main(int argc, char **argv) {
    size_t n = argc > 1 ? strtoull(argv[1], 0, 10) : 16384;
    int rounds = argc > 2 ? atoi(argv[2]) : 40;
    int write = argc > 3 && strcmp(argv[3], "write") == 0;
    if (argc > 3 && !write && strcmp(argv[3], "read") != 0) return 2;
    if (!n || (n & (n - 1)) || rounds < 1) return 2;
    uint32_t *a = malloc(n * sizeof(*a));
    if (!a) return 3;
    for (size_t i = 0; i < n; ++i) a[i] = (uint32_t)i;
    uint64_t sum = 0;
    const size_t mask = n - 1;
    for (int r = 0; r < rounds; ++r) {
        for (size_t i = 0; i < n; ++i) {
            size_t j = i ^ (i >> 7);
            j = (j * (size_t)0x9e3779b97f4a7c15ULL) & mask;
            j ^= j >> 11;
            if (write) a[j] = (uint32_t)(j + r);
            else sum += a[j];
        }
    }
    if (write)
        for (size_t i = 0; i < n; ++i) sum += a[i];
    printf("sum=%llu mode=%s\n", (unsigned long long)sum,
           write ? "write" : "read");
    free(a);
}
