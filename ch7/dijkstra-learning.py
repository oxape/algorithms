"""
学习迪克斯拉特算法
"""


def bfs_weights_list(graph: dict, start: str):
    """ 打印出起点到所有节点的最短加权路径值

    Args:
        graph: 权重图字典
        graph = dict()
        graph['start'] = {'a': 6, 'b': 2}
        graph['a'] = {'stop': 1}
        graph['b'] = {'a': 3, 'stop': 5}
        graph['stop'] = {}
        start: 起点
    """
    weights = dict()
    searched = set()
    # 加入起点到所有邻居节点的权重到权重字典
    for k, v in graph[start].items():
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
        # 感觉下面这个if内的print不会执行，但是没有论证过
        if min_node is None:
            print('min node is None')
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
    else:
        print('all node check')
    print(weights)


def bfs_path_search(graph: dict, start: str, end: str):
    """ 找出起点到终点的最短加权路径

    Args:
        graph: 权重图字典
        graph = dict()
        graph['start'] = {'a': 6, 'b': 2}
        graph['a'] = {'stop': 1}
        graph['b'] = {'a': 3, 'stop': 5}
        graph['stop'] = {}
        start: 起点
        end: 终点
    """
    weights = dict()
    parents = dict()
    searched = set()
    # 加入起点到所有邻居节点的权重到权重字典
    for k, v in graph[start].items():
        weights[k] = v
        parents[k] = start
    # 所有节点都更新过它的邻居节点权重停止
    while len(searched) != len(weights):
        # print(weights)
        min_weight = float('inf')
        min_node = None
        # 遍历所有权重节点找到距离起点最短的节点（不一定是直接距离，有可能是间接距离，当然也不是边数）
        # 这里可以优化减少遍历次数，例如加个index，只遍历index之后的，待尝试
        for k, v in weights.items():
            if v <= min_weight:
                # 如果已经搜索过相应节点的邻居节点就忽略，感觉可以添加index优化减少遍历次数
                if k in searched:
                    # print(f'{k} already check')
                    continue
                else:
                    min_weight = v
                    min_node = k
        # 感觉下面这个if内的print不会执行，但是没有论证过
        if min_node is None:
            # print('min node is None')
            break
        searched.add(min_node)
        # 遍历min_node的邻居节点更新，权重字典weights
        for k, v in graph[min_node].items():
            if k in weights:
                # 如果经过这个节点到起点的距离比已经
                if v + min_weight <= weights[k]:
                    weights[k] = v + min_weight
                    parents[k] = min_node
            else:
                # 如果不在权重字典里则添加
                weights[k] = v + min_weight
                parents[k] = min_node
    else:
        # print('all node check')
        pass
    print(weights)
    print(parents)
    parent = end
    path = [end]
    while parent != start:
        parent = parents[parent]
        path.append(parent)
    path.reverse()
    print(path)


if __name__ == '__main__':
    graph = dict()
    graph['start'] = {'a': 6, 'b': 2}
    graph['a'] = {'stop': 1}
    graph['b'] = {'a': 3, 'stop': 5}
    graph['stop'] = {}
    bfs_weights_list(graph, 'start')

    graph = dict()
    graph['乐谱'] = {'黑胶唱片': 5, '海报': 0}
    graph['黑胶唱片'] = {'低音吉他': 15, '架子鼓': 20}
    graph['海报'] = {'低音吉他': 30, '架子鼓': 35}
    graph['低音吉他'] = {'钢琴': 20}
    graph['架子鼓'] = {'钢琴': 10}
    graph['钢琴'] = {}
    # bfs_weights_list(graph, '海报')
    bfs_path_search(graph, '乐谱', '钢琴')
