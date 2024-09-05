"""display vectors"""

import numpy as np

from .generate_vectors import generate_vector


def decode() -> np.ndarray:
    return 2 * generate_vector(dim=10)
