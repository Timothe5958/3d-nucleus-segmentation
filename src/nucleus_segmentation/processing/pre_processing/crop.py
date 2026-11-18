import numpy as np
from skimage import filters


def crop_x(data):
    threshold = filters.threshold_otsu(data[::4, ::4, ::4])

    # projection on X, Y of the binarized data
    projection = data.max(axis=0)
    mask = projection > threshold

    # projection on X of the 1 values
    x_valid = np.flatnonzero(mask.any(axis=1))

    return data[
        :,
        x_valid[0]:x_valid[-1] + 1,
        :,
    ]


def crop_z(data):
    z_valid = np.where(np.any(data != 0, axis=(1, 2)))[0]
    return data[:z_valid[-1] + 1, :, :]
