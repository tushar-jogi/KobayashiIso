#include "utils.hpp"
#include <cmath>

double m_function(double T, double alpha, double gamma) {
    return (alpha / M_PI) * atan(gamma * (1.0 - T));
}

// Copy from std::vector → PETSc Vec
void copy_to_vec(const std::vector<double>& src, Vec vec) {

    for (PetscInt i = 0; i < src.size(); ++i)
        VecSetValue(vec, i, src[i], INSERT_VALUES);

    VecAssemblyBegin(vec);
    VecAssemblyEnd(vec);
}

// Copy from PETSc Vec → std::vector
void copy_from_vec(Vec vec, std::vector<double>& dest) {

    const double* array;
    PetscInt size;
    VecGetSize(vec, &size);
    dest.resize(size);

    VecGetArrayRead(vec, &array);
    for (PetscInt i = 0; i < size; ++i)
        dest[i] = array[i];
    VecRestoreArrayRead(vec, &array);
}
