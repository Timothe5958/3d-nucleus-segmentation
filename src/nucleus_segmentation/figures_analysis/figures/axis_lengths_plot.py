import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from ..figure_saver import save_fig


def save_nuclei_axis_lengths_plot(measurements, output_folder, title, metadata):
    major_axes = np.asarray(measurements.major_axes)
    minor_axes = np.asarray(measurements.minor_axes)

    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(3, 2)
    ax = fig.add_subplot(gs[:2, :2])
    fig.add_subplot(gs[2, :])

    ax.scatter(
        major_axes,
        minor_axes,
        s=30,
        color='#66C2A5',
        alpha=0.8,
        edgecolors='none',
        rasterized=True,
    )

    x_lim = (major_axes.min() * 0.7, major_axes.max() * 1.03)
    ax.set_xlim(*x_lim)
    ax.set_ylim(minor_axes.min() * 0.7, minor_axes.max() * 1.03)
    ax.set_aspect('equal', adjustable='box')

    lin_regress = linregress(major_axes, minor_axes)
    slope = lin_regress.slope
    intercept = lin_regress.intercept
    r_squared = lin_regress.rvalue ** 2

    x_line = np.array(x_lim)
    y_line = slope * x_line + intercept
    ax.plot(
        x_line,
        y_line,
        color='#333333',
        linewidth=1.3,
        label='Linear regression',
    )

    equation_text = f'$y = {slope:.4f}x + {intercept:.4f}$\n$R^2 = {r_squared:.3f}$'
    ax.text(
        0.05, 0.95, equation_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox={'facecolor': 'white'},
    )

    ax.set_title('Length of major and minor axes')
    ax.set_xlabel('Major axis (µm)')
    ax.set_ylabel('Minor axis (µm)')

    save_fig(fig, output_folder, title, metadata)
