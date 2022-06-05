import numpy as np

def findzeronewton(fun, a, b, x_0, eps, max_n, dx):

    f = fun(x_0)
    dir_f = (fun(x_0 + dx) - f) / dx
    n = 0
    convergence = 1
    while abs(f / dir_f) > eps:
        f = fun(x_0)
        dir_f = (fun(x_0 + dx) - f) / dx
        x_0 = x_0 - f / dir_f
        n += 1
        if (n >= max_n) | (x_0 < 2 * a - b) | (x_0 > 2 * b - a) | (x_0 < 0):
            convergence = 0
            return x_0, convergence

    return x_0, convergence
