"""
save.py : Writes the .h5 data 
"""
import h5py
import os

def write_h5(p, T, step):
    """
    Write the h5 data files  

    Parameters:
        p (ndarray) : phase field
        T (ndarray) : Temperature field
        step (float): Elapsed simulation time
    Returns:
        No return
    """
    output_dir = "python/data"
    os.makedirs(output_dir, exist_ok=True)
    with h5py.File(f"{output_dir}/output_{step:.1f}.h5", "w") as f:
        f.create_dataset("p", data = p) 
        f.create_dataset("T", data = T)

