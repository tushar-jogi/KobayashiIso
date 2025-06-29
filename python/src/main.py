# main.py
import numpy as np
import h5py
import yaml
from petsc4py import PETSc
from utils import initialize_fields, m_func, solve_heat_equation, save_output, visualize_fields
from utils import solve_phase_field_equation
from utils import apply_boundary_conditions

# Load parameters from config.yaml
with open("config/params.yaml", "r") as f:
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
alpha = params["alpha"]
gamma = params['gamma']

# Create grid
x = np.linspace(0, Lx, Nx, endpoint=False)
y = np.linspace(0, Ly, Ny, endpoint=False)
X, Y = np.meshgrid(x, y, indexing='ij')

# Initialize fields
p, T = initialize_fields(Nx, Ny, T_liquid=0.0)
p_new = np.zeros((Nx, Ny))

# Time evolution
for step in range(steps):

    print(f"iteration no:{step}")

    #Applying boundary conditions on p and T
    apply_boundary_conditions(p, T, T_cool=0.0)

    mT = m_func(T, alpha, gamma)

    #Solve phase field equation 
    p_new = solve_phase_field_equation(p, epsilon, tau, a, mT, dx, dt, Nx, Ny)


    # Compute dp/dt using second-order accurate scheme
    dpdt = 6.0 * p * (1.0 - p) * (p_new - p) / dt  # fallback for first step

    # Solve heat equation
    T = solve_heat_equation(T, dpdt, dt, dx, Nx, Ny, K)

    # Update phase field 
    p = p_new

    # write output 
    if step % output_interval == 0:
        save_output(p, T, step*dt)
        visualize_fields(p, T, step*dt)
        print(f"Time {step*dt}: saved output")

print("Simulation complete.")

