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
        s_a = Fun[a_id] * da
    else:
        s_a = -Fun[a_id] * da

    if x0 + b_id * h >= b:
        s_b = -Fun[b_id] * db
    else:
        s_b = Fun[b_id] * db

    S = [0]
    for i in range(a_id + 1, b_id + 1):
        if (i - a_id) % 2 == 1:
            S.append(S[i - a_id - 1] + (Fun[i - 1] + Fun[i]) / 2 * h)
        else:
            S.append(S[i - a_id - 2] + h / 3 * (Fun[i - 2] + 4 * Fun[i - 1] + Fun[i]))
    S += s_a
    S[-1] += s_b
    return np.array(S)