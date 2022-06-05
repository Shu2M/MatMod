import numpy as np
def combine(Fun_list, A, dx):
    Fun_comb = np.zeros(len(Fun_list[0, :]))
    shell = 0
    for i in range(0, len(Fun_list[0, :])):
        if shell < len(A) - 2:
            if A[0] + i * dx >= A[shell + 1]:
                shell += 1
        Fun_comb[i] = Fun_list[shell, i]

    return Fun_comb
