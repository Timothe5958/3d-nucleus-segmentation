import numpy as np
from scipy import ndimage
from skimage import morphology, segmentation

from ..segmentation import binarization_otsu


def build_scaffold_mask(data, log=False):
    if log:
        print('Building base of scaffold mask...')

    binary_data = binarization_otsu(data)

    scaffold_mask = np.zeros_like(binary_data, dtype=bool)
    for x in range(binary_data.shape[1]):
        slice_x = binary_data[:, x, :]
        if np.any(slice_x):
            scaffold_mask[:, x, :] = morphology.convex_hull_image(slice_x)

    # fill holes and closing
    scaffold_mask = ndimage.binary_fill_holes(scaffold_mask)
    return morphology.closing(scaffold_mask, morphology.ball(2))


def extract_scaffold_edges(scaffold_mask, log=False):
    if log:
        print('Extracting scaffold edge...')

    scaffold = segmentation.find_boundaries(scaffold_mask, mode='outer')
    scaffold_projected = np.any(scaffold, axis=2, keepdims=True)
    scaffold_projected_3d = np.repeat(scaffold_projected, scaffold.shape[2], axis=2)

    scaffold_sides = np.zeros_like(scaffold_projected_3d, dtype=bool)

    for z in range(scaffold_sides.shape[0]):
        slice_xy = scaffold_projected_3d[z,:,:]

        x_left = None # now didn't find any pixel from left
        for x in range (slice_xy.shape[0]):
            if np.any(slice_xy[x, :]):
                x_left = x
                break

        for x in range (slice_xy.shape[0]-1,-1,-1):
            if np.any(slice_xy[x, :]):
                x_right = x
                break

        if x_left is None or x_right is None:
            continue

        scaffold_sides[z, :x_left+1, :] = slice_xy[:x_left+1, :]
        scaffold_sides[z, x_right:, :] = slice_xy[x_right:, :]

    filled_scaffold = np.zeros_like(scaffold_sides, dtype=bool)
    for z in range(scaffold_sides.shape[0]):
        slice_xy = scaffold_sides[z,:,:]
        filled_slice = morphology.convex_hull_image(slice_xy)
        filled_scaffold[z, :, :] = filled_slice

    return filled_scaffold

"""def estimate_scaffold_boundary(filled_scaffold, x0, z0, angle):

def extrude_scaffold_mask(mask_boundary_2d, y_size):"""


def apply_scaffold_mask(data, scaffold_mask):
    return np.where(scaffold_mask, data, 0)


def find_scaffold_mask(data, x0, z0, log=False):
    scaffold_mask = build_scaffold_mask(data, log=log)

    filled_scaffold = extract_scaffold_edges(scaffold_mask, log=log)

    """boundary_mask = estimate_scaffold_boundary(
        filled_scaffold,
        x0,
        z0,
    )

    return extrude_scaffold_mask(
        boundary_mask,
        data.shape[1],
    )"""

    return filled_scaffold
