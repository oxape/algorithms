import graphviz
from graphviz import Digraph

def build_render():
    g = Digraph(format='png', node_attr={'shape': 'record', 'height': '.1'})
    return g

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.leftChild = None
        self.rightChild = None
        self.parent = None

    def height(self):
        return max(self.leftHeight(), self.rightHeight())

    def leftHeight(self):
        if self.leftChild is None:
            return 1
        else:
            return self.leftChild.height()+1

    def rightHeight(self):
        if self.rightChild is None:
            return 1
        else:
            return self.rightChild.height()+1

    @property
    def balanceFactor(self):
        return self.leftHeight()-self.rightHeight()

    def insert(self, value):
        if value < self.value:
            if self.leftChild is None:
                self.leftChild = AVLNode(value)
                self.leftChild.parent = self
            else:
                self.leftChild.insert(value)
        else:
            if self.rightChild is None:
                self.rightChild = AVLNode(value)
                self.rightChild.parent = self
            else:
                self.rightChild.insert(value)
        return self.balance()

    def delete(self, value):
        if value == self.value:
            # 左子树为空
            if self.leftChild is None:
                # self被释放
                # 因为删除前树是平衡的，所以右孩子肯定没有孩子节点
                return self.rightChild
            if self.rightChild is None:
                # self被释放
                # 因为删除前树是平衡的，所以左孩子肯定没有孩子节点
                return self.leftChild
            # 左右子树都不为空
            successor = self.successor()
            parent = self.parent
            if parent is not None:
                if parent.leftChild == self:
                    parent.leftChild = successor
                else:
                    parent.rightChild = successor
            successor.rightChild = self.rightChild.delete(successor.value)
            successor.leftChild = self.leftChild
            return successor
        if value < self.value:
            if self.leftChild is not None:
                self.leftChild = self.leftChild.delete(value)
        else:
            if self.rightChild is not None:
                self.rightChild = self.rightChild.delete(value)
        return self.balance()
    
    def mini(self):
        if self.leftChild is None:
            return self
        return self.leftChild.mini()
    
    def successor(self):
        if self.rightChild is None:
            return None
        return self.rightChild.mini()

    def draw(self, g):
        g.node(str(id(self)), label=f'{str(self.value)}')
        if self.leftChild is not None:
            self.leftChild.draw(g)
            g.edge(str(id(self)), str(id(self.leftChild)), color='red')
        else:
            g.node(str(id(self)+1), label='null')
            g.edge(str(id(self)), str(id(self)+1), color='red')
        if self.rightChild is not None:
            self.rightChild.draw(g)
            g.edge(str(id(self)), str(id(self.rightChild)), color='blue')
        else:
            g.node(str(id(self)+2), label='null')
            g.edge(str(id(self)), str(id(self)+2), color='blue')

    def traversalInOrder(self):
        if self.leftChild is not None:
            self.leftChild.traversalInOrder()
        print(f'{self.value} ')
        if self.rightChild is not None:
            self.rightChild.traversalInOrder()

    def balance(self):
        if abs(self.balanceFactor) < 2:
            return self
        if self.balanceFactor == 2:
            # self.leftChild.leftHeght >= 
            if self.leftChild.balanceFactor >= 0:
                return self.rightRotate()
            else:
                self.leftChild.leftRotate()
                return self.rightRotate()
        else:
            if self.rightChild.balanceFactor <= 0:
                return self.leftRotate()
            else:
                self.rightChild.rightRotate()
                return self.leftRotate()

    def leftRotate(self):
        # self.rightChild代替self作为self.parent的child
        if self.rightChild is not None:
            # 暂存父节点
            parent = self.parent
            # 暂存右孩子
            rightChild = self.rightChild
            # 让self的右孩子指向右孩子的左孩子
            self.rightChild = rightChild.leftChild
            if self.rightChild is not None:
                self.rightChild.parent = self
            # 右孩子的左孩子指向self
            rightChild.leftChild = self
            self.parent = rightChild

            if parent is not None:
                if parent.leftChild == self:
                    parent.leftChild = rightChild
                else:
                    parent.rightChild = rightChild
            rightChild.parent = parent

        return rightChild

    def rightRotate(self):
        # self.leftChild代替self作为self.parent的child
        if self.leftChild is not None:
            # 暂存父节点
            parent = self.parent
            # 暂存左孩子
            leftChild = self.leftChild
            # 让self的左孩子指向左孩子的右孩子
            self.leftChild = leftChild.rightChild
            if self.leftChild is not None:
                self.leftChild.parent = self
            # 左孩子的右孩子指向self
            leftChild.rightChild = self
            self.parent = leftChild

            if parent is not None:
                if parent.leftChild == self:
                    parent.leftChild = leftChild
                else:
                    parent.rightChild = leftChild
            leftChild.parent = parent

        return leftChild
        
class AVLTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if self.root is None:
            self.root = AVLNode(value)
        else:
            self.root = self.root.insert(value)
        return self.root
    
    def delete(self, value):
        if self.root is None:
            return
        self.root = self.root.delete(value)

    def traversalInOrder(self):
        if self.root is not None:
            self.root.traversalInOrder()

    def draw(self, g):
        if self.root is not None:
            self.root.draw(g)
            g.render(filename='g.gv', view=True)

import unittest

class Test(unittest.TestCase):
    def testInsert(self):
        avlTree = AVLTree()
        avlTree.insert(20)
        avlTree.insert(4)
        avlTree.insert(15)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)

        avlTree = AVLTree()
        avlTree.insert(20)
        avlTree.insert(4)
        avlTree.insert(3)
        avlTree.insert(9)
        avlTree.insert(26)
        avlTree.insert(15)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)

        avlTree = AVLTree()
        avlTree.insert(20)
        avlTree.insert(4)
        avlTree.insert(3)
        avlTree.insert(9)
        avlTree.insert(2)
        avlTree.insert(7)
        avlTree.insert(11)
        avlTree.insert(26)
        avlTree.insert(21)
        avlTree.insert(30)
        avlTree.insert(15)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)

        avlTree = AVLTree()
        avlTree.insert(20)
        avlTree.insert(4)
        avlTree.insert(8)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)

        avlTree = AVLTree()
        avlTree.insert(20)
        avlTree.insert(4)
        avlTree.insert(3)
        avlTree.insert(9)
        avlTree.insert(26)
        avlTree.insert(8)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)

        avlTree = AVLTree()
        avlTree.insert(20)
        avlTree.insert(4)
        avlTree.insert(3)
        avlTree.insert(9)
        avlTree.insert(2)
        avlTree.insert(7)
        avlTree.insert(11)
        avlTree.insert(26)
        avlTree.insert(21)
        avlTree.insert(30)
        avlTree.insert(8)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)

    def testDelete(self):
        # case 1
        avlTree = AVLTree()
        avlTree.insert(2)
        avlTree.insert(1)
        avlTree.insert(4)
        avlTree.insert(5)
        avlTree.insert(3)

        avlTree.delete(1)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)

        # case 2
        avlTree = AVLTree()
        avlTree.insert(6)
        avlTree.insert(2)
        avlTree.insert(9)
        avlTree.insert(1)
        avlTree.insert(4)
        avlTree.insert(8)
        avlTree.insert(0xB)
        avlTree.insert(3)
        avlTree.insert(5)
        avlTree.insert(7)
        avlTree.insert(0xA)
        avlTree.insert(0xC)
        avlTree.insert(0xD)

        avlTree.delete(1)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)


        # case 3
        avlTree = AVLTree()
        avlTree.insert(5)
        avlTree.insert(2)
        avlTree.insert(8)
        avlTree.insert(1)
        avlTree.insert(3)
        avlTree.insert(7)
        avlTree.insert(0xA)
        
        avlTree.insert(4)
        avlTree.insert(8)
        avlTree.insert(7)
        avlTree.insert(0xA)
        avlTree.insert(6)
        avlTree.insert(9)
        avlTree.insert(0xB)
        avlTree.insert(0xC)

        avlTree.delete(1)
        self.assertLess(abs(avlTree.root.balanceFactor), 2)
 
if __name__=='__main__':
    unittest.main()

    # # case 2
    # avlTree = AVLTree()
    # avlTree.insert(6)
    # avlTree.insert(2)
    # avlTree.insert(9)
    # avlTree.insert(1)
    # avlTree.insert(4)
    # avlTree.insert(8)
    # avlTree.insert(0xB)
    # avlTree.insert(3)
    # avlTree.insert(5)
    # avlTree.insert(7)
    # avlTree.insert(0xA)
    # avlTree.insert(0xC)
    # avlTree.insert(0xD)

    # avlTree.delete(1)

    # g = build_render()
    # avlTree.draw(g)
