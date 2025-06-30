#pragma once

#include <petscksp.h>

/**
 * Construct the matrix for the phase field solver.
 *
 * @param Nx number of grid points in X
 * @param Ny number of grid points in Y
 * @param dx spatial step size
 * @param tau relaxation parameter
 * @param dt time step size
 * @param epsilon gradient energy coefficient
 * @return PETSc matrix
 */
Mat build_phase_matrix(int Nx, int Ny, double dx, double tau, double dt, double epsilon);

/**
 * Construct the matrix for the heat equation solver.
 *
 * @param Nx number of grid points in X
 * @param Ny number of grid points in Y
 * @param dx spatial step size
 * @param dt time step size
 * @return PETSc matrix
 */
Mat build_heat_matrix(int Nx, int Ny, double dx, double dt);
