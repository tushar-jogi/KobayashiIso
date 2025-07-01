#include "io_utils.hpp"
#include <cmath>
#include <H5Cpp.h>

using namespace H5;

void write_hdf5(const std::string& filename, const std::vector<double>& p, const std::vector<double>& T, int Nx, int Ny) {
    H5File file(filename, H5F_ACC_TRUNC);
    hsize_t dims[2] = {static_cast<hsize_t>(Nx), static_cast<hsize_t>(Ny)};
    DataSpace dataspace(2, dims);
    DataSet pset = file.createDataSet("p", PredType::NATIVE_DOUBLE, dataspace);
    DataSet Tset = file.createDataSet("T", PredType::NATIVE_DOUBLE, dataspace);
    pset.write(p.data(), PredType::NATIVE_DOUBLE);
    Tset.write(T.data(), PredType::NATIVE_DOUBLE);
}

