import numpy as np
def integrate(a, b, Fun, x0, h):
    a_id = 0
    b_id = 0
    da = h
    db = h

    for i in range(0, len(Fun)):
        if abs(x0 + i * h - a) <= da:
            a_id = i
            da = abs(x0 + i * h - a)
        if abs(x0 + i * h - b) <= db:
            b_id = i
            db = abs(x0 + i * h - b)

    if x0 + a_id * h >= a:
        s_a = da ** 2 / (4 * h) * (-3 * Fun[a_id] + 4 * Fun[a_id + 1] - Fun[a_id + 2]) + da * Fun[a_id]
    else:
        s_a = - da ** 2 / (4 * h) * (-3 * Fun[a_id] + 4 * Fun[a_id + 1] - Fun[a_id + 2]) - da * Fun[a_id]

    if x0 + b_id * h >= b:
        s_b = - db ** 2 / (4 * h) * (3 * Fun[b_id] - 4 * Fun[b_id - 1] + Fun[b_id - 2]) - db * Fun[b_id]
    else:
        s_b = db ** 2 / (4 * h) * (3 * Fun[b_id] - 4 * Fun[b_id - 1] + Fun[b_id - 2]) + db * Fun[b_id]

    S = [0]
    use_simpson = 0
    skip = 0
    for i in range(a_id + 1, b_id + 1):
        if (abs(Fun[i] - Fun[i - 1]) <= 1.5 * abs(Fun[i - 1] - Fun[i - 2])) | (i == 1) | (skip == 1):
            if use_simpson == 0:
                S.append(S[i - a_id - 1] + (Fun[i - 1] + Fun[i]) / 2 * h)
                use_simpson = 1
            else:
                S.append(S[i - a_id - 2] + h / 3 * (Fun[i - 2] + 4 * Fun[i - 1] + Fun[i]))
                use_simpson = 0
            skip = 0
        else:
            S.append(S[i - a_id - 1] + h / 4 * (7 * Fun[i - 1] - 4 * Fun[i - 2] + Fun[i - 3]))
            use_simpson = 0
            skip = 1

    S += s_a
    S[-1] += s_b
    return np.array(S)