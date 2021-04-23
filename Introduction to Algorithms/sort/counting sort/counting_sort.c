#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define print(num, fmt, ...)     {printf_blank(num); printf(fmt, ##__VA_ARGS__);}    

void printf_blank(int num) {
    for (int i = 0; i < num; i++) {
        printf(" ");
    }
}

void counting_sort(int arr[], int sorted_arr[], int len, int k) {
    int *c = (int *)malloc(sizeof(c)*(k+1));
    for (int i=0; i<=k; i++) {
        c[i] = 0;
    }
    for (int i=0; i<len; i++) {
        c[arr[i]] += 1;
    }
    for (int i=1; i<=k; i++) {
        c[i] += c[i-1];
    }
    for (int i = 0; i <= k; i++) {
        printf("| %d ", c[i]);
    }
    printf("\n");
    for (int i=len-1; i>=0; i--) {
        c[arr[i]] -= 1;
        sorted_arr[c[arr[i]]] = arr[i];
    }
    for (int i = 0; i <= k; i++) {
        printf("| %d ", c[i]);
    }
    printf("\n");
}

int main() {
    int arr[] = {3, 0, 2, 3, 2};
    int len = sizeof(arr)/sizeof(int);
    int *sorted_arr = (int *)malloc(sizeof(int)*len);
    counting_sort(arr, sorted_arr, len, 3);
    for(int i=0; i<len; i++) {
        printf("%d ", sorted_arr[i]);
    }
    printf("\n");
}
