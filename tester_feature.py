SCALE = 10


def foo(a):
    return list(map(lambda i: SCALE * i, a))


if __name__ == '__main__':
    print(foo([1, 2, 3, 4, 5, 6, 7, 8, 9]))
