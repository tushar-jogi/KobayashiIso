"""
phase.py : Solves the phase field equation
"""

import numpy as np
from petsc4py import PETSc
from solvers.matrix import build_phase_matrix


def solve_phase_field_equation(p, epsilon, tau, a, mT, dx, dt, Nx, Ny):
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

    Returns:
        p : updated phase-field solution
    """
    noise = np.zeros_like(p)
    noise = a * (np.random.rand(Nx, Ny) - 0.5)

    rhs = tau * p + dt * p * (1 - p) * (p - 0.5 + mT + noise)

    rhs_vec = PETSc.Vec().createWithArray(rhs.flatten())

    A = build_phase_matrix(Nx, Ny, dx, tau, dt, epsilon)
    x = PETSc.Vec().createSeq(Nx * Ny)

    ksp = PETSc.KSP().create()
    ksp.setOperators(A)
    ksp.setFromOptions()
    ksp.solve(rhs_vec, x)

    if ksp.getConvergedReason() <= 0:
        print("WARNING: PETSc phase solver did not converge.")

    return x.getArray().reshape((Nx, Ny))
