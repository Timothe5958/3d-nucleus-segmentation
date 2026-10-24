import matplotlib.pyplot as plt

from ..save_figure import save_fig


def save_centroids_distrib(measurements, output_folder, title):
    centroids = measurements.centroids
    volumes = measurements.volumes

    fig = plt.figure()
    plt.scatter(centroids[:,1], centroids[:,0], s=volumes/100, alpha=0.4)

    plt.title('Nuclei centroid distribution')
    plt.ylabel('Z (voxel)')
    plt.xlabel('X (voxel)')
    plt.grid(visible=True, linestyle='--')

    save_fig(fig, output_folder, title)
