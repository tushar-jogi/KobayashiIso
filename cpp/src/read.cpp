#include <io_utils.hpp>
#include <yaml-cpp/yaml.h>


void read_parameters(const std::string& filename, Parameters& params) {
    YAML::Node config = YAML::LoadFile(filename);
    params.Nx = config["Nx"].as<int>();
    params.Ny = config["Ny"].as<int>();
    params.Lx = config["Lx"].as<double>();
    params.Ly = config["Ly"].as<double>();
    params.dx = params.Lx / params.Nx;
    params.dt = config["dt"].as<double>();
    params.steps = config["steps"].as<int>();
    params.epsilon = config["epsilon"].as<double>();
    params.tau = config["tau"].as<double>();
    params.a = config["a"].as<double>();
    params.gamma = config["gamma"].as<double>();
    params.alpha = config["alpha"].as<double>();
    params.K = config["K"].as<double>();
    params.tstep = config["output_interval"].as<int>();
}
