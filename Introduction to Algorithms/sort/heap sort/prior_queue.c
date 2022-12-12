#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define PRIOR_QUEUE_SIZE        64
#define PRIOR_QUEUE_HANDLE      

#define PARENT(i)   (((i)-1)>>1)

typedef struct tag_handle {
    int ower;
} prior_queu_handle_t;

typedef struct prior_queue {
    int size; //最大容量
    int len; //当前大小
    int32_t key_arr[PRIOR_QUEUE_SIZE];
    void *handle_arr[PRIOR_QUEUE_SIZE];
} prior_queue_t;

static prior_queue_t g_prior_queue;

void swap(int arr[], int a, int b) {
    int tmp;
    tmp = arr[b];
    arr[b] = arr[a];
    arr[a] = tmp;
}

void min_heap_iterative(prior_queue_t *prior_queue, int start, int end) {
    int largest_index;
    int parent_index = start;
    int left_child_index = (parent_index<<1)+1;
    int right_child_index = (parent_index<<1)+2;
    while(left_child_index <= end) {
        if (right_child_index <= end && prior_queue->key_arr[left_child_index] > prior_queue->key_arr[right_child_index]) {
            largest_index = right_child_index;
        } else {
            largest_index = left_child_index;
        }
        if (prior_queue->key_arr[parent_index] <= prior_queue->key_arr[largest_index]) {
            break;
        }
        swap(prior_queue->key_arr, parent_index, largest_index);
        parent_index = largest_index;
        left_child_index = (parent_index<<1)+1;
        right_child_index = (parent_index<<1)+2;
    }
}

int32_t heap_min(prior_queue_t *prior_queue) {
    return prior_queue->key_arr[0];
}

int32_t heap_extract_min(prior_queue_t *prior_queue) {
    int32_t min;
    if (prior_queue->len < 1) {
        return -1;
    }
    min = prior_queue->key_arr[0];
    prior_queue->key_arr[0] = prior_queue->key_arr[prior_queue->len-1];
    prior_queue->len -= 1;
    if (prior_queue->len > 0) {
        min_heap_iterative(prior_queue, 0, prior_queue->len-1);
    }
    return min;
}

void heap_decrease_key(prior_queue_t *prior_queue, int i, int32_t key) {
    if (key > prior_queue->key_arr[i]) {
        return;
    }
    prior_queue->key_arr[i] = key;
    int parent_index = PARENT(i);
    while (i > 0 && prior_queue->key_arr[parent_index] > prior_queue->key_arr[i]) {
        swap(prior_queue->key_arr, parent_index, i);
        i = PARENT(i);
        parent_index = PARENT(i);
    }
}

void min_heap_insert(prior_queue_t *prior_queue, int32_t key) {
    prior_queue->len += 1;
    prior_queue->key_arr[prior_queue->len-1] = INT32_MAX;
    heap_decrease_key(prior_queue, prior_queue->len-1, key);
}

int main() {
    int arr[] = {10, 14, 3, 1, 15, 5, 4, 20, 21, 18, 29, 11, 12, 9, 6};
    int len = sizeof(arr)/sizeof(int);
    // heap_sort_iterative(arr, 0, len-1);
    g_prior_queue.len = 0;
    for(int i=0; i<len; i++) {
        min_heap_insert(&g_prior_queue, arr[i]);
    }
    for(int i=0; i<len; i++) {
        int32_t min = heap_extract_min(&g_prior_queue);
        printf("%d\n", min);
    }
    printf("\n");
}
