from typing import *
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

class Index:
    def __init__(self, key, value):
        self._key = key
        self._value = value
    
    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

class Node:
    def __init__(self, max):
        self.max = max
        self.size = 0
        self.indexs = []
        self.pointers = []

class BTree:
    def __init__(self, rank):
        self.rank = rank
        self.root = Node(rank)

    def insert(self, node: Node):
        

    def __insert(self, parent):
    

if __name__ == '__main__':
    arr = [10, 12, 3, 1, 15, 5, 4, 20, 21, 18, 9, 10, 33, 17]
    num = len(arr)
    quick_sort_recursive(arr, 0, num-1)
    print(arr)