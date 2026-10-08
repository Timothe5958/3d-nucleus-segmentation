from scipy import ndimage


def gaussian_denoise(data, ksize=1):
    return ndimage.gaussian_filter(
        data,
        sigma=(ksize, ksize, ksize),
    )

def median_denoise(data):
    return ndimage.median_filter(
        data,
        sigma=(1, 1, 1),
    )

