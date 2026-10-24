import matplotlib.pyplot as plt
import numpy as np

from ..save_figure import save_fig


def save_centroids_3d_view(measurements, output_folder, title, distance_max, num_neighbours_max):
    centroids = measurements.centroids
    volumes = measurements.volumes

    _, _, neighbour_counts = measurements.get_neighbours_distances(
        distance_max=distance_max,
        num_neighbours_max=num_neighbours_max,
    )
    num_neighbours_max = max(neighbour_counts)

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(projection='3d')
    sc = ax.scatter(
        centroids[:,2],
        centroids[:,1],
        centroids[:,0],
        s=volumes/20,
        c=neighbour_counts,
        cmap='jet',
        alpha=0.8,
        vmin=0,
        vmax=num_neighbours_max,
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.5, aspect=10)
    cbar.set_label(f'Number of Neighbors (within {distance_max} µm)')
    cbar.set_ticks(np.arange(0, num_neighbours_max + 1))
    ax.set_title('Centroid Positions')
    ax.set_xlabel("X (Groove's width, µm)")
    ax.set_ylabel("Y (Groove's length, µm)")
    ax.set_zlabel("Z (Groove's height, µm)")

    save_fig(fig, output_folder, title)
