# Isotropic Directional Solidification using Kobayashi Model

`KobatashiIso` solves the coupled equations to model migration of solid/liquid interface. 
The package solves phase-field equation and heat equation with latent heat term. Only isotropic 
interfacial energy is assumed which will simulate isotropic directional growth.

The phase-field equation is solved using implicit-explicit scheme, whereas heat equation is solved 
using backward Euler scheme.

The repository contains python as well as C++ project.

### Prerequisites

To install these package miniforge/miniconda package management tool is required. 
Miniforge/Miniconda can be installed using documentation on following [link](https://docs.conda.io/projects/conda/en/latest/index.html#).

The codes will work best under the environment provided with file `env.yml`.

To load the environment

`$ conda env create -f env.yml`

`$ conda activate kobayashi`



