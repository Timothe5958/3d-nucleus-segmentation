from dataclasses import replace

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from ..figure_saver import save_fig


def save_centroids_distrib(measurements, output_folder, title, metadata):
    centroids = measurements.centroids

    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(3, 2)
    ax = fig.add_subplot(gs[:2, :2])
    fig.add_subplot(gs[2, :])

    # scatter for easiest way to define the limits of the figure
    ax.scatter(centroids[:,1], centroids[:,0], alpha=0)

    for x, y, diameter in zip(
        centroids[:, 1],
        centroids[:, 0],
        measurements.equivalent_diameters,
        strict=False,
    ):
        circle = Circle(
            (x, y),
            radius=diameter / 2,
            color='#66C2A5',
            linewidth=0,
            alpha=0.25,
        )
        ax.add_patch(circle)

    ax.set_title('Nuclei centroid distribution')
    ax.set_ylabel('Z (µm)')
    ax.set_xlabel('X (µm)')

    ax.set_aspect('equal')
    ax.set_axisbelow(True)
    ax.grid(visible=True, linestyle='-', color='#D1D1D1')

    metadata_boxplot = replace(
        metadata,
        graph_information=('Graph information', 'Each point represents a nucleus and is positioned at the (x, z) coordinates of its centroid; '
        'the point size is proportional to the nucleus volume.'),
    )
    save_fig(fig, output_folder, title, metadata_boxplot)
