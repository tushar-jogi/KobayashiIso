# 🌊 Isotropic Directional Solidification using the Kobayashi Phase-Field Model

**KobatashiIso** is a computational framework for simulating solid–liquid interface migration using the phase-field method. It numerically solves a coupled set of partial differential equations governing dendritic solidification in undercooled melts, as described in the seminal work by Ryo Kobayashi (Physica D, 1993).

This repository provides implementations in both **Python** and **C++**, allowing researchers and students to explore high-fidelity simulations of **directional solidification with isotropic interfacial energy**.

---

## 🔍 Key Features

* ✅ Solves the phase-field equation and heat conduction equation with latent heat coupling
* ✅ Supports **directional solidification with isotropic interfacial energy**
* ✅ Phase-field equation solved via **implicit-explicit (IMEX)** time integration
* ✅ Heat equation solved via **implicit backward Euler** method
* ✅ Parallelized using **MPI** and **PETSc**
* ✅ Python interface for ease of prototyping; C++ version for high performance

---

## 📦 Prerequisites

We recommend using **Miniforge** or **Miniconda** for managing environments and dependencies. If you don't have it installed, see the official [Conda documentation](https://docs.conda.io/projects/conda/en/latest/index.html).

---

## ⚙️ Environment Setup

This project includes a Conda environment file: [`env.yml`](./env.yml)

To set up the environment:

```bash
conda env create -f env.yml
conda activate kobayashi
```

This will install the required packages including:

* `numpy`
* `matplotlib`
* `h5py`
* `pyyaml`
* `petsc4py`
* `mpi4py`

All dependencies are sourced from **conda-forge** to ensure compatibility.

---

## 🚀 Running the Simulation

### Python Version

The Python simulation is structured around the main driver script:

```bash
mpiexec -n 4 python main.py
```

This will run the directional solidification simulation in parallel using 4 MPI processes.

Simulation data will be saved to the `data/` directory in `.h5` and `.png` formats for analysis and visualization.

### C++ Version

The C++ implementation is available in the `cpp/` directory (to be documented separately). Compilation instructions will be provided in a dedicated `README_cpp.md`.

---

## 📁 Directory Structure

```
.
├── main.py                 # Python driver script
├── utils.py                # Utilities: solvers, BCs, I/O
├── config/
│   └── params.yaml         # Simulation parameters
├── data/                   # Output: .h5 and .png files
├── cpp/                    # C++ implementation (optional)
├── env.yml                 # Conda environment specification
└── README.md
```

---

## 📘 References

* R. Kobayashi, *Modeling and numerical simulations of dendritic crystal growth*, Physica D 63 (1993), 410–423.

---

## 👥 Acknowledgements

This work builds on the foundational phase-field models of solidification and is intended as a teaching and research tool for phase transformation modeling in materials science.

---

## 🔄 Parallel Execution Support

This code is MPI-enabled using `petsc4py`. To run in parallel:

```bash
mpiexec -n 4 python main.py
```

PETSc matrices and solvers will distribute work across ranks automatically.

### File Output Safety

* Only **rank 0** writes output files (`.h5`, `.png`) to avoid collision
* Rank-aware naming can be added for per-process debug output
* To write all ranks to the same file, use **parallel HDF5** (`h5py` with `driver='mpio'`)

### Safe I/O Summary

| Case                      | Strategy                           |
| ------------------------- | ---------------------------------- |
| One file, one rank        | `if rank == 0:` ✅                  |
| One file per rank         | Append `rank` to filenames ✅       |
| Collective parallel write | Use `h5py` with `driver='mpio'` 🧪 |

---

## 🌌 Boundary Conditions Summary

Kobayashi 1993 directional solidification setup:

* **Left wall (x=0)**: `T = T_cool` (Dirichlet), `∂p/∂x = 0` (Neumann)
* **Right, Top, Bottom**: `∂T/∂n = 0` (adiabatic), `∂p/∂n = 0` (Neumann)

```text
    ^ y
    |
    |           ∂T/∂n = 0          ∂p/∂n = 0
    |     ┌──────────────────────────────┐
    |     │                              │
    |     │                              │
T=T_cool  │                              │ ∂T/∂n = 0
∂p/∂n=0   │                              │ ∂p/∂n = 0
    |     │                              │
    |     └──────────────────────────────┘
          ∂T/∂n = 0          ∂p/∂n = 0
               -------------------------> x
```

---

