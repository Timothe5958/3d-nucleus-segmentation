import copy

import numpy as np
import skimage
from scipy import ndimage


class Cropper:
    """Crop the data by removing black background without any information."""

    def __init__(self, data):
        self.data = data
        self.denoised = None
        self.binary = None
        self._cropped = None

    def crop(self):
        """Returns the cropped data."""

        if self._cropped is None:
            # removing noise
            data_copy = copy.deepcopy(self.data)
            self.denoised = ndimage.gaussian_filter(
                data_copy,
                sigma=(3, 3, 3),
            )

            # binarisation of the image
            otsu_th = skimage.filters.threshold_otsu(self.denoised)
            self.binary = self.denoised > otsu_th

            # get the limits
            _, y_indices, x_indices = np.where(self.binary != 0)

            y_min, y_max = y_indices.min(), y_indices.max()
            x_min, x_max = x_indices.min(), x_indices.max()

            self._cropped = self.data[:, y_min:y_max, x_min:x_max]

        return self._cropped
