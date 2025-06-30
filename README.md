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

This will run the directional solidification simulation using python code

Simulation data will be saved to the `python/data/` directory in `.h5` and `.png` formats for analysis and visualization.

### C++ Version

The C++ implementation is available in the `cpp/` directory. To compile and run the cpp version:

```bash
./run.sh cpp
```

This will create `bin` folder in `cpp` and output files will be saved in `cpp/data` 

---

## 📁 Directory Structure
```
.
├── python/                # Python implementation
│   ├── src/               # Core simulation code
│   │   ├── main.py        # Python driver script
│   │   └── utils.py       # Utilities: solvers, BCs, I/O
│   ├── data/              # Output data: .h5 and .png files
│   ├── tests/             # Unit tests
│   └── README.md          # Python-specific documentation
├── cpp/                   # C++ implementation
    ├── src/               # Source directory 
│   │   ├── main.cpp       # CPP main script
│   │   └── utils.cpp      # Utilities: solvers, BCs, I/O
│   ├── data/              # Output data: .h5 and .png files
|   ├── include/           # Header files 
│   ├── tests/             # Unit tests
│   └── README.md          # CPP-specific documentation
├── config/
│   └── params.yaml        # Simulation parameters
├── results/               # Aggregated simulation results and plots
├── environment/
│   ├──env.yml             # Conda environment specification
    └── requirements.txt   # pip-based dependency list
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
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
| `Nx`, `Ny`        | float   | Number of grid points in X and Y directions.   |
| `a`               | float   | Strength of added noise.                       |
| `steps`           | int     | Number of time steps to simulate.              |
| `output_interval` | int     | Frequency (in steps) for saving outputs.       |
| `p`               | ndarray | Phase field array (0 = liquid, 1 = solid).     |
| `T`               | ndarray | Temperature field array.                       |


---

## 📘 References

* R. Kobayashi, *Modeling and numerical simulations of dendritic crystal growth*, Physica D 63 (1993), 410–423.

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

