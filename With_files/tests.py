import numpy as np
a = np.array([1, 2, 3, 4])
print(a[[True, True, False, False]])
print(32)


def f(x):
    return x


def g(x):
    return -x


print(g(2) + f(2))
