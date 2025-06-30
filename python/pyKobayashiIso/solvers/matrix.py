"""
matrix.py : Builds the coefficient matrices for phase-field and heat equations
"""
from petsc4py import PETSc

def build_phase_matrix(Nx, Ny, dx, tau, dt, epsilon):
    """
    Constructs the coefficient matrix for phase-field equation. It imposes Neumann boundary 
    conditions (no-flux)

    Parameters:
        Nx (int) : Number of grid points in X
        Ny (int) : Number of grid points in Y
        dx (float) : Grid size
        tau (float) : Relaxation coefficient
        dt (float) : Time step
        epsilon (float) : Gradient energy coefficient

    Returns:
        A : Coefficient matrix for phase-field equation
    """
    A = PETSc.Mat().createAIJ([Nx*Ny, Nx*Ny])
    A.setFromOptions();
    A.setUp()

    I = lambda i, j: i * Ny + j
    beta = dt * epsilon**2 / dx**2

    for i in range(Nx):
        for j in range(Ny):
            row = I(i, j)
            diag = tau

            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:

                ni, nj = i + di, j + dj
                if 0 <= ni < Nx and 0 <= nj < Ny:
                    A.setValue(row, I(ni, nj), -beta)
                    diag += beta

            A.setValue(row, row, diag)

    A.assemble()

    return A


def build_heat_matrix(Nx, Ny, dx, dt):
    """
    Constructs the coefficient matrix for solving heat equation. It imposes Dirichlet BC at 
    left wall whereas Neumann BC at remaining walls

    Parameters:
        Nx (float): Number of grid points in X
        Ny (float): Number of grid points in Y
        dx (float): Grid size
        dt (float): Time step
    """
    A = PETSc.Mat().createAIJ([Nx*Ny, Nx*Ny])
    A.setFromOptions();
    A.setUp()

    I = lambda i, j: i * Ny + j
    beta = dt / dx**2

    for i in range(Nx):
        for j in range(Ny):
            row = I(i, j)

            if (i == 0):
                A.setValue(row, row, 1.0)
                continue

            diag = 1.0

            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:

                ni, nj = i + di, j + dj
                if 0 <= ni < Nx and 0 <= nj < Ny:
                    A.setValue(row, I(ni, nj), -beta)
                    diag += beta

            A.setValue(row, row, diag)

    A.assemble()

    return A
