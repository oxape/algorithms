#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stack>
#include <tuple>

#define print(num, fmt, ...)     {printf_blank(num); printf(fmt, ##__VA_ARGS__);}    

using namespace std;

void printf_blank(int num) {
    for (int i = 0; i < num; i++) {
        printf(" ");
    }
}

int min(int x, int y) {
    return x < y ? x : y;
}

void merge_sort_recursive(int depth, int arr[], int reg[], int start, int end) {
    if (depth == 0) {
        printf("merge_sort_recursive\n");
    }
    if (depth > 20) {
        return;
    }
    if (start >= end) {
        print(depth*10, "%2d-%2d return\n", start, end);
        return;
    }
    int len = end-start;
    int mid = len/2 + start;
    
    int start1 = start;
    int end1 = mid;

    int start2 = mid+1;
    int end2 = end;
    print(depth*10, "%2d-%2d %2d-%2d\n", start1, end1, start2, end2);
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
    print(depth*10, "");
    printf("%2d~%2d => ", start, end);
    for (k = start; k <= end; k++) {
        arr[k] = reg[k];
        printf("%d ", arr[k]);
    }
    printf("\n");
}

void merge_sort_iterative(int arr[], const int len) {
    printf("merge_sort_iterative\n");
    int *a = arr;
    int *b = (int *)malloc(len*sizeof(int));
    int seg, start;
    int depth = 0;
    for (seg = 1; seg < len; seg *= 2) {
        for (start=0; start<len; start += seg*2) {
            int end = min(start + seg*2-1 , len-1);
            int l = end - start;
            int mid = start + l/2;
            int start1 = start;
            int end1 = mid;
            int start2 = mid + 1;
            int end2 = end;
            int k = start1;
            print(depth*10, "%2d-%2d %2d-%2d\n", start1, end1, start2, end2);
            while(start1 <= end1 && start2 <= end2) {
                if (a[start1] < a[start2]) {
                    b[k] = a[start1];
                    start1++;
                } else {
                    b[k] = a[start2];
                    start2++;
                }
                k++;
            }
            if (start2 <= end2) {
                while(start2 <= end2) {
                    b[k++] = a[start2++];
                }
            } else {
                while(start1 <= end1) {
                    b[k++] = a[start1++];
                }
            }
            print(depth*10, "");
            printf("%2d ~ %2d => ", start, end);
            for (k=start; k<=end; k++) {
                a[k] = b[k];
                printf("%d ", arr[k]);
            }
            printf("\n");
        }
        depth += 1;
    }
}

void merge_sort_iterative_wiki(int arr[], const int len) {
    printf("merge_sort_iterative_wiki\n");
    int *a = arr;
    int *b = (int *) malloc(len * sizeof(int));
    int seg, start;
    int depth = 0;
    for (seg = 1; seg < len; seg += seg) {
        for (start = 0; start < len; start += seg * 2) {
            int low = start, mid = min(start + seg, len), high = min(start + seg * 2, len);
            int k = low;
            int start1 = low, end1 = mid;
            int start2 = mid, end2 = high;
            print(depth*4, "%d-%d    %d-%d\n", start1, end1-1, start2, end2-1);
            while (start1 < end1 && start2 < end2)
                b[k++] = a[start1] < a[start2] ? a[start1++] : a[start2++];
            while (start1 < end1)
                b[k++] = a[start1++];
            while (start2 < end2)
                b[k++] = a[start2++];
            print(depth*4, "");
            printf("%d ~ %d => ", start, high-1);
            for (k=start; k<high; k++) {
                a[k] = b[k];
                printf("%d ", arr[k]);
            }
            printf("\n");
        }
        int *temp = a;
        a = b;
        b = temp;
        depth += 1;
    }
    if (a != arr) {
        int i;
        for (i = 0; i < len; i++)
            b[i] = a[i];
        b = a;
    }
    free(b);
}

// #define LOG_ACTION_PUSH
// #define LOG_ACTION_POP

void merge_sort_stack_simulative(int arr[], int reg[], int start, int end) {
    printf("merge_sort_stack_simulative\n");
    int depth = 0;
    int state;
    stack< tuple<int, int, int> > s;
#ifdef LOG_ACTION_PUSH
    printf("push  %2d~%2d    %s\n", start, end, "分解");
#endif
    s.push(make_tuple(start, end, 0));
    while (true) {
        if (s.empty()) {
            break;
        }
        auto t = s.top();
        start = get<0>(t);
        end = get<1>(t);
        state = get<2>(t);
        s.pop();
#ifdef LOG_ACTION_POP
        printf("pop   %2d~%2d    %s\n", start, end, state==0?"分解":"合并");
#endif
        switch (state)
        {
        case 0: {
            if (start >= end) {
                continue;
            }
            int len = end-start;
            int mid = len/2 + start;
            
            int start1 = start;
            int end1 = mid;

            int start2 = mid+1;
            int end2 = end;
            depth += 1;
            #ifdef LOG_ACTION_PUSH
                printf("push  %2d~%2d    %s\n", start, end, "合并");
            #endif
            s.push(make_tuple(start, end, 1));
            #ifdef LOG_ACTION_PUSH
                printf("push  %2d~%2d    %s\n", start2, end2, "分解");
            #endif
            s.push(make_tuple(start2, end2, 0));
            #ifdef LOG_ACTION_PUSH
                printf("push  %2d~%2d    %s\n", start1, end1, "分解");
            #endif
            s.push(make_tuple(start1, end1, 0));
        }
            break;
        case 1: {
            depth -= 1;
            int len = end-start;
            int mid = len/2 + start;
            
            int start1 = start;
            int end1 = mid;

            int start2 = mid+1;
            int end2 = end;
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
            print(depth*10, "");
            printf("%2d~%2d => ", start, end);
            for (k = start; k <= end; k++) {
                arr[k] = reg[k];
                printf("%d ", arr[k]);
            }
            printf("\n");
        }
            break;
        default:
            break;
        }
    }
}

void merge_sort(int arr[], const int len) {
    int reg[len];
    // merge_sort_recursive(0, arr, reg, 0, len-1);
    merge_sort_stack_simulative(arr, reg, 0, len-1);
}

int main() {
    int arr[] = {10, 12, 3, 1, 15, 5, 4, 20, 21, 18, 9, 10, 33, 23, 16, 23, 17};
    // int arr[] = {10, 12, 3, 1, 17};
    int len = sizeof(arr)/sizeof(int)-1; //remain last value
    for(int i=0; i<len+1; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    merge_sort(arr, len);
    // merge_sort_iterative(arr, len);
    // merge_sort_iterative_wiki(arr, len);
    for(int i=0; i<len+1; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}
