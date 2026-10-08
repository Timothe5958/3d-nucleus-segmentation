import numpy as np
from scipy import ndimage


def resample_isotropic(data, voxel_sizes):
    """
    Returns the resampled data, using cache to avoid computing multiple times.

    Note
    ____
    We build the resampling using the smaller value amoung the voxel's dimensions,
    in order to avoid too much computation and approximation because of the interpolation.

    """
    zoom_factor = voxel_sizes / np.min(voxel_sizes)
    return ndimage.zoom(
        data,
        zoom=zoom_factor,
        order=1,
        mode='reflect',
    )
