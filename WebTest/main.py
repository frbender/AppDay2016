a = [1, 2, 3, 4, 5]


def reverse(x):
    if len(x) == 0:
        return []
    a, b = (x[0], x[1:])
    return reverse(b) + [a]


print(reverse(a))
