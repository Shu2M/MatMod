import numpy as np
from solverfunctions.Integrate import integrate
from numpy import multiply as mul
from numpy import divide as div
def bcfunction(Material_properties, Boundary_conditions, Pre_solved_integrals, y, step):
    A = Material_properties.get('Spacial radii')
    G = Material_properties.get('Material growth function')
    mu = Material_properties.get('Mu')
    Gam_r = Material_properties.get('Material gamma r')
    Gam_t = Material_properties.get('Material gamma t')
    p_long = Boundary_conditions.get('Longitude pressure')
    p_rad = Boundary_conditions.get('Radial pressure')
    i_t = Pre_solved_integrals.get('I t')
    i_z = Pre_solved_integrals.get('I z')
    I_g = Pre_solved_integrals.get('I g')

    X = [x for x in np.arange(A[0], A[-1] + step / 10, step)]
    I_y1_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                   mul(mul(y + 2 * I_g, y + 2 * I_g), mul(Gam_r, Gam_r)))
    i_y1 = integrate(A[0], A[-1], I_y1_arg, A[0], step)[-1]
    if p_rad != 0:
        I_y2_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                       mul(y + 2 * I_g, mul(Gam_r, Gam_r)))
        I_y3_arg = div(mul(G, y + 2 * I_g),
                       mul(X, mul(Gam_t, Gam_t)))
        i_y2 = integrate(A[0], A[-1], I_y2_arg, A[0], step)[-1]
        i_y3 = integrate(A[0], A[-1], I_y3_arg, A[0], step)[-1]

        if p_rad >= 1:
            zeta = mu / p_rad * (i_t - i_y1)

            f = mu / p_rad * (2 * zeta ** 5 * i_z - i_y2 - i_y3 * zeta ** 2) \
                  + y * zeta ** 3 - zeta ** 4 * p_long / (np.pi * p_rad)
        else:
            zeta_p_rad = mu * (i_t - i_y1)

            f = mu * (2 * zeta_p_rad ** 5 * i_z - i_y2 * p_rad ** 5 - i_y3 * zeta_p_rad ** 2 * p_rad ** 3) \
                + y * zeta_p_rad ** 3 * p_rad ** 3 - zeta_p_rad ** 4 * p_long * p_rad / np.pi
    else:
        f = i_t - i_y1

    return f