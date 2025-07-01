"""
visualize.py : Generates png files for p and T using matplotlib
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def write_png(p, T, step, dim=2):

    """
    Generates png files for phase-field and Temperature field

    Parameters:
        p (ndarray)  : phase-field
        T (ndarray)  : Temperature field
        step (float) : Elaspsed simulation time

    Returns:
        No return
    """
    if dim == 2:
        fig, axs = plt.subplots(1, 2, figsize = (10, 4)) 
        im0 = axs[0].imshow(p.T, cmap = 'viridis', origin = 'lower') 
        axs[0].set_title(f'Phase Field (time {step:.1f})') 
        plt.colorbar(im0, ax = axs[0]) 

        im1 = axs[1].imshow (T.T, cmap = 'inferno', origin = 'lower') 
        axs[1].set_title (f'Temperature Field (time {step:.1f})') 
        plt.colorbar (im1, ax = axs[1]) 

        plt.tight_layout()
        plt.savefig (f"../data/visualization_{step:f}.png") 
        plt.close ()

    elif dim == 3:
        print("Write a script to generate vtk files from h5 files")
