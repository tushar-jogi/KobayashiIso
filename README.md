# 🌊 Isotropic Directional Solidification using the Kobayashi Phase-Field Model

**KobatashiIso** is a computational framework for simulating solid–liquid interface migration using the phase-field method. It numerically solves a coupled set of partial differential equations governing dendritic solidification in undercooled melts, as described in the seminal work by Ryo Kobayashi (Physica D, 1993).

This repository provides implementations in both **Python** and **C++**, allowing researchers and students to explore high-fidelity simulations of **directional solidification with isotropic interfacial energy**. The current version is implement in 2D

---

## 🔍 Key Features

* ✅ Solves the phase-field equation and heat conduction equation with latent heat coupling
* ✅ Supports **directional solidification with isotropic interfacial energy**
* ✅ Phase-field equation solved via **implicit-explicit (IMEX)** time integration
* ✅ Heat equation solved via **implicit backward Euler** method
* ✅ Easily extendable to **3D simulation**
* ✅ Python interface for ease of prototyping; C++ version for high performance

---

## 📦 Prerequisites

We recommend using **Miniforge** or **Miniconda** for managing environments and dependencies. If you don't have it installed, see the official [Conda documentation](https://docs.conda.io/projects/conda/en/latest/index.html).

---

## ⚙️ Environment Setup

This project includes a Conda environment file: [`env.yml`](./env.yml)

To set up the environment:

```bash
conda env create -f environment/env.yml
conda activate kobayashi
```

This will install the required packages including:

* `numpy`
* `matplotlib`
* `h5py`
* `pyyaml`
* `petsc4py`

All dependencies are sourced from **conda-forge** to ensure compatibility.

---

## 🚀 Running the Simulation

The bash script is provided to either run python or cpp version. 
To execute the `run.sh` script, make sure it executable, if not run following command on terminal:

```bash
chmod +x run.sh
```
### Python Version

The Python simulation is structured around the main driver script:

```bash
./run.sh python
```
**To run unit test**

```bash
./run.sh pythontest
```
This will run the directional solidification simulation using python code

Simulation data will be saved to the `python/data/` directory in `.h5` and `.png` formats for analysis and visualization.

### C++ Version

The C++ implementation is available in the `cpp/` directory. To compile and run the cpp version:

```bash
./run.sh cpp
```

This will create `build` folder in `cpp` and output files will be saved in `cpp/data` 

For correct executation of cpp project, petsc installation should be properly done.
The package uses *PETSc 3.21.4* version.
The installed petsc version can compiled with following command

```
./configure --force --download-vtk --with-vtk=1 --download-mpich --download-fftw --download-hdf5 --download-fblaslapack=1 --download-zlib --with-cxx-dialect=C++11 --download-hypre --with-debugging=0 --with-mpi-f90module-visibility=0 --with-hdf5=1 --with-hdf5-dir=$CONDA_PREFIX --with-hdf5-fortran-bindings=1 --with-cc=gcc --with-cxx=g++ --with-fc=gfortran -CFLAGS="-O3" -CXXFLAGS="-O3" -FFLAGS="-O3" -CUDAOPTFLAGS="-G"
```

**To run cpp test cases**

```bash
./run.sh cpptest
```
---

## 📁 Directory Structure
```
.
├── python/                          # Python implementation
│   ├── pyKobayashiIso/              # Python package/module
│   │   ├── bc/                      # Boundary condition functions (optional)
│   │   ├── io_utils/                # HDF5 and image I/O
│   │   ├── fields/                  # Field initialization and manipulation
│   │   ├── solvers/                 # Numerical solvers (phase + heat)
│   │   ├── tests/                   # Unit tests
│   │   ├── utils/                   # Helper functions
│   │   └── main.py                  # Python entry point
│   └── data/                        # Python-generated output
│
├── cpp/                             # C++ implementation
│   ├── src/                         # C++ source files
│   │   ├── main.cpp                 # C++ entry point
│   │   ├── boundary_conditions.cpp
│   │   ├── build_matrices.cpp
│   │   ├── initialize.cpp
│   │   ├── read.cpp
│   │   ├── solve.cpp
│   │   ├── utils.cpp
│   │   └── write.cpp
│   ├── include/                     # Header files
│   ├── tests/                       # Unit tests
│   └── data/                        # C++ output files (.h5, .png)
|   └── plot.py                      # python script to generate png
│
├── config/
│   └── params.yaml                  # Shared simulation parameters
│
├── results/                         # Final collected results or post-processed outputs
│
├── environment/
│   ├── env.yml                      # Conda environment for cross-language support
│   └── requirements.txt             # For Python pip users
│
├── .gitignore                       # Exclude builds, data, etc.
└── README.md                        # High-level project overview

```
---

## 🧾 Simulation Parameters

| Name              | Type    | Description                                    |
| ----------------- | ------- | ---------------------------------------------- |
| `epsilon`         | float   | Gradient energy coefficient (interface width). |
| `tau`             | float   | Phase-field relaxation time.                   |
| `K`               | float   | Dimensionless latent heat.                     |
| `alpha`           | float   | Parameter controlling the m(T) function.       |
| `gamma`           | float   | Sharpness of the tanh in m(T).                 |
| `mT`              | ndarray | Driving force for phase-field evolution.       |
| `dt`              | float   | Time step size.                                |
| `dx`, `dy`        | float   | Spatial grid resolution.                       |
| `Nx`, `Ny`, `Nz`  | float   | Number of grid points in X and Y directions.   |
| `a`               | float   | Strength of added noise.                       |
| `steps`           | int     | Number of time steps to simulate.              |
| `output_interval` | int     | Frequency (in steps) for saving outputs.       |
| `p`               | ndarray | Phase field array (0 = liquid, 1 = solid).     |
| `T`               | ndarray | Temperature field array.                       |
| `dim`             | int     | Spacial dimension (2D or 3D)                   |


---

## 🌌 Boundary Conditions Summary

Kobayashi 1993 directional solidification setup:

* **Left wall (x=0)**: `T = T_cool` (Dirichlet), `∂p/∂x = 0` (Neumann)
* **Right, Top, Bottom**: `∂T/∂n = 0` (adiabatic), `∂p/∂n = 0` (Neumann)

```text
    ^ y
    |
    |                   ∂T/∂n = 0, ∂p/∂n = 0
    |             ┌──────────────────────────────┐
    |             │                              │
    |             │                              │
    |   T=T_cool  │                              │ ∂T/∂n = 0
    |   ∂p/∂n=0   │                              │ ∂p/∂n = 0
    |             │                              │
    |             └──────────────────────────────┘
    |                    ∂T/∂n = 0, ∂p/∂n = 0
     --------------------------------------> x
```
---

## 📘 References

* R. Kobayashi, *Modeling and numerical simulations of dendritic crystal growth*, Physica D 63 (1993), 410–423.

---

