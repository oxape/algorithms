
sorted_list = [1, 2, 4, 5, 9, 10, 20, 23]

def binary_searcy(n, sorted_list):
    low = 0
    high = len(sorted_list)-1
    while low < high:
        middle = (low+high)//2
        if n > sorted_list[middle]:
            low = middle
        elif n < sorted_list[middle]:
            high = middle
        else:
            return middle
    if low == n:
        return low
    return None

if __name__ == "__main__":
    result = binary_searcy(23, sorted_list)
    for e in sorted_list:
        result = binary_searcy(e, sorted_list)
        print(result)
