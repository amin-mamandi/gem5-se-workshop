#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Two loop orders, identical integer matrix product. */
int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : 64;
    int fast = argc > 2 && strcmp(argv[2], "ikj") == 0;
    if (n < 1 || n > 512) return 2;
    size_t count = (size_t)n * n;
    int32_t *a = malloc(count * sizeof(*a));
    int32_t *b = malloc(count * sizeof(*b));
    int64_t *c = calloc(count, sizeof(*c));
    if (!a || !b || !c) return 3;
    for (size_t p = 0; p < count; ++p) {
        a[p] = (int32_t)(p % 7);
        b[p] = (int32_t)(p % 5);
    }
    if (fast) {
        for (int i = 0; i < n; ++i)
            for (int k = 0; k < n; ++k)
                for (int j = 0; j < n; ++j)
                    c[(size_t)i*n+j] +=
                        (int64_t)a[(size_t)i*n+k] * b[(size_t)k*n+j];
    } else {
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                for (int k = 0; k < n; ++k)
                    c[(size_t)i*n+j] +=
                        (int64_t)a[(size_t)i*n+k] * b[(size_t)k*n+j];
    }
    int64_t checksum = 0;
    for (size_t p = 0; p < count; ++p) checksum += c[p];
    printf("checksum=%lld order=%s\n", (long long)checksum,
           fast ? "ikj" : "ijk");
    free(a); free(b); free(c);
}
