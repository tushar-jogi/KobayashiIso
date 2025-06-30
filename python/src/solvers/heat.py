"""
heat.py : Solves the heat equation
"""
import numpy as np
from petsc4py import PETSc
from solvers.matrix import build_heat_matrix

def solve_heat_equation(T, dpdt, dt, dx, Nx, Ny, K):
    """
    Solves the heat equation using implicit Backward Euler method

    Parameters:
        T (ndarray) : Temperature field
        dpdt (ndarray) : Coupling to phase-field
        K (float) : latent heat
        dt (float) : time step
        dx (float) : grid size
        Nx (int) : Number of grid points in X
        Ny (int) : Number of grid points in Y

    Returns:
        T (ndarray) : New solution of T

    """
    A = build_heat_matrix(Nx, Ny, dx, dt)
    b = T.flatten() + dt * K * dpdt.flatten()

    # Dirichlet BC on left wall
    I = lambda i, j: i * Ny + j
    for j in range(Ny):
        b[I(0, j)] = 0.0

    b_vec = PETSc.Vec().createWithArray(b)
    x_vec = PETSc.Vec().createSeq(Nx *Ny)

    ksp = PETSc.KSP().create();
    ksp.setOperators (A);
    ksp.solve(b_vec, x_vec)

    if ksp.getConvergedReason() <= 0:
        print("WARNING: PETSc heat solver did not converge.")

    return x_vec.getArray().reshape ((Nx, Ny))
