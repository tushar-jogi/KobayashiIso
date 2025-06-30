#include "boundary_conditions.hpp"

/**
 * Apply boundary conditions to phase and temperature fields.
 * - Phase field (p): Neumann (zero-gradient) on all sides.
 * - Temperature (T): Dirichlet on left wall (T = T_cool), Neumann elsewhere.
 */
void apply_boundary_conditions(std::vector<double>& p, std::vector<double>& T, int Nx, int Ny, double T_cool) {

    auto I = [&](int i, int j) { return i * Ny + j; };

    // Apply Neumann BC for phase field (copy adjacent values)
    for (int j = 0; j < Ny; ++j) {
        p[I(0, j)]     = p[I(1, j)];
        p[I(Nx - 1, j)] = p[I(Nx - 2, j)];
    }
    for (int i = 0; i < Nx; ++i) {
        p[I(i, 0)]     = p[I(i, 1)];
        p[I(i, Ny - 1)] = p[I(i, Ny - 2)];
    }

    // Apply BCs for temperature
    for (int j = 0; j < Ny; ++j) {
        T[I(0, j)] = T_cool;                  // Dirichlet on left
        T[I(Nx - 1, j)] = T[I(Nx - 2, j)];     // Neumann on right
    }
    for (int i = 0; i < Nx; ++i) {
        T[I(i, 0)]     = T[I(i, 1)];          // Neumann on bottom
        T[I(i, Ny - 1)] = T[I(i, Ny - 2)];    // Neumann on top
    }
}
