import numpy as np
from skimage import filters


def remove_background_otsu(data):
    th = filters.threshold_otsu(data[data != 0])
    binary = data > th
    return np.where(binary, data, 0)
