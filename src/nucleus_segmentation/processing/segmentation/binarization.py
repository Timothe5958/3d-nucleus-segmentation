
from skimage import filters


def binarization_otsu(data):
    threshold = filters.threshold_otsu(data[data != 0])
    return data > threshold

def binarization_multiotsu(data, classes=3):
    th = filters.threshold_multiotsu(data, classes=classes)
    return data > th[-1]
