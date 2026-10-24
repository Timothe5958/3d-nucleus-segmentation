import matplotlib.pyplot as plt
import numpy as np

from ..save_figure import save_fig


def save_nuclei_axis_lengths_plot(major_axes, minor_axes, output_folder, title):
    fig = plt.figure()
    plt.scatter(major_axes, minor_axes)

    slope, intercept = np.polyfit(major_axes, minor_axes, 1)
    correlation_matrix = np.corrcoef(major_axes, minor_axes)
    r_squared = correlation_matrix[0, 1]**2
    regression_line = slope * major_axes + intercept
    plt.plot(major_axes, regression_line, color='red', linewidth=2, label='Regression Line')
    equation_text = f'$y = {slope:.4f}x + {intercept:.4f}$\n$R^2 = {r_squared:.3f}$'
    plt.gca().text(0.05, 0.95, equation_text, transform=plt.gca().transAxes,
               fontsize=12, verticalalignment='top',
               bbox={'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.7})

    plt.title('Length of Major and Minor Axes')
    plt.xlabel('Major axis (µm)')
    plt.ylabel('Minor axis (µm)')

    save_fig(fig, output_folder, title)
