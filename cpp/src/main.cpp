#include "boundary_conditions.hpp"
#include "fields.hpp"
#include "io_utils.hpp"
#include "solvers.hpp"
#include "matrix.hpp"
#include "utils.hpp"

#include <petscsys.h>
#include <iostream>
#include <vector>
#include <sstream>
#include <iomanip>

int main(int argc, char **argv)
{

  PetscErrorCode ierr;

  ierr = PetscInitialize(&argc, &argv, NULL, NULL);
  if (ierr){
    std::cerr << "PETSc failed to initialize\n";
    return ierr;
  }

  std::cout << "PETSc initialized successfully!\n";

  //Load parameters from params.yaml file
  Parameters params;
  read_parameters("../../config/params.yaml", params);

  int N = params.Nx * params.Ny;

  std::vector<double> p(N), T(N), mT(N), dpdt(N);
  initialize_fields(p, T, params.Nx, params.Ny, 0.0);

  // Time evolution loop
    for (int step = 0; step <= params.steps; ++step) {

        std::cout << "Step: " << step << std::endl;

        // Apply boundary conditions
        apply_boundary_conditions(p, T, params.Nx, params.Ny, 0.0);

        // Compute m(T)
        for (int i = 0; i < N; ++i) {
            mT[i] = m_function(T[i], params.alpha, params.gamma);
        }

        // Store previous p
        std::vector<double> p_old = p;

        // Solve phase field equation
        solve_phase_field(p, mT, params.Nx, params.Ny, params.dx, params.dt, params.epsilon, params.tau, params.a);

        // Compute dp/dt
        for (int i = 0; i < N; ++i) {
            dpdt[i] = 6.0*p[i]*(1.0-p[i])*(p[i] - p_old[i]) / params.dt;
        }

        // Solve heat equation
        solve_heat_equation(T, dpdt, params.Nx, params.Ny, params.dx, params.dt, params.K);

        // Save output 
        if (step % params.tstep == 0) {
            std::ostringstream stepstr;
            stepstr << "../data/step_" << std::setw(5) << std::setfill('0') << step;
            write_hdf5(stepstr.str() + ".h5", p, T, params.Nx, params.Ny);
            //write_png(stepstr.str(), p, T, params.Nx, params.Ny);
            std::cout << "Save Output : Time " << step*params.dt << std::endl;
        }
    }

    PetscFinalize();
    return 0;
}
