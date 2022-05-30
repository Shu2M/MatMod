import numpy as np
from numpy import multiply as mul
from numpy import divide as div


class GrowTask():
    def __init__(self, Gamma_r_text, Gamma_t_text, Gamma_z_text, A_list, mu, N, P, dr_s=0.01, dr_m=0.01):

        A = A_list
        self.A = A
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

        def text2list(Text_list, A, dx):
            X = [x for x in np.arange(A[0], A[-1] + dx/2, dx)]
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

        def combine(Fun_list, A, dx):
            Fun_comb = np.zeros(len(Fun_list[0, :]))
            shell_id = 0
            for i in range(0, len(Fun_list[0, :])):
                if shell_id < len(A) - 2:
                    if A[0] + i*dx >= A[shell_id + 1]:
                        shell_id += 1
                Fun_comb[i] = Fun_list[shell_id, i]

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

        Gamma_r_list = text2list(Gamma_r_text, A, dr_s)
        Gamma_t_list = text2list(Gamma_t_text, A, dr_s)
        Gamma_z_list = text2list(Gamma_z_text, A, dr_s)
        Gam_r = combine(Gamma_r_list, A, dr_s)
        Gam_t = combine(Gamma_t_list, A, dr_s)
        Gam_z = combine(Gamma_z_list, A, dr_s)
        G = mul(mul(Gam_r, Gam_t), Gam_z)

        a = A[0] ** 2
        zeta = 1
        y = a*zeta
        lam = 10 ** -1

        ###
        X = [x for x in np.arange(A[0], A[-1] + dr_s/2, dr_s)]
        I_g = integrate(A[0], A[-1], mul(G, X), A[0], dr_s)
        i_t = integrate(A[0], A[-1], div(G,
                                         mul(X, mul(Gam_t, Gam_t))), A[0], dr_s)[-1]
        i_z = integrate(A[0], A[-1], div(mul(G, X),
                                         mul(Gam_z, Gam_z)), A[0], dr_s)[-1]

        eps = 1
        dx = dr_s
        while eps >= 1e-6:
            I_y1_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                           mul(mul(y + dx + 2 * I_g, y + dx + 2 * I_g), mul(Gam_r, Gam_r)))
            I_y2_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                           mul(y + dx + 2 * I_g, mul(Gam_r, Gam_r)))
            I_y3_arg = div(mul(G, y + dx + 2 * I_g),
                           mul(X, mul(Gam_t, Gam_t)))
            i_y1 = integrate(A[0], A[-1], I_y1_arg, A[0], dr_s)[-1]
            i_y2 = integrate(A[0], A[-1], I_y2_arg, A[0], dr_s)[-1]
            i_y3 = integrate(A[0], A[-1], I_y3_arg, A[0], dr_s)[-1]
            zeta = mu / P * (i_t - i_y1)
            f_1 = mu / (N * P) * (2 * zeta ** 5 * i_z - i_y2 - i_y3 * zeta ** 2)\
                  + y * zeta ** 3 / N - zeta ** 4 / (np.pi * P)

            I_y1_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                           mul(mul(y + 2 * I_g, y + 2 * I_g), mul(Gam_r, Gam_r)))
            I_y2_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                           mul(y + 2 * I_g, mul(Gam_r, Gam_r)))
            I_y3_arg = div(mul(G, y + 2 * I_g),
                           mul(X, mul(Gam_t, Gam_t)))
            i_y1 = integrate(A[0], A[-1], I_y1_arg, A[0], dr_s)[-1]
            i_y2 = integrate(A[0], A[-1], I_y2_arg, A[0], dr_s)[-1]
            i_y3 = integrate(A[0], A[-1], I_y3_arg, A[0], dr_s)[-1]
            zeta = mu / P * (i_t - i_y1)
            f_0 = mu / (N * P) * (2 * zeta ** 5 * i_z - i_y2 - i_y3 * zeta ** 2)\
                  + y * zeta ** 3 / N - zeta ** 4 / (np.pi * P)

            y = y - dx / (f_1 - f_0) * f_0
            eps = abs(dx / (f_1 - f_0) * f_0)

        I_y1_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                       mul(mul(y + 0.01 + 2 * I_g, y + 0.01 + 2 * I_g), mul(Gam_r, Gam_r)))
        i_y1 = integrate(A[0], A[-1],  I_y1_arg, A[0], dr_s)[-1]
        zeta = mu / P * (i_t - i_y1)
        a = y / zeta

        self.R_m = np.sqrt(a + 2 / zeta * I_g)
        self.R_s = findinverse(self.R_m, A[0], dr_s, dr_m)
        self.zeta = zeta

        ###
        self.Index_arr_m = []
        self.Index_arr_m.append(0)
        for i in range(0, len(A) - 1):
            self.Index_arr_m.append(int(np.floor((A[i+1] - A[0]) / dr_m)))

        self.Index_arr_s = []
        self.Index_arr_s.append(0)
        for i in range(0, len(A) - 1):
            self.Index_arr_s.append(int(np.floor((self.R_m[self.Index_arr_m[i+1]] - self.R_m[0]) / dr_s)))

    def getSpatialRadius(self):
        return {'r': self.R_s, 'New radii': self.R_s[self.Index_arr_s], 'step': self.dr_m}

    def getMaterialRadius(self):
        return {'R': self.R_m, 'Old radii': self.R_m[self.Index_arr_m], 'step': self.dr_s}

    def getSpatialDissplacement(self):
        Disp = self.R_m - [x for x in np.linspace(self.A[0], self.A[-1], len(self.R_m))]
        return {'Displacement': Disp,
                'Displacement on radii ': self.R_m[self.Index_arr_m] - self.R_s[self.Index_arr_s],
                'step': self.dr_m}

    def getMaterialDissplacement(self):
        Disp = [x for x in np.linspace(min(self.R_m), max(self.R_m), len(self.R_s))] - self.R_s
        return {'Displacement': Disp,
                'Displacement on radii ': self.R_m[self.Index_arr_m] - self.R_s[self.Index_arr_s],
                'step': self.dr_s}

    def getZeta(self):
        return self.zeta
