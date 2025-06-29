import numpy as np
from petsc4py import PETSc
from utils import initialize_fields, build_phase_matrix, build_heat_matrix

def test_initialize_fields():
    Nx, Ny = 100, 100
    p, T = initialize_fields(Nx, Ny, T_solid=1.0, T_liquid=0.0)
    assert p.shape == (Nx, Ny)
    assert T.shape == (Nx, Ny)
    assert np.allclose(p[:int(0.05*Nx), :], 1.0)
    assert np.allclose(T, 0.0)
