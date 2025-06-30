#pragma once
#include <vector>

/**
 * Initialize the phase and temperature fields.
 * Sets a narrow solid strip on the left as initial condition.
 * 
 * @param p phase field (output)
 * @param T temperature field (output)
 * @param Nx number of grid points in X
 * @param Ny number of grid points in Y
 * @param Te equilibrium temperature
 */
void initialize_fields(std::vector<double>& p, std::vector<double>& T, int Nx, int Ny, double Te);

struct Parameters {
    int Nx, Ny, steps, tstep;
    double Lx, Ly, dx, dt;
    double epsilon, tau, a, gamma, alpha, K;
};

