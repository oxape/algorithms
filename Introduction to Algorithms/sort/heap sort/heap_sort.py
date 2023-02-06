
def parent(i):
    return (i+1)//2-1

def left_child(i):
    return i*2+1

def right_child(i):
    return i*2+2

# 不包括end
def heap_max_heapify(array, i, end):
    left = left_child(i)
    right = right_child(i)
    largest = i
    if left < end and array[left] > array[i]:
        largest = left
    if right < end and array[right] > array[largest]:
        largest = right
    if largest != i:
        tmp = array[i]
        array[i] = array[largest]
        array[largest] = tmp
        heap_max_heapify(array, largest, end)

def heap_build_max(array):
    pass

def heap_sort(array):
    n = len(array)
    if n <= 1:
        return
    # 包括0
    for i in range(n//2-1, -1, -1):
        print(i)
        heap_max_heapify(array, i, n)

    # 不包括0, i=1时，此时数组只剩2个元素，第0个元素为大于第1个元素
    for i in range(n-1, 0, -1):
        tmp = array[i]
        array[i] = array[0]
        array[0] = tmp
        n = n-1 # i=1时，运行到这里n=1，此时[0, n)里只有一个元素
        heap_max_heapify(array, 0, n)

    print(array)

if __name__ == '__main__':
    a = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
    # a = [4, 1, 3, 2, 16, 9, 10, 14]
    heap_sort(a)