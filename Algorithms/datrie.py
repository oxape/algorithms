from typing import *
from graphviz import Graph
from collections import OrderedDict

def build_graph():
    g = Graph(format='png')
    node_id = 0

    def build_edge_with_id(context, char, node):
        nonlocal node_id
        for key, child in node._children.items():
            if child._value is None:
                g.node(context+key, label=key, style='filled', fillcolor='white', fontcolor='black')
            else:
                g.node(context+key, label=key, style='filled', fillcolor='blue', fontcolor='black')
            g.edge(context, context+key, color='black')
    return g, build_edge_with_id

def render_tree(t):
    g, b = build_graph()
    g.node('root', label='root', style='filled', fillcolor='white', fontcolor='black')
    for key, child in t._children.items():
        if child._value is None:
            g.node('root'+key, label=key, style='filled', fillcolor='white', fontcolor='black')
        else:
            g.node('root'+key, label=key, style='filled', fillcolor='blue', fontcolor='black')
        g.edge('root', 'root'+key, color='black')
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
                func(context+key, key, value)
                cls.__traverse(value, context+key, func)

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
        self.allocSize = 65535
        self.size = 0
        self.nextCheckPos = 0
        self.nonzero_num = 0

    def resize(self, size):
        self.base.extend([0]*(self.size - size + 65535))
        self.check.extend([0]*(self.size - size + 65535))
        self.allocSize += (self.size - size + 65535)
    
    def code(key):
        return ord(key)+1

    def insert_node(self, depth, node):
        children = node.children()
        tab_width = 10
        begin = 0
        first = True

        keys = []
        for key, child in children.items():
            keys.append(key)
        pos = max(self.nextCheckPos, self.code(keys[0])+1)-1
        while True:
            pos += 1
            if pos >= self.allocSize:
                self.resize(pos+1)

            if self.check[pos] != 0:
                print(f'{" "*depth*tab_width}|fail')
                self.nonzero_num += 1
                continue
            if first:
                first = False
                self.nextCheckPos = pos
            
            begin = pos - self.code(keys[0])
            if begin + self.code(keys[-1]) >= self.allocSize:
                self.resize(begin + self.code(keys[-1]))
            
             # TODO:性能优化
            for _, key in enumerate(keys, 1):
                if self.check[begin+self.code(key)] != 0:
                    break
            else:
                break

        if 1.0 * self.nonzero_num/(pos-self.nextCheckPos+1) >= 0.95:
            self.nextCheckPos = pos

        if self.size < begin + self.code(keys[-1]) + 1:
            self.size = begin + self.code(keys[-1]) + 1

        for i in range(len(keys)):
            self.check[begin + self.code(keys[i])] = begin

        for (int i = 0; i < siblings.size(); i++)
        {
            List<Node> new_siblings = new ArrayList<Node>();

            if (fetch(siblings.get(i), new_siblings) == 0)  // 一个词的终止且不为其他词的前缀
            {
                base[begin + siblings.get(i).code] = (value != null) ? (-value[siblings
                        .get(i).left] - 1) : (-siblings.get(i).left - 1);
//                System.out.println(this);

                if (value != null && (-value[siblings.get(i).left] - 1) >= 0)
                {
                    error_ = -2;
                    return 0;
                }

                progress++;
                // if (progress_func_) (*progress_func_) (progress,
                // keySize);
            }
            else
            {
                Node node = siblings.get(i);
                int h = insert(node.depth+1, new_siblings, used);   // dfs
                tab = new String(new char[(depth-1)*tab_width]).replace("\0", " ");
                if (node.code > 0) {
                    System.out.println(String.format("%s|%-2s[%2d-%2d] -> @%d h=%d", tab, (char)(node.code - 1), node.left, node.right, begin + siblings.get(i).code, h));
                }
                base[begin + siblings.get(i).code] = h;
//                System.out.println(this);
            }
        }
        return begin;

    def build_array(self, node):
        self.base[0] = 1
        self.check[0] = 0
        # self.insert_node(0, node)

        # children = node.children()
        # for key, child in children.items():
        #     self.build_array(child)
        #     print(key)

    def build(self, root:Trie):
        self.build_array(root)


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
    g = render_tree(trie)
    g.render(filename='g', view=True)