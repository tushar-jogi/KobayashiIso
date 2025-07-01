import unittest
import numpy as np
from petsc4py import PETSc

# Adjust imports as needed based on your project structure
from solvers.matrix import build_phase_matrix, build_heat_matrix
from fields.initialize import initialize_grid_and_fields


class TestFieldInitialization(unittest.TestCase):
    def test_initialize_fields_2D(self):
        Nx, Ny, Nz = 100, 100, 1
        X, Y, Z, p, T, p_new = initialize_grid_and_fields(
            Nx=Nx, Ny=Ny, Nz=Nz,
            Lx=1.0, Ly=1.0, Lz=1.0,
            dim=2, T_liquid=0.0
        )
        self.assertEqual(X.shape, (Nx, Ny))
        self.assertEqual(Y.shape, (Nx, Ny))
        self.assertIsNone(Z)
        self.assertEqual(p.shape, (Nx, Ny))
        self.assertEqual(T.shape, (Nx, Ny))
        self.assertEqual(p_new.shape, (Nx, Ny))

        # Check seed region (5% of domain)
        solid_width = int(0.05 * Nx)
        self.assertTrue(np.allclose(p[:solid_width, :], 1.0))
        self.assertTrue(np.allclose(p[solid_width:, :], 0.0))
        self.assertTrue(np.allclose(T, 0.0))


class TestMatrixBuilders(unittest.TestCase):

    def setUp(self):
        self.Nx, self.Ny, self.Nz = 5, 5, 1
        self.dx = 1.0
        self.dt = 0.01
        self.epsilon = 1.0
        self.tau = 1.0
        self.dim = 2
        self.N = self.Nx * self.Ny  # total grid points for 2D

    def check_matrix_shape(self, A):
        rows, cols = A.getSize()
        self.assertEqual(rows, self.N)
        self.assertEqual(cols, self.N)

    def test_phase_matrix_2D(self):
        A = build_phase_matrix(self.Nx, self.Ny, self.Nz, self.dx, self.tau, self.dt, self.epsilon, self.dim)
        self.check_matrix_shape(A)

    def test_heat_matrix_2D(self):
        A = build_heat_matrix(self.Nx, self.Ny, self.Nz, self.dx, self.dt, self.dim)
        self.check_matrix_shape(A)


if __name__ == '__main__':
    unittest.main()

