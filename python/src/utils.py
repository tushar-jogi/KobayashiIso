#utils.py
import numpy as np
import h5py 
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from petsc4py import PETSc 

def initialize_fields(Nx, Ny, T_solid=1.0, T_liquid=0.0):

    p = np.zeros((Nx, Ny))
    T = np.full((Nx, Ny), T_liquid)

    # Nucleation seed
    solid_width = int(0.05*Nx)
    p[:, :solid_width] = 1.0
    #T[Nx//10:Nx//10+5, Ny//2-2:Ny//2+3] = T_solid

    return p, T


def build_phase_matrix(Nx, Ny, dx, tau, dt, epsilon):

    A = PETSc.Mat().createAIJ([Nx*Ny, Nx*Ny])
    A.setFromOptions();
    A.setUp()

    I = lambda i, j: i * Ny + j
    alpha = tau 
    beta = dt * epsilon**2 / dx**2

    for i in range(Nx):
        for j in range(Ny):
            row = I(i, j)
            A.setValue(row, row, alpha + 4*beta)
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni , nj = (i + di) % Nx, (j + dj) % Ny
                A.setValue(row, I(ni, nj), -beta)

    A.assemble()

    return A

def laplacian(f, dx, dy):
    return (np.roll (f, 1, axis=0) + np.roll (f, -1, axis=0) - 2 * f) / dx**2 + \
           (np.roll (f, 1, axis=1) + np.roll (f, -1, axis=1) - 2 * f) / dy**2 

def m_func(T, alpha, gamma):
    return (alpha / np.pi) * np.arctan(gamma * (1.0 - T))

def solve_phase_field_equation(p, epsilon, tau, a, mT, dx, dt, Nx, Ny):

    noise = a * (np.random.rand(*p.shape) - 0.5)

    rhs = tau * p + dt * p * (1 - p)*(p - 0.5 + mT + noise)
    rhs_vec = PETSc.Vec().createWithArray(rhs.flatten())

    A = build_phase_matrix(Nx, Ny, dx, tau, dt, epsilon)
    x = PETSc.Vec().createSeq(Nx * Ny)

    ksp = PETSc.KSP().create()
    ksp.setOperators(A)
    ksp.setFromOptions()
    ksp.solve(rhs_vec, x)

    return x.getArray().reshape((Nx, Ny))


def solve_heat_equation(T, dpdt, dt, dx, Nx, Ny, K):

    A = PETSc.Mat().createAIJ([Nx *Ny, Nx *Ny]) 
    A.setFromOptions();
    A.setUp()
    I = lambda i, j: i * Ny + j 

    for i in range(Nx):
        for j in range(Ny):

            row = I(i, j) 
            A.setValue(row, row, 1 + 4*dt / dx**2) 

            for di, dj in[(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = (i + di) % Nx, (j + dj) % Ny 
                A.setValue(row, I(ni, nj), -dt / dx**2)

    A.assemble()

    b = T.flatten() + dt *K *dpdt.flatten()
    b_vec = PETSc.Vec().createWithArray(b) 
    x_vec = PETSc.Vec().createSeq(Nx *Ny) 

    ksp = PETSc.KSP().create();
    ksp.setOperators (A);
    ksp.solve(b_vec, x_vec) 

    return x_vec.getArray().reshape ((Nx, Ny))
     
def save_output(p, T, step):

  with h5py.File(f"../data/output_{step:05d}.h5", "w") as f:
      f.create_dataset("p", data = p) 
      f.create_dataset("T", data = T)

def visualize_fields(p, T, step):

    fig, axs = plt.subplots(1, 2, figsize = (10, 4)) 
    im0 = axs[0].imshow(p, cmap = 'viridis', origin = 'lower') 
    axs[0].set_title(f'Phase Field (step {step})') 
    plt.colorbar(im0, ax = axs[0]) 
    
    im1 = axs[1].imshow (T, cmap = 'inferno', origin = 'lower') 
    axs[1].set_title (f'Temperature Field (step {step})') 
    plt.colorbar (im1, ax = axs[1]) 

    plt.tight_layout()
    plt.savefig (f"../data/visualization_{step:05d}.png") 
    plt.close ()
