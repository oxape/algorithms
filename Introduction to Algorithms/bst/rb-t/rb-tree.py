from graphviz import Graph
from enum import Enum

class Color(Enum):
    Red = 0
    Black = 1


class RBNode:
    def __init__(self, key=0, color=Color.Red):
        self.p = None
        self.children = []     # 0: left child 1 right child
        self.color = color
        self.key = key


class RBTree:
    nil = RBNode(color=Color.Black)

    def __init__(self, root=nil):
        self.root = root

    def __left_rotate(self, x : RBNode):
        left = 0
        right = 1
        y = x.children[left]
        x.children[right] = y.children[left]
        if y.children[left] != RBTree.nil:
            y.children[left].p = x
        y.p = x.p
        if x.p == RBTree.nil:
            self.root = y
        elif x == x.p.children[left]:
            x.p.children[left] = y
        else:
            x.p.children[right] = y
        y.children[left] = x
        x.p = y

    def __right_rotate(self, node : RBNode):
        pass

    def __insert(self, node : RBNode):
        left = 0
        right = 1
        y = RBTree.nil
        x = self.root
        while x != RBTree.nil:
            y = x
            if node.key < x.key:
                x = x.children[left]
            else:
                x = x.children[right]
        node.p = y
        if y == RBTree.nil:
            self.root = node
        elif node.key < y.key:
            y.children[left] = node
        else:
            y.children[right] = node
        node.children[0] = RBTree.nil
        node.children[1] = RBTree.nil
        self.__fixup_red_red(node)

    def __fixup_red_red(self, node : RBNode):
        left = 0
        right = 1
        while node.p.color == Color.Red:
            if node.p == node.p.p.children[left]:
                y = node.p.p.children[right]
                if y.color == Color.Red:


            else:
                pass
        self.root.color = Color.Black

    def insert(self, key : int):
        n = RBNode(key, Color.Red)
        self.__insert(n)

    def delete(self, node):
        pass

    def find(self, key):
        pass

    def print(self):
        pass


if __name__ == '__main__':
    T = RBTree()
    l = [1, 48, 32, 12, 28, 13, 55, 22, 26, 35]

    g = Graph()
    g.node("1", label='2', style='filled', fillcolor='black', fontcolor='white')
    g.node("2", label='3', style='filled', fillcolor='red', fontcolor='white')
    g.node("3", label='nil', style='filled', fillcolor='black', fontcolor='white')
    g.node("4", label='nil', style='filled', fillcolor='black', fontcolor='white')
    g.node("5", label='nil', style='filled', fillcolor='black', fontcolor='white')
    g.edge("1", "2", color='black')
    g.edge("1", "3", color='black')
    g.edge("2", "4", color='black')
    g.edge("2", "5", color='black')
