"""
math_utils : utility function to calculate the driving force for phase field evolution
"""

import numpy as np

def m_func(T, alpha, gamma):
    """
    Calculate the driving force in terms of temperature

    Parameters:
        T (ndarray): local temperature
        alpha (float) : Strength of driving force
        gamma (float) : Thermal sensitivity
    Returns:
        (ndarray) : Driving force solidification
    """
    return (alpha / np.pi) * np.arctan(gamma * (1.0 - T))

