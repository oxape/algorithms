import sys


def activity_selector_dynamic(s, f, n):
    c = {}
    root = {}
    for i in range(n):
        c[i] = {i+1: 0}
        root[i] = {i+1: i}
    for width in range(3, n+2):
        print(f'width={width}')
        for i in range(0, n-width+1+1):
            j = i+width-1
            print(f'\t({i}, {j})')
            c[i][j] = 0
            root[i][j] = i
            for k in range(i+1, j):
                # print(f'\t\t{k}')
                if s[k] < f[i] or s[j] < f[k]:
                    # print(f'\t\t contine 1 ({i} {k} {j})')
                    continue
                count = c[i][k] + c[k][j] + 1
                if count >= c[i][j]:
                    root[i][j] = k
                    c[i][j] = count
            # print(f'\t\tk = {root[i][j]}')
    return c, root


def activity_selector_dynamic_reduction(root, left, right):
    # print(f'reduction ({left}, {right})')
    k = root[left][right]
    if k >= left+1:
        # print(f'left')
        activity_selector_dynamic_reduction(root, left, k)
    if k != left and k != right:
        print(k)
    if right-1 >= k >= left+1:
        # print(f'right')
        activity_selector_dynamic_reduction(root, k, right)


def test():
    s = [0, 1, 3, 0, 5, 3, 5,  6,  8,  8,  2, 12, sys.maxsize]
    f = [0, 4, 5, 6, 7, 9, 9, 10, 11, 12, 14, 16, sys.maxsize]
    n = len(s)-1
    c, root = activity_selector_dynamic(s, f, n)
    print(f'c[0][12]={c[0][12]}')
    activity_selector_dynamic_reduction(root, 0, n)


if __name__ == '__main__':
    test()
