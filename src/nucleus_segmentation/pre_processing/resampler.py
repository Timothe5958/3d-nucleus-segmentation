import numpy as np
from scipy import ndimage


class Resampler:
    """Resample the data to have isotropic voxels."""
    def __init__(self, voxel_sizes):
        self.voxel_sizes = voxel_sizes
        self.final_voxel_size = np.min(self.voxel_sizes)
        self._resampled = None

    def resample(self, data):
        """
        Returns the resampled data, using cache to avoid computing multiple times.

        Note
        ____
        We build the resampling using the smaller value amoung the voxel's dimensions,
        in order to avoid too much computation and approximation because of the interpolation.

        """
        if self._resampled is None:
            zoom_factor = self.voxel_sizes / self.final_voxel_size
            self._resampled = ndimage.zoom(
                data,
                zoom=zoom_factor,
                order=1,
                mode='reflect',
            )
        return self._resampled
