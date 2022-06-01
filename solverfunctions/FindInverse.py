import numpy as np
def findinverse(Fun, x0, dx, dy):
    Fun_inv = []

    i = 0
    j = 0
    while Fun[0] + i * dy <= Fun[-1]:
        while (Fun[0] + i * dy < Fun[j]) | (Fun[0] + i * dy >= Fun[j + 1]):
            j += 1
        Fun_inv.append(1 / (Fun[j + 1] - Fun[j]) * (
                abs(Fun[0] + i * dy - Fun[j]) * (x0 + (j + 1) * dx) +
                abs(Fun[0] + i * dy - Fun[j + 1]) * (x0 + j * dx)))
        i += 1
    return np.array(Fun_inv)