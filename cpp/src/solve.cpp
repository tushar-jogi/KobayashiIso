#include "solvers.hpp"
#include "matrix.hpp"
#include "utils.hpp"
#include <random>
#include <iostream>

void solve_phase_field(std::vector<double>& p, const std::vector<double>& mT, int Nx, int Ny, double dx, double dt, double epsilon, double tau, double a) {

    int N = Nx * Ny;
    Mat A = build_phase_matrix(Nx, Ny, dx, tau, dt, epsilon);

    Vec b, x;
    VecCreateSeq(PETSC_COMM_SELF, N, &b);
    VecDuplicate(b, &x);

    std::vector<double> rhs(N);
    std::vector<double> noise = generate_noise(N, a);
    for (int i = 0; i < N; ++i) {

        rhs[i] = tau * p[i] + dt * p[i] * (1 - p[i]) * (p[i] - 0.5 + mT[i] + noise[i]);
        VecSetValue(b, i, rhs[i], INSERT_VALUES);

    }

    VecAssemblyBegin(b);
    VecAssemblyEnd(b);

    KSP ksp;
    KSPCreate(PETSC_COMM_SELF, &ksp);
    KSPSetOperators(ksp, A, A);
    KSPSetFromOptions(ksp);
    KSPSolve(ksp, b, x);

    KSPConvergedReason reason;

    KSPGetConvergedReason(ksp, &reason);
    if (reason <= 0) {
       std::cerr << "WARNING: PETSc phase solver did not converge.\n";
    }

    // Copy solution back into std::vector
    const double* x_array;
    VecGetArrayRead(x, &x_array);
    for (int i = 0; i < N; ++i) p[i] = x_array[i];
    VecRestoreArrayRead(x, &x_array);

    VecDestroy(&b);
    VecDestroy(&x);
    MatDestroy(&A);
    KSPDestroy(&ksp);
}

void solve_heat_equation(std::vector<double>& T, const std::vector<double>& dpdt, int Nx, int Ny, double dx, double dt, double K) {
    int N = Nx * Ny;
    Mat A = build_heat_matrix(Nx, Ny, dx, dt);
    Vec b, x;
    VecCreateSeq(PETSC_COMM_SELF, N, &b);
    VecDuplicate(b, &x);

     for (int i = 0; i < N; ++i) {
        double value = T[i] + dt * K * dpdt[i];
        VecSetValue(b, i, value, INSERT_VALUES);
    }
    VecAssemblyBegin(b);
    VecAssemblyEnd(b);

    KSP ksp;
    KSPCreate(PETSC_COMM_SELF, &ksp);
    KSPSetOperators(ksp, A, A);
    KSPSetFromOptions(ksp);
    KSPSolve(ksp, b, x);
    
    KSPConvergedReason reason;

    KSPGetConvergedReason(ksp, &reason);
    if (reason <= 0) {
       std::cerr << "WARNING: PETSc heat solver did not converge.\n";
    }

    const double* x_array;
    VecGetArrayRead(x, &x_array);
    for (int i = 0; i < N; ++i) T[i] = x_array[i];
    VecRestoreArrayRead(x, &x_array);

    VecDestroy(&b);
    VecDestroy(&x);
    MatDestroy(&A);
    KSPDestroy(&ksp);
}

/**
 * Generate thermal noise for each point in a 2D field.
 *
 * @param N        Total number of points (Nx * Ny)
 * @param a        Amplitude of the noise
 * @return         Vector of noise values in [-a/2, a/2]
 */
std::vector<double> generate_noise(int N, double a) {
    std::vector<double> noise(N);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(-0.5 * a, 0.5 * a);

    for (int i = 0; i < N; ++i)
        noise[i] = dis(gen);

    return noise;
}
