#include <stdio.h>
#include <stdlib.h>

void swap(int arr[], int a, int b) {
    int tmp;
    tmp = arr[a];
    arr[a] = arr[b];
    arr[b] = tmp;
}

void bubble(int arr[], int start, int end) {
    int diff = end - start;
    for (int i=0; i<diff; i++) {
        for (int j=start; j<end-i; j++) {
            if (arr[j]>arr[j+1]) {
                swap(arr, j, j+1);
            }
        }
    }
}

int partition(int arr[], int p, int r, int x) {
    int k=p-1;
    for (int j=p; j<=r; j++) {
        if (arr[j]<x) {
            k++;
            swap(arr, k, j);
        }
    }
    return k+1;
}

int select(int arr[], int start, int end, int i) {
    if (i<=end-start) {
        bubble(arr, start, end);
        return arr[start+i];
    }
    for (int j=start; j<=end; j+=5) {
        int s = i;
        int e = i+4;
        bubble(arr, s, e);
        swap(arr, start+i/5, s+2);
    }
    // if (i>5) {
       
    // }
    int x = select(arr, start, start+(end-start)/5, (end-start)/5/2);
    int pivot_index = partition(arr, start, end, i);
    if (i+start == pivot_index) {
        return x;
    }
    if (i+start < pivot_index) {
        select(arr, start, pivot_index-1, i);
    } else {
        select(arr, start, pivot_index+1, i-(pivot_index-start+1));
    }
}

int main() {
    int arr[] = {10, 9, 12, 3, 4, 22, 6, 16, 8, 17, 23, 32, 27, 23, 18, 24};
    int len = sizeof(arr)/sizeof(int);
    int index = 8;//(len-1)/2;
    int x = select(arr, 0, len-1, index);
    printf("%d at index %d\n", x, index);
#if 1
    //bubble check
    for (int i = 0; i < len; i++) {
        printf("%2d ", i);
    }
    printf("\n");
    bubble(arr, 0, len-1);
    for (int i = 0; i < len; i++) {
        printf("%2d ", arr[i]);
    }
    printf("\n");
#endif
}