import numpy as np

from ..segmentation import binarization_otsu


def crop_background(data):
    """Returns the cropped data."""

    binary = binarization_otsu(data)

    # get the limits
    _, x_indices, y_indices = np.where(binary)

    y_min, y_max = y_indices.min(), y_indices.max()
    x_min, x_max = x_indices.min(), x_indices.max()

    return data[:, x_min:x_max + 1, y_min:y_max + 1]
