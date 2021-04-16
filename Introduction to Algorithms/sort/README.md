# 排序

## 归并排序

1. 分割时注意界限为<br>
len = end-start<br>
mid = start+len/2<br>
start ~ mid<br>
mid+1 ~ end<br>
注意len不是end-start+1，否则会造成无限递归
2. 递归的终止条件<br>
start <= end
3. 合并时有不变式<br>
A[k-1]内是分割后的两个数组中k-start个最小的元素，且按照从小到大的顺序排列

## 快速排序

1. 分割时注释初始条件<br>
    k=pivot_index; 为了k++后从pivot_index+1的开始 <br>
    满足if (arr[j] < pivot)条件后 <br>
    先执行k++
2. 递归时注意不包括pivot_index<br>
    quick_sort_recursive(depth+1, arr, start, pivot_index-1); <br>
    quick_sort_recursive(depth+1, arr, pivot_index+1, end); <br>

### 快速排序的递归版实现
