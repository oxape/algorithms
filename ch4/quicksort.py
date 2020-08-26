
def quicksort(array):
    if len(array) < 2:
        return array
    pivot = array[0]
    less = [i for i in array[1:] if i <= pivot]
    greater = [i for i in array[1:] if i > pivot]
    return quicksort(less) + [pivot] + quicksort(greater)


def quicksort_learning(array, depth=0, tips=None):
    if tips is not None:
        print(depth * 4 * ' ' + tips)
    print(depth*4*' ' + f'start {array}')
    if len(array) < 2:
        print(depth*4*' ' + f'base {array}')
        return array
    pivot = array[0]
    print(depth*4*' ' + f'pivot {pivot}')
    less = [i for i in array[1:] if i <= pivot]
    greater = [i for i in array[1:] if i > pivot]
    array = quicksort_learning(less, depth+1, 'less') + [pivot] + quicksort_learning(greater, depth+1, 'greater')
    print(depth*4*' ' + f'result {array}')
    return array


if __name__ == "__main__":
    print(quicksort_learning([10, 5, 2, 3, 8]))
