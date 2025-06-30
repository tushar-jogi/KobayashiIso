#pragma once
#include <vector>

/**
 * Apply boundary conditions for phase and temperature fields.
 * Dirichlet on left wall and Neumann elsewhere for temperature.
 * Neumann for phase field on all boundaries.
 * 
 * @param p phase field (in/out)
 * @param T temperature field (in/out)
 * @param Nx number of grid points in X
 * @param Ny number of grid points in Y
 * @param T_cool cooling temperature on left boundary
 */
void apply_boundary_conditions(std::vector<double>& p, std::vector<double>& T, int Nx, int Ny, double T_cool);

