from typing import *
from graphviz import Graph
from collections import OrderedDict

'''
[
    "12", 
    "123",
    "212",
    "312",
    "313",
    "323",
]
以下面的字典树为例
root
├── 1
│   └── 2
│       └── 3
├── 2
│   └── 1
│       └── 2
└── 3
    ├── 1
    │   ├── 2
    │   └── 3
    └── 2
        └── 3
讨论树时root为0层
ascii '1' to int 49
ascii '2' to int 50
ascii '3' to int 51

i表示base数组和check数组的偏移

char =     ×    1    2    3    2    ×    ×    1    2    ×    1    2    2    3    ×    ×    3    ×    3
i    =     0   51   52   53   54   55   56   57   59   60   61   62   63   64   65   66   67   68  107
base =     1    3    7   11   55   -1   -2    8   60   -3   12   15   65   66   -4   -5   68   -6   56
check=     0    1    1    1    3   55   56    7    8   60   11   11   12   12   65   66   15   68   55

使用unicode+1作为偏移，为了让空字符也能有一个数值0+1的偏移

查找"313"的步骤，根节点的状态位为base[0]=1
沿着'1'
base[0]+('1'+1) = 1+(49+1) = 51  # 51这里放的是树第一层节点1的状态值base[51] = 3
check[51] = 1表示父节点
沿着'2'
base[51]+('2'+1) = 3+(50+1) = 54
check[54] = 3表示父节点
沿着'3'
base[51]+('2'+1) = 3+(50+1) = 54
check[54] = 3表示父节点
'''

def build_graph():
    g = Graph(format='png')
    node_id = 0

    def build_edge_with_id(context, char, node):
        nonlocal node_id
        for key, child in node._children.items():
            label=key
            number = str(ord(key)+1)
            if key == '\0':
                label = 'null'
            if child._value is None:
                g.node(context+number, label=label, style='filled', fillcolor='white', fontcolor='black')
            else:
                g.node(context+number, label=label, style='filled', fillcolor='blue', fontcolor='black')
            g.edge(context, context+number, color='black')
    return g, build_edge_with_id

def render_tree(t):
    g, b = build_graph()
    g.node('root', label='root', style='filled', fillcolor='white', fontcolor='black')
    for key, child in t._children.items():
        label = key
        number = str(ord(key)+1)
        if key == '\0':
            label = 'null'
        if child._value is None:
            g.node('root'+number, label=label, style='filled', fillcolor='white', fontcolor='black')
        else:
            g.node('root'+number, label=label, style='filled', fillcolor='blue', fontcolor='black')
        g.edge('root', 'root'+number, color='black')
    t.traverse('root', b)
    return g

class Node(object):
    def __init__(self, value) -> None:
        self._children = OrderedDict()
        self._value = value

    def _add_child(self, char, value, overwrite=False):
        child = self._children.get(char)
        if child is None:
            child = Node(value)
            self._children[char] = child
        elif overwrite:
            child._value = value
        return child

    def children(self):
        return self._children

    # getter
    def get_value(self):
        return self._value

    # setter
    def set_value(self, value):
        self._value = value

    # creating a property object
    value = property(get_value, set_value) 

    @classmethod
    def __traverse(cls, x, context, func:Callable):
        if x != None:
            for key, value in x._children.items():
                number = str(ord(key)+1)
                func(context+number, key, value)
                cls.__traverse(value, context+number, func)

    def traverse(self, *args):
        Node.__traverse(self, *args)


class Trie(Node):
    def __init__(self) -> None:
        super().__init__(None)

    def __contains__(self, key):
        return self[key] is not None

    def __getitem__(self, key):
        state = self
        for char in key:
            state = state._children.get(char)
            if state is None:
                return None
        return state._value

    def __setitem__(self, key, value):
        state = self
        for i, char in enumerate(key):
            if i < len(key) - 1:
                state = state._add_child(char, None, False)
            else:
                state = state._add_child(char, value, True)

