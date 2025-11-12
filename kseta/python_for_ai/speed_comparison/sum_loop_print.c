#include <stdio.h>

int main(void) {
    const int N = 10000000;
    long long total = 0;

    for (int i = 0; i < N; i++) {
        total += i;
        printf("%d\n", total);
    }

    printf("Sum: %lld", total);
    return 0;
}
