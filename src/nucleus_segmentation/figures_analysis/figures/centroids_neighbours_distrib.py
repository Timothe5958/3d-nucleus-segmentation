import matplotlib.pyplot as plt

from ..figure_saver import save_fig


def save_centroids_neighbours_distrib(measurements, output_folder, title, metadata):
    _, _, neighbour_counts = measurements.get_neighbours_distances()

    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(3, 2)
    ax = fig.add_subplot(gs[:2, :2])
    fig.add_subplot(gs[2, :])

    ax.scatter(
        measurements.centroids[:,0],
        neighbour_counts,
        s=40,
        color='#66C2A5',
        alpha=0.8,
        edgecolors='none',
        rasterized=True,
    )
    ax.set_title('Number of neighbors and distance along Z-axis')
    ax.set_xlabel('Z (µm)')
    ax.set_ylabel(f'Number of neighbours (within {measurements.options.neighbours_dist_max} µm)')

    ax.set_axisbelow(True)
    ax.grid(visible=True, linestyle='-', color='#D1D1D1')

    save_fig(fig, output_folder, title, metadata)
