import matplotlib.pyplot as plt

from ..save_figure import save_fig


def save_centroids_density(measurements, bin_width, output_folder, title):
    densities, bin_centers = measurements.get_densities(bin_width)

    fig = plt.figure()

    plt.barh(bin_centers, densities, height=bin_width*0.8, color='skyblue', edgecolor='black')

    plt.title('Nuclei Density along the Vertical Axis')
    plt.xlabel('Nuclei Density (Number of Nuclei / cm$^2$)')
    plt.grid(visible=True, axis='x', linestyle='--')

    save_fig(fig, output_folder, title)
