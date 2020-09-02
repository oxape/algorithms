

def find_lowest_cost_node(costs: dict, processed: list) -> str:
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        # 如果当前节点的开销更低且未处理过
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node


def find_lowest_path(graph: dict, start: str, end):
    parents = dict()
    costs = dict()
    infinity = float('inf')
    for k, v in graph[start].items():
        costs[k] = v
        parents[k] = start
    parents[end] = None
    costs['fin'] = infinity
    processed = []
    while True:
        # 在未处理的节点中找出开销最小的节点
        node = find_lowest_cost_node(costs, processed)
        # 这个while循环在所有节点都被处理过后结束
        if node is None:
            break
        cost = costs[node]
        neighbors = graph[node]
        # 遍历邻居节点
        for n in neighbors.keys():
            new_cost = cost + neighbors[n]
            # 如果经过当前节点前往邻居比之前的costs记录更近
            if n not in costs or costs[n] > new_cost:
                costs[n] = new_cost
                parents[n] = node
        processed.append(node)
    print(costs)
    parent = end
    path = [end]
    while parent != start:
        parent = parents[parent]
        path.append(parent)
    path.reverse()
    print(path)


def test1():
    graph = dict()
    graph['start'] = {'a': 6, 'b': 2}
    graph['a'] = {'fin': 1}
    graph['b'] = {'a': 3, 'fin': 5}
    graph['fin'] = {}
    find_lowest_path(graph, 'start', 'find')


def test1():
    graph = dict()
    graph['start'] = {'a': 6, 'b': 2}
    graph['a'] = {'fin': 1}
    graph['b'] = {'a': 3, 'fin': 5}
    graph['fin'] = {}
    print('------ test1 ------')
    find_lowest_path(graph, 'start', 'fin')


def test_a():
    graph = dict()
    graph['start'] = {'A': 5, 'C': 2}
    graph['A'] = {'B': 4, 'D': 2}
    graph['B'] = {'D': 6, 'fin': 3}
    graph['C'] = {'A': 8, 'D': 7}
    graph['D'] = {'fin': 1}
    graph['fin'] = {}
    print('------ test_a ------')
    find_lowest_path(graph, 'start', 'fin')


def test_b():
    # 带环的图
    graph = dict()
    graph['start'] = {'A': 10}
    graph['A'] = {'B': 20}
    graph['B'] = {'fin': 30, 'C': 1}
    graph['C'] = {'A': 1}
    graph['fin'] = {}
    print('------ test_b ------')
    find_lowest_path(graph, 'start', 'fin')


if __name__ == '__main__':
    test1()
    test_a()
    test_b()
