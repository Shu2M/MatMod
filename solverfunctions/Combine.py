import numpy as np
def combine(Fun_list, A, dx):
    Fun_comb = np.zeros(len(Fun_list[0, :]))
    shell_id = 0
    for i in range(0, len(Fun_list[0, :])):
        if shell_id < len(A) - 2:
            if A[0] + i * dx >= A[shell_id + 1]:
                shell_id += 1
        Fun_comb[i] = Fun_list[shell_id, i]

    return Fun_comb
