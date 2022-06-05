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
from solverfunctions.Solve4Stress import solve4matstress
from solverfunctions.Solve4Stress import solve4spacstress
from wx.lib.pubsub import pub


class GrowTask():
    def __init__(self, Gamma_r_text, Gamma_t_text, Gamma_z_text, A_list, mu, p_long, p_rad, dr_s=0.01, dr_m=0.01):

        A = A_list
        self.A = A
        self.dr_s = dr_s
        self.dr_m = dr_m

        Gamma_r_fl = [float(g) for g in Gamma_r_text]
        Gamma_t_fl = [float(g) for g in Gamma_t_text]
        Gamma_z_fl = [float(g) for g in Gamma_z_text]

        self.can_solve = 1
        out_of_bounds = 0
        if min(np.array(A)) <= 0:
            pub.sendMessage("logOutputPrint", message='Radii must be positive\n')
            print('Radii must be positive')
            self.can_solve = 0

        if max(np.array(A)) > 100:
            pub.sendMessage("logOutputPrint", message='Maximum radius is too big\n')
            print('Maximum radius is too big')
            self.can_solve = 0

        if min([min(Gamma_r_fl), min(Gamma_t_fl), min(Gamma_z_fl)]) <= 0:
            pub.sendMessage("logOutputPrint", message='Gamma coefficients must be positive\n')
            print('Gamma coefficients must be positive')
            self.can_solve = 0

        if max([max(Gamma_r_fl), max(Gamma_t_fl), max(Gamma_z_fl)]) > 10:
            pub.sendMessage("logOutputPrint", message='Maximum gamma coefficient is too big\n')
            print('Maximum gamma coefficient is too big')
            self.can_solve = 0

        if mu <= 0:
            pub.sendMessage("logOutputPrint", message='Mu must be positive\n')
            print('Mu must be positive')
            self.can_solve = 0

        if min(np.array(A[1:]) - np.array(A[0:-1])) / dr_s < 10:
            pub.sendMessage("logOutputPrint", message='Radii are too close to each other\n')
            print('Radii are too close to each other')
            self.can_solve = 0


        if self.can_solve == 1:

            Gamma_r_m_list = text2list(Gamma_r_text, A, dr_s)
            Gamma_t_m_list = text2list(Gamma_t_text, A, dr_s)
            Gamma_z_m_list = text2list(Gamma_z_text, A, dr_s)
            Gam_r_m = combine(Gamma_r_m_list, A, dr_s)
            Gam_t_m = combine(Gamma_t_m_list, A, dr_s)
            Gam_z_m = combine(Gamma_z_m_list, A, dr_s)
            G_s = mul(mul(Gam_r_m, Gam_t_m), Gam_z_m)

            X = [x for x in np.arange(A[0], A[-1] + dr_s / 2, dr_s)]
            I_g = integrate(A[0], A[-1], mul(G_s, X), A[0], dr_s)
            i_t = integrate(A[0], A[-1], div(G_s,
                                             mul(X, mul(Gam_t_m, Gam_t_m))), A[0], dr_s)[-1]
            i_z = integrate(A[0], A[-1], div(mul(G_s, X),
                                             mul(Gam_z_m, Gam_z_m)), A[0], dr_s)[-1]

            Material_properties = {'Mu': mu,
                                   'Spacial radii': A,
                                   'Material growth function': G_s,
                                   'Material gamma r': Gam_r_m,
                                   'Material gamma t': Gam_t_m,
                                   'Material gamma z': Gam_z_m,
                                   'Material radii': [None],
                                   'Spacial growth function': None,
                                   'Spacial gamma r': None,
                                   'Spacial gamma t': None,
                                   'Spacial gamma z': None
                                   }
            Boundary_conditions = {'Longitude pressure': p_long,
                                   'Radial pressure': p_rad}
            Pre_solved_integrals = {'I t': i_t,
                                    'I z': i_z,
                                    'I g': I_g}

            fun = lambda y: bcfunction(Material_properties, Boundary_conditions, Pre_solved_integrals, y, dr_s)

            y_lower, y_upper, out_of_bounds = locatezero(fun, dr_s, 10000, 10, 1)
            if out_of_bounds == 0:

                y, convergence = findzeronewton(fun, y_lower, y_upper, (y_upper + y_lower) / 2,
                                                max([10 ** -6, dr_s ** 2]), 100, dr_s)
                if convergence == 0:
                    pub.sendMessage("logOutputPrint", message='Newton method diverges\n')
                    print('Newton method diverges')
                    y_1, y_2, convergence = locatezero(fun, y_lower, y_upper, y_upper - y_lower,
                                                       max([10 ** -6, dr_s ** 2]))
                    y = (y_1 + y_2) / 2

                zeta, found_zeta = findzeta(Material_properties, Boundary_conditions, Pre_solved_integrals, y, dr_s)
                if found_zeta == 1:
                    R_m = np.sqrt(y / zeta + 2 / zeta * I_g)
                    R_s = findinverse(R_m, A[0], dr_s, dr_m)

                    New_r_id_list = []
                    New_r_id_list.append(0)
                    for i in range(0, len(A) - 1):
                        New_r_id_list.append(int(np.floor((A[i + 1] - A[0]) / dr_m)))
                    self.New_r_id_list = New_r_id_list

                    Old_r_id_list = []
                    Old_r_id_list.append(0)
                    for i in range(0, len(A) - 1):
                        Old_r_id_list.append(int(np.floor((R_m[New_r_id_list[i + 1]] - R_m[0]) / dr_s)))
                    self.Old_r_id_list = Old_r_id_list

                    Gamma_r_s_list = text2list(Gamma_r_text, R_m[New_r_id_list], dr_m)
                    Gamma_t_s_list = text2list(Gamma_t_text, R_m[New_r_id_list], dr_m)
                    Gamma_z_s_list = text2list(Gamma_z_text, R_m[New_r_id_list], dr_m)
                    Gam_r_s = combine(Gamma_r_s_list, R_m[New_r_id_list], dr_m)
                    Gam_t_s = combine(Gamma_t_s_list, R_m[New_r_id_list], dr_m)
                    Gam_z_s = combine(Gamma_z_s_list, R_m[New_r_id_list], dr_m)
                    G_s = mul(mul(Gam_r_s, Gam_t_s), Gam_z_s)

                    Material_properties['Material radii'] = R_m[New_r_id_list]
                    Material_properties['Spacial growth function'] = G_s
                    Material_properties['Spacial gamma r'] = Gam_r_s
                    Material_properties['Spacial gamma t'] = Gam_t_s
                    Material_properties['Spacial gamma z'] = Gam_z_s

                    R_stress_m, T_stress_m, L_stress_m \
                        = solve4matstress(Material_properties, R_m, y, zeta, dr_s, New_r_id_list)

                    R_stress_s, T_stress_s, L_stress_s \
                        = solve4spacstress(Material_properties, R_s, y, zeta, dr_m, Old_r_id_list)

                    self.R_stress_m = R_stress_m
                    self.T_stress_m = T_stress_m
                    self.L_stress_m = L_stress_m
                    self.R_stress_s = R_stress_s
                    self.T_stress_s = T_stress_s
                    self.L_stress_s = L_stress_s

                    self.R_m = R_m
                    self.R_s = R_s
                    self.zeta = zeta

                else:
                    pub.sendMessage("logOutputPrint", message='Cannot solve for axial stretch\n')
                    print('Cannot solve for axial stretch')
                    self.can_solve = 0
            else:
                pub.sendMessage("logOutputPrint", message='Solution is out of bounds\n')
                print('Solution is out of bounds')
                self.can_solve = 0



        if self.can_solve == 0:
            pub.sendMessage("logOutputPrint", message='Cannot solve with such input\n')
            print('Cannot solve with such input')
            if out_of_bounds == 1:
                pub.sendMessage("logOutputPrint", message='Try lower pressure or larger mu coefficient\n')

            self.R_m = [0]
            self.R_s = [0]
            self.zeta = 0
            self.R_stress_m = [0]
            self.T_stress_m = [0]
            self.L_stress_m = [0]
            self.R_stress_s = [0]
            self.T_stress_s = [0]
            self.L_stress_s = [0]
            self.New_r_id_list = 0
            self.Old_r_id_list = 0


    def getSpatialRadius(self):
        return {'R': self.R_s,
                'Old radii': self.R_s[self.Old_r_id_list],
                'Argument': [x for x in np.arange(self.R_m[0], self.R_m[-1] + self.dr_m / 10, self.dr_m)],
                'step': self.dr_m}

    def getMaterialRadius(self):
        return {'r': self.R_m,
                'New radii': self.R_m[self.New_r_id_list],
                'Argument': [x for x in np.arange(self.A[0], self.A[-1] + self.dr_s / 10, self.dr_s)],
                'step': self.dr_s}

    def getSpatialDissplacement(self):
        X = [x for x in np.arange(self.R_m[0], self.R_m[-1] + self.dr_m / 10, self.dr_m)]
        if len(self.R_s) != len(X):
            X = np.delete(X, -1)

        Disp = X - self.R_s
        return {'Displacement': Disp,
                'Displacement on radii': self.R_m[self.New_r_id_list] - self.R_s[self.Old_r_id_list],
                'Argument': X,
                'step': self.dr_m}

    def getMaterialDissplacement(self):
        Disp = self.R_m - [x for x in np.arange(self.A[0], self.A[-1] + self.dr_s / 10, self.dr_s)]
        return {'Displacement': Disp,
                'Displacement on radii': self.R_m[self.New_r_id_list] - self.R_s[self.Old_r_id_list],
                'Argument': [x for x in np.arange(self.A[0], self.A[-1] + self.dr_s / 10, self.dr_s)],
                'step': self.dr_s}

    def getAxialStretch(self):
        return self.zeta

    def IsSolved(self):
        return self.can_solve

    def getMaterialStresses(self):
        return {'Radial stress': self.R_stress_m,
                'Tangential stress': self.T_stress_m,
                'Longitudinal stress': self.L_stress_m,
                'Minimal radial stress': min(self.R_stress_m),
                'Minimal tangential stress': min(self.R_stress_m),
                'Minimal longitudinal stress': min(self.R_stress_m),
                'Maximal radial stress': max(self.R_stress_m),
                'Maximal tangential stress': max(self.R_stress_m),
                'Maximal longitudinal stress': max(self.R_stress_m),
                'Overall minimum': min(min(self.R_stress_m), min(self.T_stress_m), min(self.L_stress_m)),
                'Overall maximum': max(max(self.R_stress_m), max(self.T_stress_m), max(self.L_stress_m)),
                'Argument': [x for x in np.arange(self.A[0], self.A[-1] + self.dr_s / 10, self.dr_s)],
                'step': self.dr_s}

    def getSpacialStresses(self):
        X = [x for x in np.arange(self.R_m[0], self.R_m[-1] + self.dr_m / 10, self.dr_m)]
        if len(self.R_s) != len(X):
            X = np.delete(X, -1)
        return {'Radial stress': self.R_stress_s,
                'Tangential stress': self.T_stress_s,
                'Longitudinal stress': self.L_stress_s,
                'Minimal radial stress': min(self.R_stress_s),
                'Minimal tangential stress': min(self.R_stress_s),
                'Minimal longitudinal stress': min(self.R_stress_s),
                'Maximal radial stress': max(self.R_stress_s),
                'Maximal tangential stress': max(self.R_stress_s),
                'Maximal longitudinal stress': max(self.R_stress_s),
                'Overall minimum': min(min(self.R_stress_s), min(self.T_stress_s), min(self.L_stress_s)),
                'Overall maximum': max(max(self.R_stress_s), max(self.T_stress_s), max(self.L_stress_s)),
                'Argument': X,
                'step': self.dr_m}
