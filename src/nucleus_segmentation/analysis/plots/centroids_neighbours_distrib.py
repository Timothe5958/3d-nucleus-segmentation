import matplotlib.pyplot as plt

from ..save_figure import save_fig


def save_centroids_neighbours_distrib(measurements, output_folder, title, distance_max, num_neighbours_max):
    _, _, neighbour_counts = measurements.get_neighbours_distances(
        distance_max=distance_max,
        num_neighbours_max=num_neighbours_max,
    )

    fig = plt.figure()

    plt.scatter(measurements.centroids[:,0], neighbour_counts)
    plt.title('Number of Neighbors vs. Distance along the Z Axis')
    plt.xlabel('Distance along the Z Axis (µm)')
    plt.ylabel(f'Number of Neighbours (within {distance_max} µm)')

    save_fig(fig, output_folder, title)
