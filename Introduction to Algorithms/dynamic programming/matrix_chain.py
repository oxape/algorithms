import sys


def matrix_chain_order(p):
    n = len(p)
    m = {}
    s = {}
    for i in range(1, n):
        m[i] = {i: 0}
        s[i] = {i: i}
    for width in range(2, n):
        for i in range(1, n-width+1):
            j = i+width-1
            m[i][j] = sys.maxsize
            for k in range(i, j):
                q = m[i][k]+m[k+1][j]+p[i-1]*p[k]*p[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s


def matrix_chain_solution(s, start, end):
    if start == end:
        print('A', end='')
        s = []
        while start != 0:
            number = start % 10
            s.append(chr(0x2080+number))
            start //= 10
        print(''.join(s), end='')
        return
    k = s[start][end]
    print('(', end='')
    matrix_chain_solution(s, start, k)
    matrix_chain_solution(s, k+1, end)
    print(')', end='')


if __name__ == '__main__':
    a = [30, 35, 15, 5, 10, 20, 25]
    rm, rs = matrix_chain_order(a)
    print(rm[1][len(a)-1])
    matrix_chain_solution(rs, 1, len(a)-1)
