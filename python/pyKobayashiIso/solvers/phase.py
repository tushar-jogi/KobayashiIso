"""
phase.py : Solves the phase field equation
"""

import numpy as np
from petsc4py import PETSc
from solvers.matrix import build_phase_matrix


def solve_phase_field_equation(p, epsilon, tau, a, mT, dx, dt, Nx, Ny, Nz=1, dim=2):
    """
    Builds the coefficient matrix and solves the phase-field equation IMEX scheme

    Parameters:
        p (ndarray) : phase-field
        epsilon (float) : gradient energy coefficient
        tau (float) : relaxation coefficient
        a (float) : strength of thermal noise
        mT (ndarray) : Driving force
        dx (float) : grid size
        dt (float) : time step
        Nx (int) : Number of grid points in X
        Ny (int) : Number of grid points in Y
        NZ (int) : Number of grid points in Z
        dim (int) : Spacial dimension

    Returns:
        p : updated phase-field solution
    """
    shape = (Nx, Ny) if dim == 2 else (Nx, Ny, Nz)
    N = Nx * Ny * (Nz if dim == 3 else 1)
    noise = a * (np.random.rand(*shape) - 0.5)

    rhs = tau * p + dt * p * (1 - p) * (p - 0.5 + mT + noise)

    rhs_vec = PETSc.Vec().createWithArray(rhs.flatten(), comm=PETSc.COMM_SELF)

    A = build_phase_matrix(Nx, Ny, Nz, dx, tau, dt, epsilon, dim)
    x = PETSc.Vec().createSeq(N, comm=PETSc.COMM_SELF)

    ksp = PETSc.KSP().create()
    ksp.setOperators(A)
    ksp.setFromOptions()
    ksp.solve(rhs_vec, x)

    if ksp.getConvergedReason() <= 0:
        print("WARNING: PETSc phase solver did not converge.")

    return x.getArray().reshape(shape)
