import numpy as np
from skimage import filters


def crop_background(data):
    threshold = filters.threshold_otsu(data[::4, ::4, ::4])

    # projection on X, Y of the binarized data
    projection = data.max(axis=0)
    mask = projection > threshold

    # projection on Z
    projection_z = data.max(axis=(1, 2))
    z_valid = np.flatnonzero(projection_z > threshold)

    # projection on X and on Y of the values 1
    x_valid = np.flatnonzero(mask.any(axis=1))
    y_valid = np.flatnonzero(mask.any(axis=0))

    return data[
        z_valid[0]:z_valid[-1] + 1,
        x_valid[0]:x_valid[-1] + 1,
        y_valid[0]:y_valid[-1] + 1,
    ]
