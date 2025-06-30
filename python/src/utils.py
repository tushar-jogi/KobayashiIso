#utils.py
import numpy as np
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from petsc4py import PETSc

def initialize_fields(Nx, Ny, T_liquid=0.0):

    p = np.zeros((Nx, Ny))
    T = np.full((Nx, Ny), T_liquid)

    # Nucleation seed
    solid_width = int(0.05*Nx)
    p[:solid_width, :] = 1.0

    return p, T




def apply_boundary_conditions(p, T, T_cool=0.0):
    """
    Apply boundary conditions to phase field (p) and temperature field (T)
    according to Kobayashi 1993 settings.

    Parameters:
    - p : 2D numpy array (phase field)
    - T : 2D numpy array (temperature field)
    - T_cool : float or None. If not None, Dirichlet BC applied on left wall of T
    - mode : "directional" or "adiabatic"
    """

    if p is not None:
        p[0, :]  = p[1, :]
        p[-1, :] = p[-2, :]
        p[:, 0]  = p[:, 1]
        p[:, -1] = p[:, -2]

    # Dirichlet on left, Neumann elsewhere for T
    T[0, :]  = T_cool
    T[-1, :] = T[-2, :]
    T[:, 0]  = T[:, 1]
    T[:, -1] = T[:, -2]

def m_func(T, alpha, gamma):
    return (alpha / np.pi) * np.arctan(gamma * (1.0 - T))






