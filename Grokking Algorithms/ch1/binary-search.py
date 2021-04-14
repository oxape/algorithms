
sorted_list = [1, 2, 4, 5, 9, 10, 20, 23]


def binary_search(n, array):
    low = 0
    high = len(array)-1
    while low <= high:
        middle = (low+high)//2
        if n > array[middle]:
            low = middle+1
        elif n < array[middle]:
            high = middle-1
        else:
            return middle
    return None


def _binary_search_recursion(n, array, low, high):
    print('low = %d high = %d' % (low, high))
    # 终止
    if low > high:
        return None
    middle = (low + high) // 2
    print('middle = %d' % middle)
    # 终止
    if n == array[middle]:
        return middle
    if n > array[middle]:
        return _binary_search_recursion(n, array, middle+1, high)
    else:
        return _binary_search_recursion(n, array, low, middle-1)


def binary_search_recursion(n, array):
    low = 0
    high = len(array) - 1
    return _binary_search_recursion(n, array, low, high)


if __name__ == "__main__":
    # for e in sorted_list:
    #     result = binary_search(e, sorted_list)
    #     print(result)
    print('******')
    print(binary_search_recursion(20, [1]))
    print('******')
    print(binary_search_recursion(20, [20, 1]))
    print('******')
    print(binary_search_recursion(20, sorted_list))
