#pragma once
#include <vector>
#include <petscksp.h>

/**
 * Solve the heat diffusion equation with a source term from latent heat.
 * 
 * @param T temperature field (in/out)
 * @param dpdt time derivative of phase field
 * @param Nx number of grid points in X
 * @param Ny number of grid points in Y
 * @param dx spatial step size
 * @param dt time step size
 * @param K latent heat coefficient
 */
void solve_heat_equation(std::vector<double>& T, const std::vector<double>& dpdt, int Nx, int Ny, double dx, double dt, double K);

/**
 * Solve the phase field evolution equation using PETSc.
 * 
 * @param p phase field (in/out)
 * @param mT driving force field from temperature
 * @param Nx number of grid points in X
 * @param Ny number of grid points in Y
 * @param dx spatial step size
 * @param dt time step size
 * @param epsilon gradient energy coefficient
 * @param tau time scaling coefficient
 * @param a noise amplitude
 */
void solve_phase_field(std::vector<double>& p, const std::vector<double>& mT, int Nx, int Ny, double dx, double dt, double epsilon, double tau, double a);
