class Item:
    def __init__(self, key, value):
        super().__init__()
        self.key = key
        self.value = value    

def print_array(arr):
    string = '['
    for i in range(len(arr)):
        string = string+f'{arr[i]:2d}, '
    string += ']'
    return string

def counting_sort(arr, k):
    count_arr = [0]*k
    b = [0]*len(arr)
    for i in range(len(arr)):
        count_arr[arr[i]] += 1
    index = 0
    for i in range(k):
        if count_arr[i] > 0:
            b[index:index+count_arr[i]] = [i]*count_arr[i]
            '''
            or 使用下面的循环
            j = 0
            while j< count_arr[i]:
                b[index+j] = i
            '''
            index += count_arr[i]
    return b

def counting_sortV2(arr, k): #探究稳定排序的本质
    count_arr = [0]*k
    b = [0]*len(arr)
    arr = [Item(arr[i], i) for i in range(len(arr))]
    for i in range(len(arr)):
        count_arr[arr[i].key] += 1
    # 方法1 稳定排序
    for i in range(1, k):
        count_arr[i] += count_arr[i-1]
    for i in reversed(range(len(arr))): # 稳定排序的关键是这里输出数组是要从后往前，或者采用方法2
        b[count_arr[arr[i].key]-1] = arr[i]
        count_arr[arr[i].key] -= 1
    # 方法2 稳定排序
    '''
    repeat_count = [0]*k
    for i in range(0, k):
        repeat_count[i] = count_arr[i]
    # count_arr存储的是当前值等于i的元素加上比i小的元素有多少个
    for i in range(1, k):
        count_arr[i] += count_arr[i-1]
    for i in range(len(arr)):
        # 排在当前key的元素有几个，包括当前key，例如，[0, 1, 1]，第一次遇到1时count_arr[arr[i].key]=3，所以需要减1
        index = count_arr[arr[i].key]-1
        # 相同的key的个数
        repeat = repeat_count[arr[i].key]
        # arr中排在前面的数据应该往前放，往前放多少个取决于相同的key有多少个，相同的key有2个，第一个出现的key就往前放1个位置，有3个就往前放2两个位置
        index -= repeat-1
        print(f'key = {arr[i].key} index = {index} repeat = {repeat}')
        b[index] = arr[i]
        repeat_count[arr[i].key] -= 1
    '''
    for e in b:
        print(f'k={e.key} v={e.value}')
    return b

if __name__ == '__main__':
    k = 10 # 所有元素小于10
    arr = [1, 3, 8, 3, 9, 0, 7, 6, 6, 4, 4, 5]
    print(f'len(arr) = {len(arr)}')
    print(f'index  = {print_array([i for i in range(len(arr))])}')
    print(f'arr    = {print_array(arr)}')
    result = counting_sort(arr, k)
    print(f'####################')
    print(f'sort   = {print_array(sorted(arr))}')
    print(f'result = {print_array(result)}')
    counting_sortV2(arr, k)
    
