import numpy as np
from scipy import ndimage


def get_labelled_cells(data):
    return ndimage.label(
        data,
        structure=np.ones((3, 3, 3)),
    )[0]
