#include "io_utils.hpp"
#include <cmath>
#include <H5Cpp.h>
#include <opencv2/opencv.hpp>

using namespace H5;
using namespace cv;

void write_hdf5(const std::string& filename, const std::vector<double>& p, const std::vector<double>& T, int Nx, int Ny) {
    H5File file(filename, H5F_ACC_TRUNC);
    hsize_t dims[2] = {static_cast<hsize_t>(Nx), static_cast<hsize_t>(Ny)};
    DataSpace dataspace(2, dims);
    DataSet pset = file.createDataSet("p", PredType::NATIVE_DOUBLE, dataspace);
    DataSet Tset = file.createDataSet("T", PredType::NATIVE_DOUBLE, dataspace);
    pset.write(p.data(), PredType::NATIVE_DOUBLE);
    Tset.write(T.data(), PredType::NATIVE_DOUBLE);
}

void write_png(const std::string& filename, const std::vector<double>& p, const std::vector<double>& T, int Nx, int Ny) {

    Mat imgP(Ny, Nx, CV_64F, const_cast<double*>(p.data()));
    Mat imgT(Ny, Nx, CV_64F, const_cast<double*>(T.data()));

       for (int i = 0; i < Nx; ++i)
        for (int j = 0; j < Ny; ++j) {
            imgP.at<double>(j, i) = p[i * Ny + j];  // transpose
            imgT.at<double>(j, i) = T[i * Ny + j];
        }

    normalize(imgP, imgP, 0, 255, NORM_MINMAX);
    normalize(imgT, imgT, 0, 255, NORM_MINMAX);
    imgP.convertTo(imgP, CV_8U);
    imgT.convertTo(imgT, CV_8U);

    Mat colorP, colorT;
    applyColorMap(imgP, colorP, COLORMAP_TURBO);
    applyColorMap(imgT, colorT, COLORMAP_TURBO);

    imwrite(filename + "_p.png", imgP);
    imwrite(filename + "_T.png", imgT);
}
