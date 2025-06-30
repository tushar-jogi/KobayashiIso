# main.py
import numpy as np
import h5py
import yaml

from petsc4py import PETSc
from io_utils.read  import load_params 
from io_utils.save import write_h5 
from io_utils.visualize import write_png 
from bc.boundary_conditions import apply_boundary_conditions
from fields.initialize import initialize_fields
from solvers.phase import solve_phase_field_equation
from solvers.heat import solve_heat_equation
from utils.math_utils import m_func


def run_simulation():
    """
    Runs the simulation.

    Parameters:
        epsilon (float)       : Gradient energy coefficient (interface width).
        tau (float)           : Phase-field relaxation time.
        K (float)             : Dimensionless latent heat.
        alpha (float)         : Parameter controlling the m(T) function.
        gamma (float)         : Sharpness of the tanh in m(T).
        mT (ndarray)          : Driving force for phase-field evolution
        dt (float)            : Time step size.
        dx, dy (float)        : Spatial grid resolution.
        Nx, Ny (float)        : Number of grids in X and Y.
        a (float)             : Strength of noise
        steps (int)           : Number of time steps to simulate.
        output_interval (int) : Output frequency
        p (ndarray)           : Phase field array 
        T (ndarray)           : Temperature field array 
    """

    # Load parameters from params.yaml
    params = load_params()

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
            write_h5(p, T, step*dt)
            write_png(p, T, step*dt)
            print(f"Time {step*dt}: saved output")


    print("Simulation complete.")

if __name__ == "main__":
    run_simulation()

