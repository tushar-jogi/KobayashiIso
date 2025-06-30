#==============================================================
# Initialize p and T field for directional solidification
#==============================================================

"""
initialize.py - Initializes the phase-field and temperature fields.
"""

import numpy as np

def initialize_fields(Nx, Ny, T_liquid=0.0):
    """
    Initialize the phase field and temperature field arrays.

    Parameters:
        Nx (int): Number of grid points in X direction
        Ny (int): Number of grid points in Y direction
        T_liquid (float): Initial temperature in the liquid region

    Returns:
        tuple: p (phase field), T (temperature field)
    """
    p = np.zeros((Nx, Ny))
    T = np.full((Nx, Ny), T_liquid)

    # Nucleation seed 
    solid_width = int(0.05*Nx)
    p[:solid_width, :] = 1.0

    return p, T
