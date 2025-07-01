"""
matrix.py : Builds the coefficient matrices for phase-field and heat equations
"""
from petsc4py import PETSc

def build_phase_matrix(Nx, Ny, Nz, dx, tau, dt, epsilon, dim):
    """
    Constructs the coefficient matrix for phase-field equation. It imposes Neumann boundary 
    conditions (no-flux)

    Parameters:
        Nx (int) : Number of grid points in X
        Ny (int) : Number of grid points in Y
        Nz (int) : Number of grid points in Z
        dx (float) : Grid size
        tau (float) : Relaxation coefficient
        dt (float) : Time step
        epsilon (float) : Gradient energy coefficient
        dim (int) : spacial dimensions (2D or 3D)

    Returns:
        A : Coefficient matrix for phase-field equation
    """

    N = Nx * Ny * (Nz if dim == 3 else 1)
    A = PETSc.Mat().createAIJ([N, N], comm=PETSc.COMM_SELF)
    A.setFromOptions();
    A.setUp()

    # Unified indexing: flatten (i,j,k) to 1D
    def I(i, j, k): return i * Ny * Nz + j * Nz + k

    beta = dt * epsilon**2 / dx**2

    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz if dim == 3 else 1):
                row = I(i, j, k)
                diag = tau
                
                # 2D or 3D stencil
                stencil = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0)]
                if dim == 3:
                    stencil += [(0,0,-1), (0,0,1)]

                for di, dj, dk in stencil:
                    ni, nj, nk = i + di, j + dj, k + dk
                    if 0 <= ni < Nx and 0 <= nj < Ny and 0 <= nk < (Nz if dim == 3 else 1):
                        A.setValue(row, I(ni, nj, nk), -beta)
                        diag += beta

                A.setValue(row, row, diag)

    A.assemble()

    return A


def build_heat_matrix(Nx, Ny, Nz, dx, dt, dim):
    """
    Constructs the coefficient matrix for solving heat equation. It imposes Dirichlet BC at 
    left wall whereas Neumann BC at remaining walls

    Parameters:
        Nx (int): Number of grid points in X
        Ny (int): Number of grid points in Y
        Nz (int): Number of grid points in Z
        dx (float): Grid size
        dt (float): Time step
        dim (int) : Spacial dimension 
    """
    N = Nx * Ny * (Nz if dim == 3 else 1)
    A = PETSc.Mat().createAIJ([N, N],comm=PETSc.COMM_SELF)
    A.setFromOptions();
    A.setUp()

    def I(i, j, k): return i * Ny * Nz + j * Nz + k

    beta = dt / dx**2

    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz if dim == 3 else 1):
                row = I(i, j, k)

                if (i == 0):
                    A.setValue(row, row, 1.0)
                    continue

                diag = 1.0

                stencil = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0)]
                if dim == 3:
                    stencil += [(0,0,-1), (0,0,1)]

                for di, dj, dk in stencil:
                    ni, nj, nk = i + di, j + dj, k + dk
                    if 0 <= ni < Nx and 0 <= nj < Ny and 0 <= nk < (Nz if dim == 3 else 1):
                        A.setValue(row, I(ni, nj, nk), -beta)
                        diag += beta

                A.setValue(row, row, diag)

    A.assemble()

    return A
