import numpy as np
from skimage import filters, morphology


def fast_binarization(image):
    """
    Return a basic binary image form the grey-level input image.

    Parameters
    ----------
    image : numpy.array (float)
        3D Image to process

    Returns
    -------
    binary_data : numpy.array (binary)
        Treated image, binary image of the input data.

    """
    kernel = morphology.ball(2)

    opened_membranes = morphology.opening(image, kernel)

    opened_membranes = filters.gaussian(opened_membranes, sigma=1)
    threshold = filters.threshold_otsu(opened_membranes)

    binary_img = opened_membranes > threshold

    binary_membranes = np.zeros(np.shape(image), dtype=int)
    binary_membranes[binary_img] = 1

    return binary_membranes
