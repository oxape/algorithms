#include <stdio.h>
#include <stdlib.h>

// #define DEBUG

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
#ifdef DEBUG
    printf("%2d~%2d %2d\n", start, end, i);
#endif
    if (end-start<5) {
        bubble(arr, start, end);
#ifdef DEBUG
        for (int k = start; k <= end; k++) {
            printf("%2d ", arr[k]);
        }
        printf("\n");
#endif
        return arr[start+i];
    }
    for (int j=start; j+4<=end; j+=5) {
        int s = j;
        int e = j+4;
        bubble(arr, s, e);
        swap(arr, start+j/5, s+2);
    }
    // if (i>5) {
       
    // }
    int x = select(arr, start, start+(end-start-4)/5, (end-start)/5/2);
#ifdef DEBUG
    for (int k = start; k <= end; k++) {
        printf("%2d ", arr[k]);
    }
    printf("\n");
#endif
    int pivot_index = partition(arr, start, end, x);
#ifdef DEBUG
    printf(" x = %2d pivot_index = %2d\n", x, pivot_index);
    for (int k = start; k <= end; k++) {
        printf("%2d ", arr[k]);
    }
    printf("\n");
#endif
    if (i+start == pivot_index) {
        return x;
    }
    if (i+start < pivot_index) {
        return select(arr, start, pivot_index-1, i);
    } else {
        return select(arr, pivot_index+1, end, i-(pivot_index-start+1));
    }
}

int main() {
    int arr[] = {10, 9, 12, 3, 4, 22, 6, 16, 8, 17, 23, 32, 27, 25, 18, 24};
    int len = sizeof(arr)/sizeof(int);
    int *tmp = (int *)malloc(len);

    for (int i = 0; i < len; i++) {
        tmp[i] = arr[i];
    }
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
    for (int index=0; index<len; index++) {
        for (int i = 0; i < len; i++) {
            // printf("%2d ", tmp[i]);
            arr[i] = tmp[i];
        }
        // printf("\n");

        // int index = 8;//(len-1)/2;
        int x = select(arr, 0, len-1, index);
        printf("%d at index %d\n", x, index);
    }
    int index = 8;//(len-1)/2;
    int x = select(arr, 0, len-1, index);
    printf("%d at index %d\n", x, index);
    free(tmp);
}