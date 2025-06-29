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


def build_phase_matrix(Nx, Ny, dx, tau, dt, epsilon):

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


def solve_phase_field_equation(p, epsilon, tau, a, mT, dx, dt, Nx, Ny):

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
    

def solve_heat_equation(T, dpdt, dt, dx, Nx, Ny, K):

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


def save_output(p, T, step):
    
    with h5py.File(f"data/output_{step:f}.h5", "w") as f:
        f.create_dataset("p", data = p) 
        f.create_dataset("T", data = T)

def visualize_fields(p, T, step):

    fig, axs = plt.subplots(1, 2, figsize = (10, 4)) 
    im0 = axs[0].imshow(p.T, cmap = 'viridis', origin = 'lower') 
    axs[0].set_title(f'Phase Field (time {step})') 
    plt.colorbar(im0, ax = axs[0]) 
    
    im1 = axs[1].imshow (T.T, cmap = 'inferno', origin = 'lower') 
    axs[1].set_title (f'Temperature Field (time {step})') 
    plt.colorbar (im1, ax = axs[1]) 

    plt.tight_layout()
    plt.savefig (f"data/visualization_{step:f}.png") 
    plt.close ()
