#include <gtest/gtest.h>
#include "matrix.hpp"
#include "fields.hpp"
#include <petscsys.h>
#include <petscmat.h>
#include <vector>

// PETSc Test Fixture
class PetscTest : public ::testing::Test {
protected:
    static void SetUpTestSuite() {
        int argc = 0;
        char **argv = nullptr;
        PetscInitialize(&argc, &argv, nullptr, nullptr);
    }

    static void TearDownTestSuite() {
        PetscFinalize();
    }
};

// Utility to get matrix size
void get_matrix_size(Mat A, int& m, int& n) {
    MatGetSize(A, &m, &n);
}

class MatrixTest : public PetscTest {};

// Phase matrix shape test
TEST_F(MatrixTest, PhaseMatrix2DShape) {
    int Nx = 10, Ny = 10;
    double dx = 1.0, tau = 1.0, dt = 0.01, epsilon = 1.0;

    Mat A = build_phase_matrix(Nx, Ny, dx, tau, dt, epsilon);
    int m, n;
    get_matrix_size(A, m, n);

    EXPECT_EQ(m, Nx * Ny);
    EXPECT_EQ(n, Nx * Ny);

    MatDestroy(&A);
}

// Heat matrix shape test
TEST_F(MatrixTest, HeatMatrix2DShape) {
    int Nx = 10, Ny = 10;
    double dx = 1.0, dt = 0.01;

    Mat A = build_heat_matrix(Nx, Ny, dx, dt);
    int m, n;
    get_matrix_size(A, m, n);

    EXPECT_EQ(m, Nx * Ny);
    EXPECT_EQ(n, Nx * Ny);

    MatDestroy(&A);
}

class InitTest : public ::testing::Test {};

// Initial condition test
TEST_F(InitTest, InitialSolidSeed) {
    int Nx = 100, Ny = 100;
    std::vector<double> p, T;
    double Te = 0.0;

    initialize_fields(p, T, Nx, Ny, Te);

    int N = Nx * Ny;
    EXPECT_EQ(p.size(), N);
    EXPECT_EQ(T.size(), N);

    for (int i = 0; i < static_cast<int>(0.05 * Nx); ++i) {
        for (int j = 0; j < Ny; ++j) {
            int idx = i * Ny + j;
            EXPECT_DOUBLE_EQ(p[idx], 1.0);
        }
    }

    for (int i = 0; i < N; ++i) {
        EXPECT_DOUBLE_EQ(T[i], 0.0);
    }
}

