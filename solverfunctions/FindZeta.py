import numpy as np
from solverfunctions.Integrate import integrate
from numpy import multiply as mul
from numpy import divide as div
def findzeta(Material_properties, Boundary_conditions, Pre_solved_integrals, y, step):
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

    can_solve = 1
    if p_rad != 0:
        zeta = mu / p_rad * (i_t - i_y1)

        if zeta < 0:
            can_solve = 0
            print('Cannot solve for zeta')
            return zeta, can_solve
    else:
        I_y2_arg = div(mul(mul(mul(X, X), X), mul(mul(G, G), G)),
                       mul(y + 2 * I_g, mul(Gam_r, Gam_r)))
        I_y3_arg = div(mul(G, y + 2 * I_g),
                       mul(X, mul(Gam_t, Gam_t)))
        i_y2 = integrate(A[0], A[-1], I_y2_arg, A[0], step)[-1]
        i_y3 = integrate(A[0], A[-1], I_y3_arg, A[0], step)[-1]

        zeta = np.roots([2 * mu * i_z,
                         -p_long / np.pi,
                         0,
                         -mu * i_y3,
                         0,
                         -mu * i_y2])
        zeta = zeta.real[abs(zeta.imag) < 1e-5]
        if len(zeta[zeta > 0]) != 1:
            can_solve = 0
            print('Cannot solve for zeta')
            return zeta, can_solve
        zeta = zeta[zeta > 0][0]

    return zeta, can_solve