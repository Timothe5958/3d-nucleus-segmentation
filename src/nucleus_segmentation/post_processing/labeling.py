import numpy as np
import scipy.ndimage as ndi


def get_labelled_cells(data):
    return ndi.label(
        data,
        structure=np.ones((3, 3, 3)),
    )[0]
