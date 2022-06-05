import numpy as np

def locatezero(fun, a, b, init_interval, eps):
    r = init_interval
    a_new = a
    b_new = a + r

    out_of_range = 0
    if fun(a) * fun(b) > 0:
        out_of_range = 1
        return a_new, b_new, out_of_range

    while fun(a_new) * fun(b_new) > 0:
        r = b_new - a_new
        a_new = b_new
        b_new = b_new + r * 2

    while r > eps:
        r = b_new - a_new
        b_new = a_new + r / 2
        if fun(a_new) * fun(b_new) > 0:
            a_new = b_new
            b_new = a_new + r / 2
        r = b_new - a_new

    return a_new, b_new, out_of_range