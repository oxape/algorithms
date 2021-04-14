#include <stdio.h>

void merge_sort_recursive(int depth, int arr[], int reg[], int start, int end) {
    if (start >= end) {
        return;
    }
    int len = end-start;
    int mid = len/2 + start;
    
    int start1 = start;
    int end1 = mid;

    int start2 = mid+1;
    int end2 = end;
    merge_sort_recursive(depth+1, arr, reg, start1, end1);
    merge_sort_recursive(depth+1, arr, reg, start2, end2);

    int k = start;
    while(start1 <= end1 && start2 <= end2) {
        if (arr[start1] < arr[start2]) {
            reg[k] = arr[start1];
            start1++;
        } else {
            reg[k] = arr[start2];
            start2++;
        }
        k++;
    }
    if (start1 <= end1) {
        while(start1 <= end1) {
            reg[k++] = arr[start1++];
        }
    } else {
        while(start2 <= end2) {
            reg[k++] = arr[start2++];
        }
    }
    for (k = start; k <= end; k++)
        arr[k] = reg[k];
}

void merge_sort(int arr[], const int len) {
    int reg[len];
    merge_sort_recursive(0, arr, reg, 0, len-1);
}

int main() {
    int arr[] = {10, 12, 3, 1, 15, 5, 4, 20, 21, 18};
    int len = sizeof(arr)/sizeof(int)-1;
    merge_sort(arr, len);
    for(int i=0; i<len+1; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}