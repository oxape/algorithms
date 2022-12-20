#include <stdio.h>
#include <stdlib.h>

#define log_print(group, depth, ...)    do {if (group) break; int d_d = depth; if (d_d < 0) { d_d * -1; } for (int ddd=0;ddd<d_d*4;ddd++){ printf(" "); } printf("|"); printf(__VA_ARGS__);} while(0)
#define group_print(group, ...)  do {if (group) break; printf(__VA_ARGS__);} while(0)

typedef int array[33];
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

int select(int group, int depth, int arr[], int start, int end, int i, int *index_ptr) {
#ifdef DEBUG
    log_print(group, depth, "%2d~%2d %2d\n", start, end, i);
#endif
    if (group == 0 && depth == 3) {
        asm("NOP");
    }
    //end-start+1等于end到start之间的元素数量，包括end和start
    if (end-start+1<=5) {  //or end-start<5 数量小于等于5直接泡排排序
        bubble(arr, start, end);
        *index_ptr = start+i;
        return arr[start+i];
    }
    for (int j=start; j+4<=end; j+=5) {
        int s = j;
        int e = j+4;
        bubble(arr, s, e);
#ifdef DEBUG
        log_print(group, depth, "[%d-%d]->%d\n", s, e, arr[s+2]);
#endif
        swap(arr, start+(j-start)/5, s+2); //重复利用arr，不另外开辟空间，s+2为中位数的index，第2个(从0开始)
    }
    //处理最后一组不足5个数，其实这里可以忽略掉，因为只在前面的分组中选出中位数也能满足算法时间O(n)
    int remain = (end-start+1)%5;
    if (end-start+1 > 5 && remain > 0) {
        int mid = end-remain+2;
        if (remain < 3) {
            mid = end;
        }
        bubble(arr, end-remain+1, end);
        swap(arr, start+(end-start)/5, mid);
    }
    //把每五个元素的的中位数拿出来，从中选出中位数
#ifdef DEBUG
    log_print(group, depth, "");
    for (int i = start; i <= end; i++) {
        group_print(group, "%2d ", arr[i]);
    }
    group_print(group, "\n");
#endif
    //start+(end-start)/5-1 不包含最后remain的元素, start+(end-start)/5 包含最后remain的元素
    int x = select(1, depth+1, arr, start, start+(end-start+1-4)/5, (end-start+1-4)/5/2, index_ptr); //end-start+1为[start~end]之间元素个数-4之后为了向下取整
#ifdef DEBUG
    log_print(group, depth, "pivot = %d @%d [%d~%d]\n", x, *index_ptr, start, end);
    if (arr[*index_ptr] != x) {
        log_print(group, depth, "xxx\n");
    }
    log_print(group, depth, "");
    for (int i = start; i <= end; i++) {
        group_print(group, "%2d ", arr[i]);
    }
    group_print(group, "\n");
#endif
    swap(arr, end, *index_ptr); //先把pivot放在最后，这样partition结束后它还在最后
#ifdef DEBUG
    log_print(group, depth, "");
    for (int i = start; i <= end; i++) {
        group_print(group, "%2d ", arr[i]);
    }
    group_print(group, "\n");
#endif
    //使用刚刚选出的中位数x作为pivot，执行partition
    int pivot_index = partition(arr, start, end, x);
    swap(arr, end, pivot_index);
#ifdef DEBUG
    log_print(group, depth, "");
    for (int i = start; i <= end; i++) {
        group_print(group, "%2d ", arr[i]);
    }
    group_print(group, "\n");
    log_print(group, depth, "pivot = %d @%d [%d~%d]\n", x, pivot_index, start, end);
#endif
    if (i+start == pivot_index) {
        *index_ptr = pivot_index;
        return x;
    }
    int result;
    if (i+start < pivot_index) {
        result = select(group, depth+1, arr, start, pivot_index-1, i, index_ptr);
    } else {
        result = select(group, depth+1, arr, pivot_index+1, end, i-(pivot_index-start+1), index_ptr);
    }
    return result;
}
//一下为测试代码
int random_uniform(int rangeLow, int rangeHigh) {
    uint32_t value;
    value = 0;
    value = arc4random_uniform(RAND_MAX);
    // value = value >> 1;
    double myRand = (double)value/(RAND_MAX+1.0);
    int range = rangeHigh - rangeLow;
    int myRand_scaled = (myRand * range) + rangeLow;
    return myRand_scaled;
}

int g_arr[] = {151,255,110,267,207,253,124,269,119,299,102,11,186,13,106,201,275,274,200,152,20,127,22,222,174,258,215,246,28,293,175,31,125,282,34,35,184,160,241,294,181,287,42,214,209,45,195,47,218,49,263,122,176,143,54,55,254,57,148,59,60,61,62,262,64,135,108,227,301,196,123,247,171,165,74,75,146,77,182,224,298,266,82,286,251,190,285,103,277,191,154,179,92,153,144,95,141,288,98,290,159};

void test() {
    int group = 0;
    int index;
    int num = random_uniform(100, 10000);
#if 0
    num = sizeof(g_arr)/sizeof(g_arr[0]);
    int *arr = g_arr;
#else
    // num = 101;
    int *arr = (int *)malloc(num*sizeof(int));
    for (int i=0; i<num*3; i++) {
        if (i<num) {
            arr[i] = i;
        } else {
            int index = random_uniform(0, i+1);
            if (index < num) {
                arr[index] = i;
            }
        }
    }
#endif
    int *tmp = (int *)malloc(num*sizeof(int));
    for (int i = 0; i < num; i++) {
        tmp[i] = arr[i];
    }
#ifdef DEBUG
    for (int i = 0; i < num; i++) {
        group_print(group, "%2d ", i);
    }
    group_print(group,"\n");
#endif
    bubble(arr, 0, num-1);
#ifdef DEBUG
    for (int i = 0; i < num; i++) {
        group_print(group, "%2d ", arr[i]);
    }
    group_print(group, "\n");
#endif
    int median_index = (num-1)/2;
    int median = arr[median_index];
    //还原arr数组
    for (int i = 0; i < num; i++) {
        arr[i] = tmp[i];
        // group_print(group, "%d,", tmp[i]);
    }
    // group_print(group, "\n");
    int x = select(0, 0, arr, 0, num-1, median_index, &index);
    // group_print(group, "%d at index %d\n", x, median_index);
    if (x != median) {
        group_print(group, "!!! right median:%d at index %d\n", median, median_index);
    }
    // free(arr);
    free(tmp);
}

int main() {
    for (int i=0; i<1000; i++) {
        // printf("%d\n", i);
        test();
        // break;
    }
    
}
