"""
heat.py : Solves the heat equation
"""
import numpy as np
from petsc4py import PETSc
from solvers.matrix import build_heat_matrix

def solve_heat_equation(T, dpdt, dt, dx, Nx, Ny, K, Nz=1, dim=2):
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


    shape = (Nx, Ny) if dim == 2 else (Nx, Ny, Nz)
    N = Nx * Ny * (Nz if dim == 3 else 1)

    A = build_heat_matrix(Nx, Ny, Nz, dx, dt, dim)

    b_array = T + dt * K * dpdt

    # Apply Dirichlet BC on left wall (i=0)
    def I(i, j, k=0): return i * Ny * Nz + j * Nz + k

    b_flat = b_array.flatten()
    if dim == 2:
        for j in range(Ny):
            b_flat[I(0, j)] = 0.0
    elif dim == 3:
        for j in range(Ny):
            for k in range(Nz):
                b_flat[I(0, j, k)] = 0.0

    b_vec = PETSc.Vec().createWithArray(b_flat, comm=PETSc.COMM_SELF)
    x_vec = PETSc.Vec().createSeq(N, comm=PETSc.COMM_SELF)

    ksp = PETSc.KSP().create(comm=PETSc.COMM_SELF)
    ksp.setOperators(A)
    ksp.setFromOptions()
    ksp.solve(b_vec, x_vec)

    if ksp.getConvergedReason() <= 0:
        print("WARNING: PETSc heat solver did not converge.")

    return x_vec.getArray().reshape(shape)
