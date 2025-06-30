import h5py
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os

def plot_fields(h5file, output_dir="plots"):
    # Load fields from HDF5
    with h5py.File(h5file, "r") as f:
        p = f["p"][:]
        T = f["T"][:]

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Plot phase field
    plt.figure()
    plt.imshow(p.T, cmap="turbo", origin="lower")
    plt.colorbar(label="Phase field p")
    plt.title("Phase field")
    plt.savefig(os.path.join(output_dir, os.path.basename(h5file).replace(".h5", "_p.png")))
    plt.close()

    # Plot temperature field
    plt.figure()
    plt.imshow(T.T, cmap="coolwarm", origin="lower")
    plt.colorbar(label="Temperature T")
    plt.title("Temperature field")
    plt.savefig(os.path.join(output_dir, os.path.basename(h5file).replace(".h5", "_T.png")))
    plt.close()

    print(f"✅ Saved plots to {output_dir}/")

# Usage: python plot_fields.py ../data/step_00020.h5
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plot_fields.py <file.h5>")
    else:
        plot_fields(sys.argv[1])

