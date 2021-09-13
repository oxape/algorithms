from graphviz import Graph


def optimal_bst(p, q, n):
    root = {}
    e = {}
    w = {}
    for i in range(1, n+1):
        root[i] = {}
    for i in range(1, n+2):
        e[i] = {i-1: q[i-1]}
        w[i] = {i-1: q[i-1]}
    print(e)
    print(w)
    for width in range(1, n+1):
        print(f'width={width}')
        for i in range(1, n-width+1+1):
            j = i+width-1
            print(f'\ti={i}')
            e[i][j] = float("inf")
            w[i][j] = w[i][j-1] + p[j] + q[j]
            for r in range(i, j+1):
                print(f'\t\t({i},{r-1}) ({r+1},{j})')
                t = e[i][r-1] + e[r+1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t
                    root[i][j] = r
    return e, root


def render_tree(root, left, right, p=None, graph=None):
    if graph is None:
        graph = Graph(format='png')
    r = root[left][right]
    print(f'({left}, {right}) {r} {p}')
    graph.node(f'k{r}')
    if p is not None:
        graph.edge(f'k{p}', f'k{r}')
    if r > left:
        render_tree(root, left, r-1, r, graph)
    else:
        graph.node(f'd{r-1}')
        graph.edge(f'k{r}', f'd{r-1}')
    if r < right:
        render_tree(root, r+1, right, r, graph)
    else:
        graph.node(f'd{r}')
        graph.edge(f'k{r}', f'd{r}')
    return graph


def test():
    p = [0, 0.15, 0.10, 0.05, 0.10, 0.20]
    q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]
    n = len(p)-1
    e, root = optimal_bst(p, q, n)
    g = render_tree(root, 1, n)
    g.render(filename='g', view=True)


if __name__ == '__main__':
    test()
