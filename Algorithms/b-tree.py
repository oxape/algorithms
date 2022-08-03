from graphviz import Graph

def swap(arr, a, b):
    tmp = arr[b]
    arr[b] = arr[a]
    arr[a] = tmp

def partition(arr, start, end):
    pivot = arr[start]
    k=start
    for j in range(start+1, end+1):
        if arr[j] < pivot:
            k += 1
            swap(arr, k, j)
    swap(arr, start, k)
    return k

def quick_sort_recursive(arr, start, end):
    if start >= end:
        return
    pivot_index = partition(arr, start, end)
    quick_sort_recursive(arr, start, pivot_index-1)
    quick_sort_recursive(arr, pivot_index+1, end)


# class Node(object):
#     def __init__(self, value) -> None:
#         self._children = OrderedDict()
#         self._value = value
if __name__ == '__main__':
    arr = [10, 12, 3, 1, 15, 5, 4, 20, 21, 18, 9, 10, 33, 17]
    num = len(arr)
    quick_sort_recursive(arr, 0, num-1)
    print(arr)