from dataclasses import replace

import matplotlib.pyplot as plt
import numpy as np

from ..figure_saver import save_fig


def save_centroids_3d_view(measurements, output_folder, title, metadata):
    centroids = measurements.centroids
    volumes = measurements.volumes

    _, _, neighbour_counts = measurements.get_neighbours_distances()
    num_neighbours_max = max(neighbour_counts)

    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(3, 2)
    ax = fig.add_subplot(gs[:2, :2], projection='3d')
    fig.add_subplot(gs[2, :])

    sc = ax.scatter(
        centroids[:,2],
        centroids[:,1],
        centroids[:,0],
        s=volumes/40,
        c=neighbour_counts,
        cmap='plasma_r',
        alpha=0.85,
        vmin=0,
        vmax=num_neighbours_max,
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.4, aspect=10, pad=0.15)
    cbar.set_label(f'Number of Neighbors (within {measurements.options.neighbours_dist_max} µm)')
    cbar.set_ticks(np.arange(0, num_neighbours_max + 1, 6))
    ax.set_title("Nuclei's volume and centroid position")
    ax.set_xlabel('Y (µm)')
    ax.set_ylabel('X (µm)')
    ax.set_zlabel('Z (µm)')

    metadata_boxplot = replace(
        metadata,
        graph_information=('Graph information', 'Each point represents a nucleus and is positioned at its center; '
        'the point size is proportional to the nucleus volume.'),
    )
    save_fig(fig, output_folder, title, metadata_boxplot)
