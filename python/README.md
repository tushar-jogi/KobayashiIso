# Phase-Field Simulation for Dendritic Growth

This project implements a 2D phase-field model for simulating dendritic crystal growth during directional solidification, based on the model introduced by R. Kobayashi (1993). The simulation solves the coupled phase-field and heat diffusion equations using PETSc, NumPy, and HDF5.

---

## 📦 Folder Structure

```
python/
├── config/                      
│   └── params.yaml              # Simulation parameters
├── data/                        
│   ├── output_00000.h5          # Output HDF5 snapshots (generated during run)
│   └── visualization_00000.png  # Visualization snapshots (generated during run)
├── tests/                       
│   └── test_utils.py            # Unit tests   
├── src/                    
│   ├── main.py                  # Main simulation driver 
│   └── utils.py                 # Utility functions (Laplacisn, solver, I/O, visualization)
├── README.md
├── requirements.txt             # (optional) Python dependencies
└── .gitignore              
```

---

## ⚙️ Configuration (`config.yaml`)
You can configure the simulation grid, time step, material constants, and output frequency in `config.yaml`:

```yaml
Nx: 100
Ny: 100
Lx: 1.0
Ly: 1.0
dt: 0.0001
steps: 5000
output_interval: 1000
epsilon: 0.01
tau: 0.0003
K: 1.0
a: 0.9
gamma: 10.0
```

---

## 🚀 How to Run

1. Install the required packages:
```bash
pip install numpy matplotlib h5py petsc4py pyyaml
```

2. Run the simulation:
```bash
python main.py
```

3. Outputs:
   - `output_XXXXX.h5` files contain the phase (`p`) and temperature (`T`) fields.
      - `visualization_XXXXX.png` files visualize the current state of the fields.

      ---

## 📊 Visualization
Each saved step generates a PNG image comparing the phase and temperature fields. You can view them in any image viewer or compile them into a video using `ffmpeg`.

---

## 🧪 Testing
To add tests, create a `tests/` folder and write `pytest` or `unittest` based scripts for:
- `laplacian()`
- `m_func()`
- `solve_heat_equation()`

---

## 📚 References
- R. Kobayashi, *Modeling and numerical simulations of dendritic crystal growth*, Physica D 63, 410–423 (1993).

---

## 📝 License
This project is licensed under the MIT License.

---

## ✉️ Contact
For questions, reach out to Tushar Jogi ([tushar.jogi@gmail.com](mailto:tushar.jogi@gmail.com)).

```
```
```
```
```
```
```
```
