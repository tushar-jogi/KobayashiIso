#pragma once
#include <vector>
#include <petscksp.h>

/**
 * Compute the driving force m(T) from temperature.
 * 
 * @param T temperature value
 * @param alpha prefactor
 * @param gamma slope parameter
 * @return value of m(T)
 */

double m_function(double T, double alpha, double gamma);

void copy_to_vec(const std::vector<double>& src, Vec vec);
void copy_from_vec(Vec vec, std::vector<double>& dest);
std::vector<double> generate_noise(int N, double a);
