import copy

from scipy import ndimage


class Denoiser:
    """Denoise the data by the choosen method (each sub-class use a specific method)."""
    def __init__(self, data):
        self.data = data

    def denoise(self):
        raise NotImplementedError


class DenoiserGaussian(Denoiser):
    """Returns the denoised data using a gaussian filter."""
    def denoise(self):
        data_copy = copy.deepcopy(self.data)
        return ndimage.gaussian_filter(
            data_copy,
            sigma=(1, 1, 1),
        )


class DenoiserMedian(Denoiser):
    """Returns the denoised data using a median filter."""
    def denoise(self):
        data_copy = copy.deepcopy(self.data)
        return ndimage.median_filter(
            data_copy,
            sigma=(2, 2, 2),
        )
