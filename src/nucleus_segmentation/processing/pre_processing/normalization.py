from dataclasses import dataclass
from functools import cache

import numpy as np
from skimage import filters


@dataclass
class NormalizationOptions:
    sigma: int = 15
    alpha: float = 0.1
    ref_th: float | None = None


def split_in_cubes(data, cube_size=30, shift=False):
    cubes = []
    coords = []
    z_size, x_size, y_size = data.shape

    start = - cube_size // 2 if shift else 0

    for z_0 in range(start, z_size, cube_size):
        for x_0 in range(start, x_size, cube_size):
            for y_0 in range(start, y_size, cube_size):
                cube = data[
                    max(z_0, 0) : min(z_0 + cube_size, z_size),
                    max(x_0, 0) : min(x_0 + cube_size, x_size),
                    max(y_0, 0) : min(y_0 + cube_size, y_size),
                ]

                if not cube.any():
                    continue

                cubes.append(cube)
                coords.append((max(z_0, 0), max(x_0, 0), max(y_0, 0)))

    return cubes, coords

def find_reference_cube(cubes):
    average_inten_groups = []

    for group in cubes:
        layer_mean = np.mean(group[group != 0])
        average_inten_groups.append(layer_mean)

    return cubes[np.argmax(average_inten_groups)]

@cache
def cube_gaussian_weights(shape, sigma):
    z, x, y = np.indices(shape)

    return np.exp(
        -(
            (z - shape[0]/2) ** 2
            + (x - shape[1]/2) ** 2
            + (y - shape[2]/2) ** 2
        ) / (2 * sigma**2)
    ).astype(np.float32)

def from_cubes_to_normalized(data, cubes, cubes_coords, options: NormalizationOptions):
    if options.ref_th is None:
        ref_cube = find_reference_cube(cubes)
        options.ref_th = filters.threshold_otsu(ref_cube[ref_cube != 0])

    normalized_data = np.zeros(data.shape, dtype=np.float32)
    gaussian_data = np.zeros(data.shape, dtype=np.float32)

    for cube, (z0, x0, y0) in zip(cubes, cubes_coords, strict=True):
        zone = (
            slice(z0, z0 + cube.shape[0]),
            slice(x0, x0 + cube.shape[1]),
            slice(y0, y0 + cube.shape[2]),
        )

        cube_threshold = filters.threshold_otsu(cube[cube != 0])
        binary_cube = cube > cube_threshold
        cube_f = cube.astype(np.float32)

        gaussian_data[zone] = cube_gaussian_weights(cube_f.shape, options.sigma)

        if cube_threshold == 0:
            normalized_data[zone] = cube_f
            continue

        full_gain = options.ref_th / cube_threshold
        gain = 1.0 + (full_gain - 1.0) * options.alpha
        cube_f[binary_cube] *= gain

        normalized_data[zone] = np.clip(np.rint(cube_f), 0, 65535)

    return normalized_data, gaussian_data

def normalize_intensity_shift_method(data, cube_size=30, sigma=15, alpha=0.1):
    norm_options = NormalizationOptions(sigma=sigma, alpha=alpha)

    cubes, cubes_coords = split_in_cubes(data, cube_size=cube_size)
    normalized, gaussian = from_cubes_to_normalized(
        data,
        cubes,
        cubes_coords,
        norm_options,
    )

    cubes_shift, cubes_coords_shift = split_in_cubes(data, cube_size=cube_size, shift=True)
    normalized_shift, gaussian_shift = from_cubes_to_normalized(
        data,
        cubes_shift,
        cubes_coords_shift,
        norm_options,
    )

    normalized *= gaussian
    normalized_shift *= gaussian_shift
    normalized += normalized_shift
    gaussian += gaussian_shift

    np.divide(normalized, gaussian, out=normalized, where=gaussian > 0)
    return normalized

