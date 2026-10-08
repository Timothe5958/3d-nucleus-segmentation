import numpy as np
from skimage import filters


def split_in_cubes(data, cube_size=30):
    cubes = []
    coords = []
    z_size, x_size, y_size = data.shape

    for z_0 in range(0, z_size, cube_size):
        for x_0 in range(0, x_size, cube_size):
            for y_0 in range(0, y_size, cube_size):
                cube = data[
                    z_0 : min(z_0 + cube_size, z_size),
                    x_0 : min(x_0 + cube_size, x_size),
                    y_0 : min(y_0 + cube_size, y_size),
                ]

                if not cube.any():
                    continue

                cubes.append(cube)
                coords.append((z_0, x_0, y_0))

    return cubes, coords


def merge_cubes(normalized_cubes, coords, original_shape):
    normalized_data = np.zeros(original_shape, dtype=np.float64)
    for cube, (z0, y0, x0) in zip(normalized_cubes, coords, strict=True):
        z1 = z0 + cube.shape[0]
        y1 = y0 + cube.shape[1]
        x1 = x0 + cube.shape[2]
        normalized_data[z0:z1, y0:y1, x0:x1] = cube
    return normalized_data


def find_reference_cube(cubes):
    average_inten_groups = []

    for group in cubes:
        layer_mean = np.mean(group[group != 0])
        average_inten_groups.append(layer_mean)

    # return the cube with the max average intensity
    return cubes[np.argmax(average_inten_groups)]


def normalize_intensity(data, cube_size=30, alpha=0.1, empty_cubes_th=100):
    # split the data into cubes
    cubes, cubes_coords = split_in_cubes(data, cube_size=cube_size)

    # find the one with higher mean intensity
    ref_cube = find_reference_cube(cubes)
    ref_threshold = filters.threshold_otsu(ref_cube[ref_cube != 0])

    normalized_cubes = []
    for cube in cubes:
        # find the otsu th without considering voxels of intensity 0.
        cube_threshold = filters.threshold_otsu(cube[cube != 0])
        binary_cube = cube > cube_threshold

        # create a new array for avoiding overflow, cube.dtype: uint16; cube_threshold.dtype: int64
        cube_f = cube.astype(np.float64)

        if cube_threshold == 0 or cube[cube != 0].var() < empty_cubes_th:
            normalized_cubes.append(cube_f)
            continue

        # compute the gain
        full_gain = ref_threshold / cube_threshold
        gain = 1.0 + (full_gain - 1.0) * alpha

        # multiply the intensity only of the foreground voxels
        cube_f[binary_cube] = cube_f[binary_cube] * gain

        normalized_cubes.append(cube_f)

    return merge_cubes(normalized_cubes, cubes_coords, data.shape)
