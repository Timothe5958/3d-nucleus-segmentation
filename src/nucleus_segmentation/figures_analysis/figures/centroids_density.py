import matplotlib.pyplot as plt

from ..figure_saver import save_fig


def save_centroids_density(measurements, output_folder, title, metadata):
    densities, bin_centers = measurements.get_densities()
    bin_width = measurements.options.centroids_density_bin_with

    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(3, 2)
    ax = fig.add_subplot(gs[:2, :2])
    fig.add_subplot(gs[2, :])

    ax.barh(bin_centers, densities, height=bin_width*0.8, edgecolor='white', linewidth=0.5, color='#66C2A5')

    ax.set_title('Nuclei density along the vertical axis')
    ax.set_xlabel('Nuclei density (number of nuclei / (100 µm)$^3$)')
    ax.set_ylabel('Z (µm)')

    ax.set_axisbelow(True)
    ax.grid(visible=True, axis='x', linestyle='-')

    save_fig(fig, output_folder, title, metadata)
