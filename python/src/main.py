# main.py
import numpy as np
import h5py
import yaml
from petsc4py import PETSc
from utils import laplacian, m_func, solve_heat_equation, save_output, visualize_fields

# Load parameters from config.yaml
with open("../config/params.yaml", "r") as f:
        config = yaml.safe_load(f)

Nx, Ny = config['Nx'], config['Ny']
Lx, Ly = config['Lx'], config['Ly']
dx, dy = Lx / Nx, Ly / Ny
dt = config['dt']
steps = config['steps']
output_interval = config['output_interval']

# Physical parameters
epsilon = config['epsilon']
tau = config['tau']
K = config['K']
a = config['a']
gamma = config['gamma']

# Create grid
x = np.linspace(0, Lx, Nx, endpoint=False)
y = np.linspace(0, Ly, Ny, endpoint=False)
X, Y = np.meshgrid(x, y, indexing='ij')

# Initialize fields
p = np.zeros((Nx, Ny))
T = np.ones((Nx, Ny)) * 0.0
p[0:5, :] = 1.0  # Nucleation from left

# Time evolution
for step in range(steps):
    m = m_func(T, a, gamma)
    lap_p = laplacian(p, dx, dy)
    F = p * (1 - p) * (p - 0.5 + m)
    dpdt = (epsilon**2 * lap_p + F) / tau
    p += dt * dpdt

    T = solve_heat_equation(T, dpdt, dt, dx, Nx, Ny, K)

    if step % output_interval == 0:
        save_output(p, T, step)
        visualize_fields(p, T, step)
        print(f"Step {step}: saved output")

print("Simulation complete.")

