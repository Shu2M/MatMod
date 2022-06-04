import numpy as np
from numpy import multiply as mul
from numpy import divide as div
from solverfunctions.Integrate import integrate
from solverfunctions.Combine import combine

def solve4matstress(Material_properties, Pre_solved_integrals, R_material, y, zeta, step, New_radii_id_list):
    A = Material_properties.get('Spacial radii')
    G = Material_properties.get('Material growth function')
    mu = Material_properties.get('Mu')
    Gam_r = Material_properties.get('Material gamma r')
    Gam_z = Material_properties.get('Material gamma z')
    Gam_t = Material_properties.get('Material gamma t')
    i_t = Pre_solved_integrals.get('I t')
    R_m = R_material
    New_r_id_list = New_radii_id_list

    X = [x for x in np.arange(A[0], A[-1] + step / 10, step)]
    I_y_m_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                   mul(mul(R_m, R_m), mul(Gam_r, Gam_r)))
    I_y_m = integrate(A[0], A[-1], I_y_m_arg, A[0], step)

    Tau_last_m = mu / zeta * (i_t - I_y_m)
    Tau_m = np.zeros([len(A) - 1, len(Tau_last_m)])
    shell = 0
    for i in range(0, len(A) - 1):
        id = New_r_id_list[i]
        Tau_m[shell, :] = Tau_last_m - Tau_last_m[id]
        shell += 1

    Radial_stress_m = combine(Tau_m, A, step)
    Tang_stress_m = Radial_stress_m + mu * (pow(div(R_m, mul(X, Gam_t)), 2)
                                            - pow(div(mul(X, mul(Gam_t, Gam_z)), zeta * R_m), 2))
    Long_stress_m = Radial_stress_m + mu * (pow(div(zeta, Gam_z), 2)
                                            - pow(div(mul(X, mul(Gam_t, Gam_z)), zeta * R_m), 2))
    return Radial_stress_m, Tang_stress_m, Long_stress_m

def solve4spacstress(Material_properties, Pre_solved_integrals, R_spatial, y, zeta, step, Old_radii_id_list):
    A_new = Material_properties.get('Material radii')
    G = Material_properties.get('Spacial growth function')
    mu = Material_properties.get('Mu')
    Gam_r = Material_properties.get('Spacial gamma r')
    Gam_t = Material_properties.get('Spacial gamma t')
    Gam_z = Material_properties.get('Spacial gamma z')
    i_t = Pre_solved_integrals.get('I t')
    R_s = R_spatial
    Old_r_id_list = Old_radii_id_list

    X = [x for x in np.arange(A_new[0], A_new[-1] + step / 10, step)]
    I_y_s_arg = div(mul(mul(R_s, R_s), mul(G, G)),
                    mul(mul(X, X), X), mul(Gam_r, Gam_r))
    I_y_s = integrate(A_new[0], A_new[-1], I_y_s_arg, A_new[0], step)

    Tau_last_s = mu * (i_t / zeta - I_y_s)
    Tau_s = np.zeros([len(A_new) - 1, len(Tau_last_s)])
    shell = 0
    for i in range(0, len(A_new) - 1):
        id = Old_r_id_list[i]
        Tau_s[shell, :] = Tau_last_s - Tau_last_s[id]
        shell += 1

    Radial_stress_s = combine(Tau_s, A_new, step)
    Tang_stress_s = Radial_stress_s + mu * (np.square(div(X, mul(R_s, Gam_t)))
                                            - np.square(div(mul(R_s, mul(Gam_t, Gam_z)), X)) / zeta ** 2)
    Long_stress_s = Radial_stress_s + mu * (np.square(div(zeta, Gam_z))
                                            - np.square(div(mul(R_s, mul(Gam_t, Gam_z)), X)) / zeta ** 2)
    return Radial_stress_s, Tang_stress_s, Long_stress_s











