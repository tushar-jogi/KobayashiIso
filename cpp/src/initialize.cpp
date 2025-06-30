#include "fields.hpp"

/*
 * Initialize phase field and temperature field.
 * The left portion of the domain is initialized as solid (p = 1), rest is liquid (p = 0).
 * The temperature is initially uniform.
 */

void initialize_fields(std::vector<double>& p, std::vector<double>& T, int Nx, int Ny, double Te) {

    p.resize(Nx * Ny, 0.0);
    T.resize(Nx * Ny, 0.0);  // Supercooled liquid everywhere initially

    int solid_width = static_cast<int>(0.05 * Nx);  // 5% of domain as solid

    for (int i = 0; i < Nx; ++i) {
        for (int j = 0; j < Ny; ++j) {
            int idx = i * Ny + j;
            if (i < solid_width) {
                p[idx] = 1.0;   // Solid
                //T[idx] = Te;    // Equilibrium temperature in the solid seed
            }
        }
    }
}

