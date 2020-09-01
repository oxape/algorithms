"""
学习迪克斯拉特算法
"""


def bfs_weight_search(graph: dict):
    """ 打印出起点到所有节点的最短加权路径值

    Args:
        graph: 权重图字典
        graph = dict()
        graph['start'] = {'a': 6, 'b': 2}
        graph['a'] = {'stop': 1}
        graph['b'] = {'a': 3, 'stop': 5}
        graph['stop'] = {}
    """
    weights = dict()
    searched = set()
    # 加入起点到所有邻居节点的权重到权重字典
    for k, v in graph['start'].items():
        weights[k] = v
    # 所有节点都更新过它的邻居节点权重停止
    while len(searched) != len(weights):
        print(weights)
        min_weight = float('inf')
        min_node = None
        # 遍历所有权重节点找到距离起点最短的节点（不一定是直接距离，有可能是间接距离，当然也不是边数）
        for k, v in weights.items():
            if v <= min_weight:
                # 如果已经搜索过相应节点的邻居节点就忽略
                if k in searched:
                    print(f'{k} already check')
                    continue
                else:
                    min_weight = v
                    min_node = k
        if min_node is None:
            break
        searched.add(min_node)
        # 遍历min_node的邻居节点更新，权重字典weights
        for k, v in graph[min_node].items():
            if k in weights:
                # 如果经过这个节点到起点的距离比已经
                if v + min_weight <= weights[k]:
                    weights[k] = v + min_weight
            else:
                # 如果不在权重字典里则添加
                weights[k] = v + min_weight
    print(weights)


if __name__ == '__main__':
    graph = dict()
    graph['start'] = {'a': 6, 'b': 2}
    graph['a'] = {'stop': 1}
    graph['b'] = {'a': 3, 'stop': 5}
    graph['stop'] = {}
    bfs_weight_search(graph)
