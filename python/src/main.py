# main.py
import numpy as np
import h5py
import yaml
from petsc4py import PETSc
from utils import initialize_fields, laplacian, m_func, solve_heat_equation, save_output, visualize_fields
from utils import solve_phase_field_equation

# Load parameters from config.yaml
with open("../config/params.yaml", "r") as f:
        params = yaml.safe_load(f)

Nx, Ny = params['Nx'], params['Ny']
Lx, Ly = params['Lx'], params['Ly']
dx, dy = Lx / Nx, Ly / Ny
dt = params['dt']
steps = params['steps']
output_interval = params['output_interval']

# Physical parameters
epsilon = params['epsilon']
tau = params['tau']
K = params['K']
a = params['a']
gamma = params['gamma']
Te = params["T_e"]
alpha = params["alpha"]

# Create grid
x = np.linspace(0, Lx, Nx, endpoint=False)
y = np.linspace(0, Ly, Ny, endpoint=False)
X, Y = np.meshgrid(x, y, indexing='ij')

# Initialize fields
p, T = initialize_fields(Nx, Ny, T_solid=Te, T_liquid=0.0)
p_new = np.zeros((Nx, Ny))
T_new = np.zeros((Nx, Ny))

# Time evolution
for step in range(steps):

    print(f"iteration no:{step}")
    mT = m_func(T, alpha, gamma)
    lap_p = laplacian(p, dx, dy)

    #Solve phase field equation 
    p_new = solve_phase_field_equation(p, epsilon, tau, a, mT, dx, dt, Nx, Ny)

    #F = p * (1 - p) * (p - 0.5 + mT)
    dpdt = (p_new - p) / dt

    T = solve_heat_equation(T, dpdt, dt, dx, Nx, Ny, K)

    if step % output_interval == 0:
        save_output(p, T, step)
        visualize_fields(p, T, step)
        print(f"Step {step}: saved output")

print("Simulation complete.")

