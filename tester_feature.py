def foo(a):
    nn = a
    for i in range(len(a) - 1):
        print(nn[i])
        nn[i + 1] += 10


if __name__ == '__main__':
    foo([1, 2, 3, 4, 5, 6, 7, 8, 9])
