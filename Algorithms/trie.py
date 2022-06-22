import string
from typing import *
from graphviz import Graph
from collections import OrderedDict

def build_graph():
    g = Graph(format='png')
    node_id = 0

    def build_edge_with_id(context, node):
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

    @classmethod
    def __traverse(cls, x, context, func:Callable):
        if x != None:
            print(context)
            for key, value in x._children.items():
                func(context+key, value)
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


if __name__ == '__main__':
    trie = Trie()
    trie['自然'] = 'nature'
    trie['自然人'] = 'human'
    trie['自然语言'] = 'language'
    trie['自语'] = 'talk  to oneself'
    trie['入门'] = 'introduction'
    g = render_tree(trie)
    g.render(filename='g', view=True)