class DaTrie:
    def __init__(self):
        super().__init__()
        self.base = [0]*65535 # TODO:性能优化
        self.check = [0]*65535
        self.beginSet = set()
        self.allocSize = 65535
        self.size = 0
        self.nextCheckPos = 0
        self.nonzero_num = 0

    def resize(self, size):
        self.base.extend([0]*(self.size - size + 65535))
        self.check.extend([0]*(self.size - size + 65535))
        self.allocSize += (self.size - size + 65535)
    
    def code(self, key):
        return ord(key) if ord(key) == 0 else ord(key)+1

    def insert_children(self, depth, children):
        tab_width = 10
        begin = 0
        first = True

        keys = []
        for key, child in children.items():
            keys.append(key)
        pos = max(self.code(keys[0])+1, self.nextCheckPos)-1 # pos要比self.code(keys[0])大的目的是防止base中非叶子节点出现负数
        while True:
            pos += 1
            if pos >= self.allocSize:
                self.resize(pos+1)

            if self.check[pos] != 0:
                # print(f'{" "*depth*tab_width}|fail check [{pos}] at 0')
                self.nonzero_num += 1
                continue
            if first:
                first = False
                self.nextCheckPos = pos
            
            begin = pos - self.code(keys[0])
            if begin + self.code(keys[-1]) >= self.allocSize:
                self.resize(begin + self.code(keys[-1]))
            
            # 防止不同的节点在base中有相同的begin，例如'1'和'2'在base数组中都是51，
            # 那么'1xxx...','2xxx...'会冲突，无法区分'1'和'2'的子节点
            if begin in self.beginSet:
                continue
            # TODO:性能优化
            for i, key in enumerate(keys, 1):
                if self.check[begin+self.code(key)] != 0:
                    # print(f'{" "*depth*tab_width}|fail check [{begin+self.code(key)}] at {i}')
                    break
            else:
                break

        if 1.0 * self.nonzero_num/(pos-self.nextCheckPos+1) >= 0.95:
            self.nextCheckPos = pos

        self.beginSet.add(begin)

        if self.size < begin + self.code(keys[-1]) + 1:
            self.size = begin + self.code(keys[-1]) + 1

        for i in range(len(keys)):
            self.check[begin + self.code(keys[i])] = begin

        for key, child in children.items():
            if len(child.children()) == 0:
                if child.value < 0: # 小于0是次if对应的else插入的节点 
                    self.base[begin + self.code(key)] = child.value
                    # print(f'{" "*depth*tab_width}|{key:2s} -> @{begin+self.code(key)} h={child.value}')
                else:
                    #修改trie
                    child._add_child('\0', -child.value-1)
                    h = self.insert_children(depth+1, child.children())
                    self.base[begin+self.code(key)] = h
                    # print(f'{" "*depth*tab_width}|{key:2s} -> @{begin+self.code(key)} h={h}')
            else:
                if child.value is not None:
                    #修改trie
                    child._add_child('\0', -child.value-1)
                    child.children().move_to_end('\0', last=False)

                h = self.insert_children(depth+1, child.children())
                self.base[begin+self.code(key)] = h
                # print(f'{" "*depth*tab_width}|{key:2s} -> @{begin+self.code(key)} h={h}')
        return begin

    def build(self, root:Trie):
        self.base[0] = 1
        self.check[0] = 0
        children = root.children()
        self.insert_children(0, children)


if __name__ == '__main__':
    keys = [
        "12", 
        "123",
        "212",
        "312",
        "313",
        "323",
    ]
    keys.sort()
    print(keys)
    trie = Trie()
    for index, key in enumerate(keys):
        trie[key] = index
    
    # def build(node):
    #     children = node.children()
    #     for key, child in children.items():
    #         build(child)
    #         print(key)
    # build(trie)
    datrie = DaTrie()
    datrie.build(trie)

    base = datrie.base
    check = datrie.check
    infoIndex    = "i    = "
    infoChar     = "char = "
    infoBase     = "base = "
    infoCheck    = "check= "
    for i in range(datrie.size):
        if base[i] != 0 or check[i] != 0:
            infoChar  += "    " +   ( "×" if i == check[i] else chr(i - check[i] - 1))
            infoIndex += " " + f'{i:4d}'
            infoBase  += " " + f'{base[i]:4d}'
            infoCheck += " " + f'{check[i]:4d}'
    print("\n" + infoChar +
            "\n" + infoIndex +
            "\n" + infoBase +
            "\n" + infoCheck + "\n")
    print(base[0:datrie.size])
    g = render_tree(trie)
    g.render(filename='g', view=True)