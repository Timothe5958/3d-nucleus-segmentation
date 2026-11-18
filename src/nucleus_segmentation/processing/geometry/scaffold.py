import numpy as np
from scipy.signal import correlate


def scaffold_mask_2d(voxel_size_m, include_bottom=True):
    voxel_size_um = voxel_size_m * 1e6

    width = int(250 // voxel_size_um)
    height_parallel = int(250 // voxel_size_um)
    height_triangle = width // 2
    height = height_triangle + height_parallel

    scaffold_filled = np.zeros((height, width))
    scaffold_filled[height_triangle:height, :] = 1

    if include_bottom:
        for z in range(height_triangle):
            max_x = width - z
            min_x = z
            scaffold_filled[height_triangle - 1 - z, min_x:max_x] = 1

    return scaffold_filled


def scaffold_mask_3d(voxel_size_m, depth_voxels):
    voxel_size_um = voxel_size_m * 1e6

    width = int(250 // voxel_size_um)
    height_parallel = int(250 // voxel_size_um)
    height_triangle = width // 2
    height = height_triangle + height_parallel

    scaffold_filled = np.zeros((height, width, depth_voxels))
    scaffold_filled[height_triangle:height, :, :] = 1

    for z in range(height_triangle):
        max_x = width - z
        min_x = z
        scaffold_filled[height_triangle - 1 - z, min_x:max_x, :] = 1

    return scaffold_filled


def global_scaffold(data, voxel_size, include_bottom=False):
    z_bottom, x_bottom = estimate_scaffold_origin(data, voxel_size=voxel_size)
    scaffold_2d = scaffold_mask_2d(voxel_size, include_bottom=include_bottom)

    # crop the offset bottom of the scaffolds (outside image)
    if z_bottom < 0:
        scaffold_2d = scaffold_2d[-z_bottom:, :]
        z_bottom = 0

    # crop the offset top
    top_offset = z_bottom + scaffold_2d.shape[0] - data.shape[0]
    if top_offset > 0:
        scaffold_2d = scaffold_2d[:-top_offset, :]

    # create the global scaffolds
    scaffold_2d_global = np.zeros(data.shape[:2])
    scaffold_2d_global[
        z_bottom:z_bottom + scaffold_2d.shape[0],
        x_bottom:x_bottom + scaffold_2d.shape[1],
    ] = scaffold_2d

    return scaffold_2d_global


def estimate_scaffold_origin(data, voxel_size):
    scaffold_2d = scaffold_mask_2d(voxel_size)
    projected_data = np.any(data, axis=2)

    scores = correlate(
        projected_data,
        scaffold_2d,
        mode='full',
        method='fft',
    )

    best_score = 0
    origin = (0, 0)

    for x in range(scores.shape[1]):
        scores_col = scores[:, x]
        z = np.where(scores_col == scores_col.max())[0].max()
        score = scores_col[z]

        if score > best_score:
            best_score = score
            origin = (
                z - (scaffold_2d.shape[0] - 1),
                x - (scaffold_2d.shape[1] - 1),
            )
    return origin
