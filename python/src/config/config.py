#============================================================
#           Loads the input file 
#============================================================

"""
config.py - Load simulation parameters from a YAML file.
"""

import yaml
import os

def load_config():
"""
    Load simulation parameters from a YAML file.

    Parameters:
        filepath (str): Path to YAML file

    Returns:
        dict: Parsed configuration parameters
"""
    path = os.getcwd() + "config/params.yaml"
    with open(path, 'r') as f:
        return yaml.safe_load(f)
