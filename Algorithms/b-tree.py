from turtle import right
from typing import *
from graphviz import Digraph, nohtml
from operator import itemgetter

'''
g = Digraph('g', filename='btree.gv',
            node_attr={'shape': 'record', 'height': '.1'})
g.node('node0', nohtml('<f0> |<f1> G|<f2>'))
g.node('node1', nohtml('<f0> |<f1> E|<f2>'))
g.node('node2', nohtml('<f0> |<f1> B|<f2>'))
g.node('node3', nohtml('<f0> |<f1> F|<f2>'))
g.node('node4', nohtml('<f0> |<f1> R|<f2>'))
g.node('node5', nohtml('<f0> |<f1> H|<f2>'))
g.node('node6', nohtml('<f0> |<f1> Y|<f2>'))
g.node('node7', nohtml('<f0> |<f1> A|<f2>'))
g.node('node8', nohtml('<f0> |<f1> C|<f2>'))
g.edge('node0:f2', 'node4:f1')
g.edge('node0:f0', 'node1:f1')
g.edge('node1:f0', 'node2:f1')
g.edge('node1:f2', 'node3:f1')
g.edge('node2:f2', 'node8:f1')
g.edge('node2:f0', 'node7:f1')
g.edge('node4:f2', 'node6:f1')
g.edge('node4:f0', 'node5:f1')
g.view()
'''

def binary_search_to_insert(arr, key, getter=None):
    min = 0
    max = len(arr)
    if getter is None:
        while min != max:
            middle = (min+max)//2
            if arr[middle] == key:
                return middle
            if key < arr[middle]:
                max = middle
            else:
                min = middle+1
    else:
        while min < max:
            middle = (min+max)//2
            if getter(key) == getter(arr[middle]):
                return middle
            if getter(key) < getter(arr[middle]):
                max = middle
            else:
                min = middle+1
    return min

class Item:
    def __init__(self, key, value):
        self._key = key
        self._value = value
    
    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def __getitem__(self, key):
        if key == 'key':
            return self.key
        else:
            return self.value

    def __repr__(self):
        return f'<Item {{{self.key}:{self.value}}}>'
    
    def __str__(self):
        return f'{{{self.key}:{self.value}}}'

class Node:
    def __init__(self, isLeaf):
        self.isLeaf = isLeaf
        self.items = []
        self.pointers = [None]
        self.parent = None
        self.posInParent = 0

    @property
    def size(self):
        return len(self.items)

    def insert(self, item):
        pos = binary_search_to_insert(self.items, item, itemgetter('key'))
        if pos < self.size:
            prevSize = self.size
            self.items.append(None)
            self.pointers.append(None)
            for i in reversed(range(pos, prevSize)):
                self.items[i+1] = self.items[i]
                self.pointers[i+1] = self.items[i]
            self.items[pos] = item
        else:
            self.items.append(item)
            self.pointers.append(None)

class BTree:
    def __init__(self, rank):
        self.rank = rank
        self.root = Node(True)

    def insert(self, item: Item):
        node = self._find_node_to_insert(self.root, item)
        node.insert(item)
        if node.size <= self.rank-1:
            return
        middle = node.size//2
        leftChild = Node(True)
        leftChild.items = node.items[:middle]
        rightChild = Node(True)
        rightChild.items = node.items[middle+1:]
        while True:
            pos = node.posInParent
            parent = node.parent
            if parent is None:
                parent = Node(False)
            prevSize = parent.size
            parent.items.append(None)
            parent.pointers.append(None)
            for i in reversed(range(pos, prevSize)):
                parent.items[i+1] = self.items[i]
                parent.pointers[i+1] = self.pointers[i]
            parent.items[pos] = item
            parent.pointers[pos] = leftChild
            parent.pointers[pos+1] = rightChild
            if 
            if parent.size < self.rank-1:
                break
            else:
                break

    def _find_node_to_insert(self, node: Node, item: Item):
        if node.isLeaf:
            return node
        items_len =  node.size
        for i in range(items_len):
            if item.key < node.items[i].key:
                return node.pointers[i]
        return self._find_node_to_insert(node, item)

    def _insert(self, parent):
        pass


if __name__ == '__main__':
    arr = [Item(13, 0), Item(5, 1), Item(2, 1), Item(7, 1), Item(6, 1)]

    btree = BTree(5)
    for item in arr:
        btree.insert(item)
