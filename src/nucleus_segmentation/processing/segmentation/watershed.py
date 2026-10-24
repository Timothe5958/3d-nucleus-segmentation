import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.segmentation import watershed


def split_aggregates(binary_image, min_distance=10):
    binary_image = binary_image.astype(bool)

    # distance map
    distance = ndi.distance_transform_edt(binary_image)

    # detection of peaks
    coords = peak_local_max(
        distance,
        min_distance=min_distance,
        labels=binary_image,
        exclude_border=False,
    )

    # peak's centers
    peaks = np.zeros(binary_image.shape, dtype=bool)
    peaks[tuple(coords.T)] = True
    markers, _ = ndi.label(peaks)

    # watershed
    labels = watershed(
        -distance,
        markers,
        mask=binary_image,
    )

    return labels
