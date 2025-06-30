"""
boundary_conditions.py : Imposes boundary conditions for p and T
"""

def apply_boundary_conditions(p, T, T_cool=0.0):
    """
    Imposes the BCs for phase-field and temperature.
    Neumann BC at all walls for phase-field.
    Dirichlet BC at left wall and Neumann BC at remaining walls for Temperature field.

    Parameters:
        
    """
    if p is not None:
        p[0, :] = p[1, :]
        p[-1, :] = p[-2, :]
        p[:, 0] = p[:, 1]
        p[:, -1] = p[:, -2]

    T[0, :] = T_cool
    T[-1, :] = T[-2, :]
    T[:, 0] = T[:, 1]
    T[:, -1] = T[:, -2]
