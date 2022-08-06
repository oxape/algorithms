from typing import *
from graphviz import Digraph, nohtml
from operator import itemgetter

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
    index = 0
    def __init__(self, key, value):
        self._key = key
        self._value = value
        Item.index += 1
        self.index = Item.index
    
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
    index = 0
    def __init__(self, isLeaf):
        self.isLeaf = isLeaf
        self.items = []
        self.pointers = [None]
        self.parent = None
        self.posInParent = 0
        Node.index += 1
        self.index = Node.index+1

    @property
    def size(self):
        return len(self.items)

    def setPointers(self, index, child):
        if len(self.pointers) <= index:
            self.pointers.append(child)
        else:
            self.pointers[index] = child

    def insertToLeaf(self, item):
        pos = binary_search_to_insert(self.items, item, itemgetter('key'))
        if pos < self.size:
            prevSize = self.size
            self.items.append(None)
            self.pointers.append(None)
            for i in reversed(range(pos, prevSize)):
                self.items[i+1] = self.items[i]
                self.pointers[i+1] = None
            self.items[pos] = item
        else:
            self.items.append(item)
            self.pointers.append(None)

    def bubbleToParent(self, pos, middleItem, leftChild, rightChild):
        if middleItem.key == 15:
            pass
        pos = self.posInParent
        parent = self.parent
        if parent is None:
            parent = Node(False)
        leftChild.parent = parent
        leftChild.posInParent = pos
        rightChild.parent = parent
        rightChild.posInParent = pos+1

        print(f'{id(leftChild.parent)}')
        print(f'{id(rightChild.parent)}')

        prevSize = parent.size
        parent.items.append(None)
        parent.pointers.append(None)
        # 先移动尾部，最右孩子指针
        parent.pointers[prevSize+1] = parent.pointers[prevSize]
        if parent.pointers[prevSize+1] is not None:
            parent.pointers[prevSize+1].posInParent = prevSize+1
        for i in reversed(range(pos, prevSize)):
            parent.items[i+1] = parent.items[i]
            parent.pointers[i+1] = parent.pointers[i]
            parent.pointers[i+1].posInParent = i+1
        parent.items[pos] = middleItem
        parent.pointers[pos] = leftChild
        parent.pointers[pos+1] = rightChild
        print(f'{id(parent)}')
        return parent

    def split(self):
        middle = self.size//2
        leftChild = Node(self.isLeaf)
        leftChild.items = self.items[:middle]
        for i in range(middle+1):
            node = self.pointers[i]
            pos = i
            leftChild.setPointers(pos, node)
            if node is not None:
                node.parent = leftChild
                node.posInParent = i
        rightChild = Node(self.isLeaf)
        rightChild.items = self.items[middle+1:]
        for i in range(middle+1, self.size+1):
            node = self.pointers[i]
            pos = i-(middle+1)
            rightChild.setPointers(pos, node)
            if node is not None:
                node.parent = rightChild
                node.posInParent = i-(middle+1)
        return leftChild, self.items[middle], rightChild

class BTree:
    def __init__(self, rank):
        self.rank = rank
        self.root = Node(True)

    def traverse(self, g=None):
        print(f'###### traverse ######')
        self._traverse(self.root, g)
        pass

    def insert(self, item: Item):
        node = self._find_node_to_insert(self.root, item)
        node.insertToLeaf(item)
        if node.size <= self.rank-1:
            return
        print(item.key)
        while True:
            leftChild, middleItem, rightChild = node.split()
            print('########')
            parent = node.bubbleToParent(node.posInParent, middleItem, leftChild, rightChild)
            print(f'{id(parent)}')
            if parent.parent is None:
                self.root = parent
            node = parent
            print(f'{id(node)}')
            if node.size <= self.rank-1:
                break

    def _find_node_to_insert(self, node: Node, item: Item):
        if node.isLeaf:
            return node
        items_len =  node.size
        for i in range(items_len):
            if item.key < node.items[i].key:
                return self._find_node_to_insert(node.pointers[i], item)
        return self._find_node_to_insert(node.pointers[items_len], item)

    def _traverse(self, node, g, depth = 0):
        print(f'{" "*depth*4} _traverse')
        print(f'{" "*depth*4} pos = {node.posInParent}')
        if g is not None:
            nohtml_list = []
            for i in range(node.size):
                if node.pointers[i] is not None:
                    nohtml_list.append(f'<f{str(id(node.pointers[i]))}>')
                nohtml_list.append(f'{node.items[i].key}:{node.items[i].index}')
            if node.size > 0:
                if node.pointers[node.size] is not None:
                    nohtml_list.append(f'<f{str(id(node.pointers[node.size]))}>')
            print(f'{" "*depth*4} {str(id(node))}:{"|".join(nohtml_list)}')
            g.node(str(id(node)), nohtml('|'.join(nohtml_list)))
            if node.parent is not None:
                print(f'{" "*depth*4} {str(id(node.parent))}:f{str(id(node))} -> {str(id(node))}')
                g.edge(f'{str(id(node.parent))}:f{str(id(node))}', f'{str(id(node))}')

        for i in range(node.size):
            if node.pointers[i] is not None:
                self._traverse(node.pointers[i], g, depth+1)
            print(f'{" "*depth*4} {node.items[i]}')
        
        if node.size > 0:
            if node.pointers[node.size] is not None:
                self._traverse(node.pointers[node.size], g, depth+1)


def btree_easy_insert(btree, key):
    # print(f'insert {key}')
    btree.insert(Item(key, key))

def build_render():
    g = Digraph(format='png', node_attr={'shape': 'record', 'height': '.1'})
    return g

if __name__ == '__main__':
    arr = [1, 23, 12, 8, 9, 7]
    arr = map(lambda x: Item(x, x), arr)

    btree = BTree(5)
    for item in arr:
        btree.insert(item)
    # btree.traverse()
    btree_easy_insert(btree, 19)
    btree_easy_insert(btree, 28)
    # btree.traverse()
    btree_easy_insert(btree, 26)
    btree_easy_insert(btree, 18)
    btree_easy_insert(btree, 20)
    btree_easy_insert(btree, 10)
    btree_easy_insert(btree, 5)
    btree_easy_insert(btree, 2)
    btree_easy_insert(btree, 15)
    btree_easy_insert(btree, 16)
    btree_easy_insert(btree, 17)
    btree_easy_insert(btree, 15)
    btree_easy_insert(btree, 16)
    btree_easy_insert(btree, 16)
    btree_easy_insert(btree, 15)
    # btree_easy_insert(btree, 29)

    g = build_render()
    btree.traverse(g)
    g.render(filename='tmp/g', view=True)