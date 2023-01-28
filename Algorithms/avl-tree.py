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
        self.balance()

    def delete(self):
        pass

    def successor(self):
        if self.rightChild is None:
            return None
        return self.rightChild.successor()

    def draw(self, g):
        g.node(str(id(self)), label=str(self.value))
        if self.leftChild is not None:
            self.leftChild.draw(g)
            g.edge(str(id(self)), str(id(self.leftChild)), color='red')
        if self.rightChild is not None:
            self.rightChild.draw(g)
            g.edge(str(id(self)), str(id(self.rightChild)), color='blue')
        

    def traversalInOrder(self):
        if self.leftChild is not None:
            self.leftChild.traversalInOrder()
        print(f'{self.value} ')
        if self.rightChild is not None:
            self.rightChild.traversalInOrder()

    def balance(self):
        if abs(self.balanceFactor) < 2:
            return
        if self.balanceFactor == 2:
            # self.leftChild.leftHeght >= 
            if self.leftChild.balanceFactor >= 0:
                self.rightRotate()
            else:
                self.leftChild.leftRotate()
                self.rightRotate()
        else:
            if self.rightChild.balanceFactor <= 0:
                self.leftRotate()
            else:
                self.rightChild.rightRotate()
                self.leftRotate()

    def leftRotate(self):
        # self.rightChild代替self作为self.parent的child
        if self.parent:
            if self.parent.leftChild == self:
                self.parent.leftChild = self
            else:
                self.parent.rightChild = self
        
        if self.rightChild is not None:
            rightChild = self.rightChild
            self.rightChild = self.rightChild.leftChild
            rightChild.leftChild = self
            rightChild.parent = self.parent
            self.parent = rightChild
        return self.parent

    def rightRotate(self):
        # self.leftChild代替self作为self.parent的child
        if self.parent:
            if self.parent.leftChild == self:
                self.parent.leftChild = self
            else:
                self.parent.rightChild = self
        if self.leftChild is not None:
            leftChild = self.leftChild
            self.leftChild = self.leftChild.rightChild
            leftChild.rightChild = self
            leftChild.parent = self.parent
            self.parent = leftChild
        return self.parent
        
class AVLTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if self.root is None:
            self.root = AVLNode(value)
        else:
            self.root.insert(value)
        return self.root

    def traversalInOrder(self):
        if self.root is not None:
            self.root.traversalInOrder()

    def draw(self, g):
        if self.root is not None:
            self.root.draw(g)
            g.render(filename='g.gv', view=True)

if __name__ == '__main__':
    avlTree = AVLTree()
    avlTree.insert(1)
    avlTree.insert(102)
    avlTree.insert(20)
    # avlTree.insert(100)
    # avlTree.insert(80)
    # avlTree.insert(200)
    avlTree.traversalInOrder()

    g = build_render()
    avlTree.draw(g)