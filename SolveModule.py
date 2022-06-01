import numpy as np
from numpy import multiply as mul
from numpy import divide as div
from solverfunctions.Integrate import integrate
from solverfunctions.Combine import combine
from solverfunctions.Text2List import text2list
from solverfunctions.FindInverse import findinverse
from solverfunctions.BCFunction import bcfunction
from solverfunctions.LocateZero import locatezero
from solverfunctions.FindZeroNewton import findzeronewton
from solverfunctions.FindZeta import findzeta
'''
import matplotlib.pyplot as plt
'''

class GrowTask():
    def __init__(self, Gamma_r_text, Gamma_t_text, Gamma_z_text, A_list, mu, p_long, p_rad, dr_s=0.01, dr_m=0.01):

        A = A_list
        self.A = A
        self.dr_s = dr_s
        self.dr_m = dr_m

        Gamma_r_list = text2list(Gamma_r_text, A, dr_s)
        Gamma_t_list = text2list(Gamma_t_text, A, dr_s)
        Gamma_z_list = text2list(Gamma_z_text, A, dr_s)
        Gam_r = combine(Gamma_r_list, A, dr_s)
        Gam_t = combine(Gamma_t_list, A, dr_s)
        Gam_z = combine(Gamma_z_list, A, dr_s)
        G = mul(mul(Gam_r, Gam_t), Gam_z)

        X = [x for x in np.arange(A[0], A[-1] + dr_s / 2, dr_s)]
        I_g = integrate(A[0], A[-1], mul(G, X), A[0], dr_s)
        i_t = integrate(A[0], A[-1], div(G,
                                         mul(X, mul(Gam_t, Gam_t))), A[0], dr_s)[-1]
        i_z = integrate(A[0], A[-1], div(mul(G, X),
                                         mul(Gam_z, Gam_z)), A[0], dr_s)[-1]

        Material_properties = {'Radii': A,
                               'Growth function': G,
                               'Mu': mu,
                               'Gamma r': Gam_r,
                               'Gamma t': Gam_t,
                               'Gamma z': Gam_z}
        Boundary_conditions = {'Longitude pressure': p_long,
                               'Radial pressure': p_rad}
        Pre_solved_integrals = {'I t': i_t,
                                'I z': i_z,
                                'I g': I_g}

        fun = lambda y: bcfunction(Material_properties, Boundary_conditions, Pre_solved_integrals, y, dr_s)

        '''
        #######################
        F = []
        y_span = np.arange(15, 16, 0.1)
        for y in y_span:
            F.append(fun(y))

        plt.plot(y_span, F)
        plt.plot([y_span[0], y_span[-1]], [0, 0])
        plt.show()
        #######################
        '''

        self.can_solve = 1
        y_lower, y_upper, out_of_range = locatezero(fun, 0.1, 10000, 10, 1)
        if out_of_range == 0:

            y, convergence = findzeronewton(fun, y_lower, y_upper, (y_upper + y_lower) / 2, 10 ** -6, 100, dr_s)
            if convergence == 0:
                y_1, y_2, convergence = locatezero(fun, y_lower, y_upper, y_upper - y_lower, 10 ** -6)
                y = (y_1 + y_2) / 2

            zeta, found_zeta = findzeta(Material_properties, Boundary_conditions, Pre_solved_integrals, y, dr_s)
            if found_zeta == 1:
                self.R_m = np.sqrt(y / zeta + 2 / zeta * I_g)
                self.R_s = findinverse(self.R_m, A[0], dr_s, dr_m)
                self.zeta = zeta

                self.Index_arr_m = []
                self.Index_arr_m.append(0)
                for i in range(0, len(A) - 1):
                    self.Index_arr_m.append(int(np.floor((A[i + 1] - A[0]) / dr_m)))

                self.Index_arr_s = []
                self.Index_arr_s.append(0)
                for i in range(0, len(A) - 1):
                    self.Index_arr_s.append(int(np.floor((self.R_m[self.Index_arr_m[i + 1]] - self.R_m[0]) / dr_s)))

            else:
                self.can_solve = 0
        else:
            self.can_solve = 0

        if self.can_solve == 0:
            print('Cannot solve with such input')
            self.R_m = [None]
            self.R_s = [None]
            self.zeta = None
            self.Index_arr_m = 0
            self.Index_arr_s = 0


    def getSpatialRadius(self):
        return {'r': self.R_s, 'Old radii': self.R_s[self.Index_arr_s], 'step': self.dr_m}

    def getMaterialRadius(self):
        return {'R': self.R_m, 'New radii': self.R_m[self.Index_arr_m], 'step': self.dr_s}

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

    def IsSolved(self):
        return self.can_solve
