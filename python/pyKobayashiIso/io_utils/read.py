#============================================================
#           Loads the input file 
#============================================================

"""
read.py - Load simulation parameters from a YAML file.
"""

import yaml
import os

def load_params():
    """
    Load simulation parameters from a YAML file.

    Parameters:
        filepath (str): Path to YAML file
        (default in the root folder: config/params.yaml)

    Returns:
        dict: Parsed configuration parameters
    """
    #path = os.getcwd() + "/config/params.yaml"
    path =  "../../config/params.yaml"
    with open(path, 'r') as f:
        return yaml.safe_load(f)
