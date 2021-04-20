#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define print(num, fmt, ...)     {printf_blank(num); printf(fmt, ##__VA_ARGS__);}    

int g_stack[1024] = {0};
int g_index = 1024;

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

void push(int value) {
    if (g_index > 0) {
        g_index--;
        g_stack[g_index] = value;
    }
}

bool pop(int *value) {
    if (g_index < 1024) {
        *value = g_stack[g_index];
        g_index++;
        return true;
    }
    return false;
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
    return k;
}

void quick_sort_recursive(int depth, int arr[], int start, int end) {
    print(depth*4, "%d ~ %d\n", start, end);
    if (start >= end) {
        return;
    }
    int pivot_index = partition(depth, arr, start, end);
    quick_sort_recursive(depth+1, arr, start, pivot_index-1);
    quick_sort_recursive(depth+1, arr, pivot_index+1, end);
}

void quick_sort_iterative(int arr[], int start, int end) {
    if (start >= end) {
        return;
    }
    int left;
    int right;
    push(start);
    push(end);
    while(true) {
        if (!pop(&right) || !pop(&left)) {
            break;
        }
        printf("%d ~ %d\n", left, right);
        if (left >= right) {
            continue;
        }
        int pivot_index = partition(0, arr, left, right);
        push(pivot_index+1);
        push(right);
        push(left);
        push(pivot_index-1);
    }
}

int main() {
    int arr[] = {10, 12, 3, 1, 15, 5, 4, 20, 21, 18};
    int len = sizeof(arr)/sizeof(int);
    // quick_sort_recursive(0, arr, 0, len-1);
    quick_sort_iterative(arr, 0, len-1);
    for(int i=0; i<len+1; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}
