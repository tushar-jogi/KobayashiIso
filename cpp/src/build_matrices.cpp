#include "matrix.hpp"
#include <vector>

Mat build_phase_matrix(int Nx, int Ny, double dx, double tau, double dt, double epsilon) {

    int N = Nx * Ny;

    Mat A;
    MatCreateSeqAIJ(PETSC_COMM_SELF, N, N, 5, NULL, &A);

    double beta = dt * epsilon * epsilon / (dx * dx);
    auto I = [&](int i, int j) { return i * Ny + j; };

    for (int i = 0; i < Nx; ++i) {
        for (int j = 0; j < Ny; ++j) {

            int row = I(i, j);
            double diag = tau;

            for (auto [di, dj] : std::vector<std::pair<int, int>>{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}) {
                int ni = i + di;
                int nj = j + dj;
                if (ni >= 0 && ni < Nx && nj >= 0 && nj < Ny) {
                    MatSetValue(A, row, I(ni, nj), -beta, INSERT_VALUES);
                    diag += beta;
                }
            }

            MatSetValue(A, row, row, diag, INSERT_VALUES);
        }
    }
    MatAssemblyBegin(A, MAT_FINAL_ASSEMBLY);
    MatAssemblyEnd(A, MAT_FINAL_ASSEMBLY);
    return A;
}

Mat build_heat_matrix(int Nx, int Ny, double dx, double dt) {

    int N = Nx * Ny;
    Mat A;

    MatCreateSeqAIJ(PETSC_COMM_SELF, N, N, 5, NULL, &A);

    double beta = dt / (dx * dx);
    auto I = [&](int i, int j) { return i * Ny + j; };

    for (int i = 0; i < Nx; ++i) {
        for (int j = 0; j < Ny; ++j) {

            int row = I(i, j);

            if ( i == 0) {
              MatSetValue(A, row, row, 1.0, INSERT_VALUES);
              continue;
            }

            double diag = 1.0;

            for (int d = -1; d <= 1; d += 2) {

                if (i + d >= 0 && i + d < Nx) {
                    MatSetValue(A, row, I(i + d, j), -beta, INSERT_VALUES);
                    diag += beta;
                }

                if (j + d >= 0 && j + d < Ny) {
                    MatSetValue(A, row, I(i, j + d), -beta, INSERT_VALUES);
                    diag += beta;
                }
            }
            MatSetValue(A, row, row, diag, INSERT_VALUES);
        }
    }
    MatAssemblyBegin(A, MAT_FINAL_ASSEMBLY);
    MatAssemblyEnd(A, MAT_FINAL_ASSEMBLY);
    return A;
}

