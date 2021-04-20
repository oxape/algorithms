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

void max_heapify_recursive(int arr[], int start, int end) {
    int largest_index;
    int parent_index = start;
    int left_child_index = parent_index*2+1;
    int right_child_index = parent_index*2+2;
    if (left_child_index >= parent_index) {
        return;
    }
    if (right_child_index <= end && arr[left_child_index] < arr[right_child_index]) {
        largest_index = right_child_index;
    } else {
        largest_index = left_child_index;
    }
    if (arr[parent_index] >= arr[largest_index]) {
        return;
    }
    swap(arr, parent_index, largest_index);
    max_heapify_recursive(arr, largest_index, end);
}

void max_heapify_iterative(int arr[], int start, int end) {
    int largest_index;
    int parent_index = start;
    int left_child_index = parent_index*2+1;
    int right_child_index = parent_index*2+2;
    while(left_child_index <= end) {
        if (right_child_index <= end && arr[left_child_index] < arr[right_child_index]) {
            largest_index = right_child_index;
        } else {
            largest_index = left_child_index;
        }
        if (arr[parent_index] >= arr[largest_index]) {
            break;
        }
        swap(arr, parent_index, largest_index);
        parent_index = largest_index;
        left_child_index = parent_index*2+1;
        right_child_index = parent_index*2+2;
    }
}

void heap_sort_recursive(int arr[], int start, int end) {
    printf("node = %d\n", (end-1)/2);
    for (int i=(end-1)/2; i>=0; i--) {
        max_heapify_recursive(arr, i, end);
    }
    for(int i=0; i<=end; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    for (int i=end; i>0; i--) {
        swap(arr, 0, i);
        max_heapify_recursive(arr, 0, i-1);
    }
}

void heap_sort_iterative(int arr[], int start, int end) {
    for (int i=(end-1)/2; i>=0; i--) {
        max_heapify_iterative(arr, i, end);
    }
    for (int i=end; i>0; i--) {
        swap(arr, 0, i);
        max_heapify_iterative(arr, 0, i-1);
    }
}

int main() {
    int arr[] = {10, 14, 3, 1, 15, 5, 4, 20, 21, 18, 29, 11, 12, 13};
    int len = sizeof(arr)/sizeof(int);
    // heap_sort_recursive(arr, 0, len-1);
    heap_sort_iterative(arr, 0, len-1);
    for(int i=0; i<len; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}