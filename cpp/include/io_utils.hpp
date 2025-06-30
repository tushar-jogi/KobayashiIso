#pragma once

#include <vector>
#include <string>
#include "fields.hpp"

/*
 * Read simulation parameters from a YAML configuration file.
 * 
 * @param filename path to YAML file
 * @param params struct to populate with values
 */
void read_parameters(const std::string& filename, Parameters& params);

/*
 * Save phase and temperature fields to an HDF5 file.
 *
 * @param filename path to the output .h5 file
 * @param p phase field array
 * @param T temperature field array
 * @param Nx number of grid points in X
 * @param Ny number of grid points in Y
 */
void write_hdf5(const std::string& filename, const std::vector<double>& p, const std::vector<double>& T, int Nx, int Ny);

/*
 * Save a PNG image of the phase and temperature fields.
 *
 * @param filename path to the output .png file
 * @param p phase field array
 * @param T temperature field array
 * @param Nx number of grid points in X
 * @param Ny number of grid points in Y
 */
void write_png(const std::string& filename, const std::vector<double>& p, const std::vector<double>& T, int Nx, int Ny);
