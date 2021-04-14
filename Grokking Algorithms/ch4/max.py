
numbers = [3, 5, 6, 17, 9, 10, 40, 42, 23]


def max_recursion(array):
    if len(array) == 0:
        return 0
    elif len(array) == 1:
        return array[0]
    a = array[0]
    b = max_recursion(array[1:])
    if a > b:
        return a
    return b


if __name__ == "__main__":
    print(max_recursion(numbers))
