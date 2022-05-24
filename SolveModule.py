import wx
import numpy as np
from numpy import multiply as mul
from numpy import divide as div


class GrowTask(wx.Panel):
    def __init__(self, Gamma_r_list, Gamma_t_list, Gamma_z_list, A_list, mu, N, P, dr_s=0.001, dr_m=0.001):

        A = A_list
        self.dr_s = dr_s
        self.dr_m = dr_m

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

        def combine(Fun_list, A, dx):
            Fun_comb = []
            X_span = np.arange(A[0], A[-1] + dx, dx)
            len_A = len(A)

            shell_id = 0
            for x in X_span:
                if shell_id < len_A:
                    if x > A[shell_id]:
                        shell_id += 1
                Fun_comb.append(eval(Fun_list[shell_id]))

            return Fun_comb

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

        G_r = combine(Gamma_r_list, A, dr_s)
        G_t = combine(Gamma_t_list, A, dr_s)
        G_z = combine(Gamma_z_list, A, dr_s)
        G_f = mul(mul(G_r, G_t), G_z)

        a = A[0] ** 2
        zeta = 1
        y = zeta * a
        y_old = y

        X = [x for x in np.arange(A[0], A[-1] + dr_s, dr_s)]
        I_g = integrate(A[0], A[-1], mul(G_f, X), A[0], dr_s)
        i_t = integrate(A[0], A[-1], div(mul(G_f, X),
                                                   mul(G_t, G_t)), A[0], dr_s)[-1]
        i_z = integrate(A[0], A[-1], div(mul(G_f, X),
                                                   mul(G_z, G_z)), A[0], dr_s)[-1]

        I_y1_arg = div(mul(mul(mul(mul(X, X), X), mul(G_t, G_t)), mul(G_z, G_z)),
                       mul((y + 2 * I_g), (y + 2 * I_g)))
        I_y2_arg = div((y + 2 * I_g),
                       mul(X, mul(G_t, G_t)))
        i_y1 = integrate(A[0], A[-1], I_y1_arg, A[0], dr_s)[-1]
        i_y2 = integrate(A[0], A[-1], I_y2_arg, A[0], dr_s)[-1]
        zeta = mu / P * (i_t - i_y1)
        y = 1 / P * (zeta / np.pi * N - mu * zeta ** 2 * i_z + mu / zeta * i_y2)

        eps = abs(y_old - y)
        while eps >= 1e-6:
            y_old = y
            I_y1_arg = div(mul(mul(mul(mul(X, X), X), mul(G_t, G_t)), mul(G_z, G_z)),
                           mul((y + 2 * I_g), (y + 2 * I_g)))
            I_y2_arg = div((y + 2 * I_g),
                           mul(X, mul(G_t, G_t)))
            i_y1 = integrate(A[0], A[-1], I_y1_arg, A[0], dr_s)[-1]
            i_y2 = integrate(A[0], A[-1], I_y2_arg, A[0], dr_s)[-1]
            zeta = mu / P * (i_t - i_y1)
            y = 1 / P * (zeta / np.pi * N - mu * zeta ** 2 * i_z + mu / zeta * i_y2)
            eps = abs(y_old - y)

        i_y1 = integrate(A[0], A[-1], div(mul(mul(mul(mul(X, X), X), mul(G_t, G_t)), mul(G_z, G_z)),
                                                    mul((y + 2 * I_g), (y + 2 * I_g))), A[0], dr_s)[-1]
        zeta = mu / P * (i_t - i_y1)
        a = y / zeta

        self.R_s = np.sqrt(a + 2 / zeta * I_g)
        self.R_m = findinverse(self.R_s, A[0], dr_s, dr_m)

        self.Index_arr_s = []
        self.Index_arr_s.append(0)
        for i in range(0, len(A)-1):
            self.Index_arr_s.append(int(np.floor((A[i+1] - A[0])/dr_s) ))

        self.Index_arr_m = []
        self.Index_arr_m.append(0)
        for i in range(0, len(A)-1):
            self.Index_arr_m.append(int(np.floor((self.R_s[self.Index_arr_s[i+1]] - self.R_s[0])/dr_m)))

        print()

    def getMaterialRadius(self):
        return {'r': self.R_s, 'start': self.A[0], 'end': self.A[-1], 'step': self.dr_s,
                'Radius id': self.Index_arr_s}

    def getSpatialRadius(self):

        return {'R': self.R_m, 'start': min(self.R_s), 'end': max(self.R_s), 'step': self.dr_m,
                'Radius id': self.Index_arr_m}

    def getMaterialDissplacement(self):
        Diss = self.R_s - [x for x in np.linspace(self.A[0], self.A[-1], len(self.R_s))]
        return {'Diss': Diss, 'start': self.A[0], 'end': self.A[-1], 'step': self.dr_s,
                'Radius id': self.Index_arr_s}

    def getSpatiallDissplacement(self):
        Diss = [x for x in np.linspace(min(self.R_s), max(self.R_s), len(self.R_m))] - self.R_m
        return {'Diss': Diss, 'start': min(self.R_s), 'end': max(self.R_s), 'step': self.dr_m,
                'Radius id': self.Index_arr_m}
