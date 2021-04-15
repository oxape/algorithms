# 排序

## 归并排序

1. 分割是注意界限为<br>
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

1. 快速排序的递归版实现
2. 