import numpy as np
from numpy import multiply as mul
from numpy import divide as div
from solverfunctions.Integrate import integrate
from solverfunctions.Combine import combine
import matplotlib.pyplot as plt

def solve4matstress(Material_properties, R_material, y, zeta, step, New_radii_id_list):
    A = Material_properties.get('Spacial radii')
    G = Material_properties.get('Material growth function')
    mu = Material_properties.get('Mu')
    Gam_r = Material_properties.get('Material gamma r')
    Gam_z = Material_properties.get('Material gamma z')
    Gam_t = Material_properties.get('Material gamma t')
    R_m = R_material
    New_r_id_list = New_radii_id_list

    X = [x for x in np.arange(A[0], A[-1] + step / 10, step)]
    I_y_m_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                    mul(np.square(np.square(R_m)), mul(Gam_r, Gam_r)))
    I_y_m = integrate(A[0], A[-1], I_y_m_arg, A[0], step)
    I_t = integrate(A[0], A[-1], div(G,
                                     mul(X, mul(Gam_t, Gam_t))), A[0], step)

    Tau_m = mu * (I_t / zeta - I_y_m / zeta ** 3)


    Radial_stress_m =  Tau_m - Tau_m[-1]
    Tang_stress_m = Radial_stress_m + mu * (pow(div(R_m, mul(X, Gam_t)), 2)
                                            - pow(div(mul(X, mul(Gam_t, Gam_z)), zeta * R_m), 2))
    Long_stress_m = Radial_stress_m + mu * (pow(div(zeta, Gam_z), 2)
                                            - pow(div(mul(X, mul(Gam_t, Gam_z)), zeta * R_m), 2))
    return Radial_stress_m, Tang_stress_m, Long_stress_m

def solve4spacstress(Material_properties, R_spatial, y, zeta, step, Old_radii_id_list):
    A_new = Material_properties.get('Material radii')
    G = Material_properties.get('Spacial growth function')
    mu = Material_properties.get('Mu')
    Gam_r = Material_properties.get('Spacial gamma r')
    Gam_t = Material_properties.get('Spacial gamma t')
    Gam_z = Material_properties.get('Spacial gamma z')
    R_s = R_spatial
    Old_r_id_list = Old_radii_id_list

    X = [x for x in np.arange(A_new[0], A_new[-1] + step / 10, step)]

    if len(R_s) != len(G):
        X = np.delete(X, -1)
        G = np.delete(G, -1)
        Gam_r = np.delete(Gam_r, -1)
        Gam_t = np.delete(Gam_t, -1)
        Gam_z = np.delete(Gam_z, -1)

    I_y_s_arg = div(mul(mul(R_s, R_s), mul(G, G)),
                    mul(mul(mul(X, X), X), mul(Gam_r, Gam_r)))
    I_y_s = integrate(A_new[0], A_new[-1], I_y_s_arg, A_new[0], step)
    I_t = integrate(A_new[0], A_new[-1], div(X,
                                             mul(mul(R_s, R_s), mul(Gam_t, Gam_t))), A_new[0], step)

    Tau_s = mu * (I_t - I_y_s / zeta ** 2)

    Radial_stress_s = Tau_s - Tau_s[-1]
    Tang_stress_s = Radial_stress_s + mu * (np.square(div(X, mul(R_s, Gam_t)))
                                            - np.square(div(mul(R_s, mul(Gam_t, Gam_z)), X)) / zeta ** 2)
    Long_stress_s = Radial_stress_s + mu * (np.square(div(zeta, Gam_z))
                                            - np.square(div(mul(R_s, mul(Gam_t, Gam_z)), X)) / zeta ** 2)
    return Radial_stress_s, Tang_stress_s, Long_stress_s











