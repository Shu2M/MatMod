import numpy as np
def text2list(Text_list, A, dx):
    X = [x for x in np.arange(A[0], A[-1] + dx / 10, dx)]
    Fun_list = np.zeros([len(Text_list), len(X)])
    for i in range(0, len(Text_list)):
        j = 0
        for x in X:
            if type(Text_list[i]) == 'string':
                Fun_list[i, j] = eval(Text_list[i])
                j += 1
            else:
                Fun_list[i, j] = Text_list[i]
                j += 1

    return Fun_list
