


def partition(array, start, end):
    q = end-1
    x = array[q]
    i = start-1
    for j in range(start, end-1):
        if array[j] < x:
            i=i+1
            tmp = array[i]
            array[i] = array[j]
            array[j] = tmp
    tmp = array[i+1]
    array[i+1] = array[q]
    array[q] = tmp
    return i+1

def quick_sort(array, start, end):
    if end <= start+1:
        return
    q = partition(array, start, end)
    quick_sort(array, start, q)
    quick_sort(array, q+1, end)


if __name__ == '__main__':
    arr = [10, 12, 3, 1, 15, 5, 4, 20, 21, 18, 9, 10, 33, 17]
    
    quick_sort(arr, 0, len(arr))
    print(arr)