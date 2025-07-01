#==============================================================
# Initialize p and T field for directional solidification
#==============================================================

"""
initialize.py - Initializes the phase-field and temperature fields.
"""

import numpy as np

def initialize_grid_and_fields(Nx, Ny, Lx, Ly, Nz=1, Lz=1.0, dim=2, T_liquid=0.0):
    """
    Initialize the phase field and temperature field arrays.

    Parameters:
        Nx (int): Number of grid points in X direction
        Ny (int): Number of grid points in Y direction
        Nz (int): Number of grid points in Z direction
        Lx, Ly, Lz (float) : Length of simulation in X, Y, Z directions
        dim (int) : Spacial dimension
        T_liquid (float): Initial temperature in the liquid region

    Returns:
        X, Y, Z : Coordinate grids (Z is None for 2D)
        tuple: p (phase field), T (temperature field), p_new ( new phase field  array)
    """

    x = np.linspace(0, Lx, Nx, endpoint=False)
    y = np.linspace(0, Ly, Ny, endpoint=False)

    solid_width = int(0.05 * Nx)  # 5% of domain as solid 

    if dim == 2:
        X, Y = np.meshgrid(x, y, indexing='ij')
        Z = None
        p = np.zeros((Nx, Ny))
        T = np.full((Nx, Ny), T_liquid)
        p_new = np.zeros_like(p)

        # Add initial solid seed
        p[:solid_width, :] = 1.0

    elif dim == 3:
        z = np.linspace(0, Lz, Nz, endpoint=False)
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        p = np.zeros((Nx, Ny, Nz))
        T = np.full((Nx, Ny, Nz), T_liquid)
        p_new = np.zeros_like(p)

        # Add initial solid seed
        p[:solid_width, :, :] = 1.0

    else:
        raise ValueError(f"Invalid dimension: {dim}. Must be 2 or 3.")

    return X, Y, Z, p, T, p_new
