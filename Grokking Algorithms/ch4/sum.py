
numbers = [3, 5, 6, 17, 9, 10, 40, 23]


def sum_recursion(array):
    if len(array) == 0:
        return 0
    elif len(array) == 1:
        return array[0]
    return sum_recursion(array[1:])+array[0]


def sum_loop(array):
    result = 0
    for e in array:
        result = result + e
    return result


if __name__ == "__main__":
    print(sum_recursion(numbers))
    print(sum_loop(numbers))
