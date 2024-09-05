"""helper function to generate random vectors"""

import numpy as np


def generate_vector(dim: int = 10) -> np.ndarray:
    return np.random.rand(dim)
