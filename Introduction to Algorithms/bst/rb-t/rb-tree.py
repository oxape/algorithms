from enum import Enum


class Color(Enum):
    Red = 0
    Black = 1


class RBNode:
    def __init__(self, key=0, color=Color.Red):
        self.p = None
        self.child = {}     # 0: left child 1 right child
        self.color = color
        self.key = key


class RBTree:
    nil = RBNode(color=Color.Black)

    def __init__(self, root=nil):
        self.root = root

    def __insert(self, node):
        pass

    def insert(self, key):
        pass

    def delete(self, node):
        pass

    def find(self, key):
        pass

    def print(self):
        pass


if __name__ == '__main__':
    T = RBTree()
