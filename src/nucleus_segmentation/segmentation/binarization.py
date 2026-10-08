
from skimage import filters


def binarization_simple_otsu(data):
    threshold = filters.threshold_otsu(data[data != 0])
    return data > threshold

def binarization_double_otsu(data):
    threshold = filters.threshold_otsu(data)
    selected = data[data > threshold]

    threshold2 = filters.threshold_otsu(selected)
    return data > threshold2
