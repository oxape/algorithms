#include <stdio.h>
#include <stdlib.h>

#define print(num, fmt, ...)     {printf_blank(num); printf(fmt, ##__VA_ARGS__);}    

void printf_blank(int num) {
    for (int i = 0; i < num; i++) {
        printf(" ");
    }
}

void swap(int arr[], int a, int b) {
    int tmp;
    tmp = arr[b];
    arr[b] = arr[a];
    arr[a] = tmp;
}

int partition(int depth, int arr[], int start, int end) {
    int pivot = arr[start];
    int k=start;
    for (int j=start+1; j<=end; j++) {
        if (arr[j] < pivot) {
            k++;
            swap(arr, k, j);
        }
    }
    swap(arr, start, k);
    print(depth*4, "%d ~ %d ~ %d\n", start, k, end);
    return k;
}

void quick_sort_recursive(int depth, int arr[], int start, int end) {
    if (start >= end) {
        return;
    }
    int pivot_index = partition(depth, arr, start, end);
    quick_sort_recursive(depth+1, arr, start, pivot_index-1);
    quick_sort_recursive(depth+1, arr, pivot_index+1, end);
}

int main() {
    int arr[] = {10, 12, 3, 1, 15, 5, 4, 20, 21, 18};
    int len = sizeof(arr)/sizeof(int)-1;
    quick_sort_recursive(0, arr, 0, len-1);
    for(int i=0; i<len+1; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}