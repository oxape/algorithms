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

观察代码和输出可以发现，递归版快速排序的执行顺序，类似于先序遍历。分割后先递归快排序做左子树，知道左子树，触发递归终止条件，层层返回之后，同样递归排序右子树。<br>
所以可以利用栈，先压栈右子树，后压栈左子树，出栈时顺序相反，由于左子树出栈后如果不触发终止条件，同样会压栈左子树节点，右子树，左子树，等左子树递归结束后，栈里右子树出栈。这和递归对栈使用方式是一样的。

## 堆排序
1. 计算子节点时，左右子节点分别为i*2+1和i*2+2，而不是i*2和i*2+1，这是因为算法导论是从index=1开始算起，而实际编程是从index=0开始算起。
2. wiki上建堆是倒数第二层最后一个父节点的index为len/2-1，这是因为最后一个节点的index为len-1，而一个节点的父节点为floor((i-1)/2)，所以最后一个节点为floor((len-1-1)/2)，也就是这里是用len先得到index，然后在算出父节点，化简之后就是len/2-1。

## 计数排序
1. 实际的计数排序索引是从0开始，想想一下如果有一个最小的数字为a[x]，c[a[x]]++，之后，如果直接用计数就会把最小的数据排在第1位，而不是第0位，所以负责计数的数据最后都需要减1，这也可以放在最后分配的步骤中先执行:
    
        c[arr[i]] -= 1

    然后在执行:

        sorted_arr[c[arr[i]]] = arr[i];

## 随机选择

1. 分割后的pivot_index和start+r比较，如果start+r大于pivot_index，则从pivot_index+1~end中寻找，这时候要从r中减去(pivot_index-start+1)，因为这时已经排除了pivot_index-start+1这么多的数据，总数组中排名为r（从0开始）的数据，在剩余的数据中，排名要减去pivot_index-start+1这么多。