"""
boundary_conditions.py : Imposes boundary conditions for p and T
"""

def apply_boundary_conditions(p, T, T_cool=0.0):
    """
    Applies boundary conditions for phase-field and temperature fields.

    Phase field:
        - Neumann (zero-flux) on all boundaries

    Temperature field:
        - Dirichlet on left wall (x=0): T = T_cool
        - Neumann on all other faces

    Supports both 2D (Nx, Ny) and 3D (Nx, Ny, Nz) arrays.
    """

    if p is not None:
        # Phase field: Neumann BC
        if p.ndim == 2:
            p[0, :] = p[1, :]
            p[-1, :] = p[-2, :]
            p[:, 0] = p[:, 1]
            p[:, -1] = p[:, -2]
        elif p.ndim == 3:
            p[0, :, :] = p[1, :, :]
            p[-1, :, :] = p[-2, :, :]
            p[:, 0, :] = p[:, 1, :]
            p[:, -1, :] = p[:, -2, :]
            p[:, :, 0] = p[:, :, 1]
            p[:, :, -1] = p[:, :, -2]

    # Temperature field: Dirichlet left face, Neumann elsewhere
    if T.ndim == 2:
        T[0, :] = T_cool
        T[-1, :] = T[-2, :]
        T[:, 0] = T[:, 1]
        T[:, -1] = T[:, -2]
    elif T.ndim == 3:
        T[0, :, :] = T_cool
        T[-1, :, :] = T[-2, :, :]
        T[:, 0, :] = T[:, 1, :]
        T[:, -1, :] = T[:, -2, :]
        T[:, :, 0] = T[:, :, 1]
        T[:, :, -1] = T[:, :, -2]


