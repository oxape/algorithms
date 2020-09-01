from collections import deque


def person_is_seller(name):
    return name.endswith('m')


def breadth_first_search(graph):
    search_queue = deque()
    search_queue += graph['you']    # 这里会把值中对应的列表的每个元素都添加到deque
    searched = set()
    while search_queue:
        person = search_queue.popleft()
        if person in searched:
            print(f'{person} checked')
            continue
        if person_is_seller(person):
            print(f'{person} is a mango seller!')
            return True
        else:
            search_queue += graph[person]
            searched.add(person)
    return False


if __name__ == '__main__':
    graph = dict()
    graph['you'] = ['alice', 'bob', 'claire']
    graph['bob'] = ['anuj', 'peggy']
    graph['alice'] = ['peggy']
    graph['claire'] = ['thom', 'jonny']
    graph['anuj'] = []
    graph['peggy'] = []
    graph['thom'] = []
    graph['jonny'] = []
    breadth_first_search(graph)

    graph = dict()
    graph['you'] = ['alice', 'bob', 'claire']
    graph['bob'] = ['anuj', 'peggy']
    graph['alice'] = ['peggy']
    graph['claire'] = ['thom', 'jonny']
    graph['anuj'] = []
    graph['peggy'] = []
    graph['thom'] = []
    graph['jonny'] = []
    breadth_first_search(graph)
