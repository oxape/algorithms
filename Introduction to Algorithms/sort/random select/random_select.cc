#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <random>
#include <time.h>

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

int random_partition(int arr[], int start, int end) {
    int pivot;
    int k;
    // std::default_random_engine e(time(NULL));
    // std::uniform_int_distribution<int> d(start, end);
    // int pivot_index = d(e);
    // swap(arr, start, pivot_index);
    pivot = arr[start];
    k = start;
    for (int j=start+1; j<=end; j++) {
        if (arr[j] < pivot) {
            k++;
            swap(arr, k, j);
        }
    }
    swap(arr, start, k);
    return k;
}

int random_select_recursive(int depth, int arr[], int start, int end, int r) {
    print(depth*8, "%2d ~ %2d\n", start, end);
    if (start == end) {
        return arr[start];
    }
    int pivot_index = random_partition(arr, start, end);
    if (pivot_index == r) {
        return arr[pivot_index];
    }
    if (pivot_index > r) {
        return random_select_recursive(depth+1, arr, start, pivot_index-1, r);
    } else {
        return random_select_recursive(depth+1, arr, pivot_index+1, end, r);
    }
}

int random_select_iterative(int arr[], int start, int end, int r) {
    if (start >= end) {
        return -1;
    }
    int left = start;
    int right = end;
    while(true) {
        if (left >= right) {
            if (left == r) {
                return arr[left];
            } else {
                return arr[right];
            }
        }
        int pivot_index = random_partition(arr, left, right);
        if (pivot_index == r) {
            return arr[pivot_index];
        } 
        if (pivot_index > r) {
            right = pivot_index-1;
        } else {
            left = pivot_index+1;
        }
    }
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
        int pivot_index = random_partition(arr, left, right);
        push(pivot_index+1);
        push(right);
        push(left);
        push(pivot_index-1);
    }
}

int main() {
    int arr[] = {10, 12, 3, 1, 15, 5, 4, 20, 21, 18, 9, 10, 33, 17};
    int len = sizeof(arr)/sizeof(int);
    int tmp[14] = {};
    for (int i = 0; i<len; i++) {
        for (int k = 0; k<len; k++) {
            tmp[k] = arr[k];
        }
        int r = random_select_recursive(0, tmp, 0, len-1, i);
        // int r = random_select_iterative(arr, 0, len-1, i);
        printf("%d at index %d\n", r, i);
    }
    // int r = random_select_recursive(0, arr, 0, len-1, 13);
    quick_sort_iterative(arr, 0, len-1);
    // printf("%d at index %d\n", r, len/2);
    for(int i=0; i<len; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}
