from dataclasses import replace

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba

from ..figure_saver import save_fig


def save_boxplot_points(values, output_folder, title, labels, metadata):
    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(3, 2)
    ax = fig.add_subplot(gs[:2, 0])
    fig.add_subplot(gs[2, :])

    ax.boxplot(
        values,
        vert=True,
        patch_artist=True,
        showfliers=False,
        boxprops={'facecolor': to_rgba('#009E73', 0.35), 'edgecolor': '#000000', 'linewidth': 1},
        medianprops={'color': '#000000', 'linewidth': 2},
        whiskerprops={'color': '#000000', 'linewidth': 1},
        capprops={'color': '#000000', 'linewidth': 1},
    )

    x_jitter = np.random.normal(1, 0.025, size=len(values))
    ax.scatter(x_jitter, values, alpha=0.4, color='gray', s=15, zorder=3)

    ax.set_title(title)
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    save_fig(fig, output_folder, title + '.png', metadata)


def save_boxplot_violin(values, output_folder, title, labels, metadata):
    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(3, 2)
    ax = fig.add_subplot(gs[:2, 0])
    fig.add_subplot(gs[2, :])

    parts = ax.violinplot(
        values,
        positions=[1],
        widths=0.5,
        showextrema=False,
        showmedians=False,
    )
    for body in parts['bodies']:
        # remove the left part
        verts = body.get_paths()[0].vertices
        verts[:, 0] = np.maximum(verts[:, 0], 1)

        body.set_facecolor(to_rgba('#009E73', 0.25))
        body.set_edgecolor('#009E73')
        body.set_linewidth(0.8)

    boxplot = ax.boxplot(
        values,
        positions=[1],
        vert=True,
        patch_artist=True,
        showfliers=True,
        boxprops={'facecolor': '#66C2A5', 'edgecolor': '#000000', 'linewidth': 0.8},
        medianprops={'color': '#000000', 'linewidth': 1.5},
        whiskerprops={'color': '#000000', 'linewidth': 0.8},
        capprops={'color': '#000000', 'linewidth': 0.8},
    )

    ax.set_xlim(0.5, 1.5)

    ax.set_title(title)
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    # add number of outliers and graph info to the metadata
    n_outliers = len(boxplot['fliers'][0].get_ydata())
    n_outliers_txt = f' (including {n_outliers} outliers in the boxplot)'
    metadata_nb_nuclei = (metadata.nb_nuclei[0], metadata.nb_nuclei[1] + n_outliers_txt)

    metadata_boxplot = replace(
        metadata,
        graph_information=('Graph information', 'Boxes show the interquartile range (IQR) with the median as a line; '
        'whiskers extend to 1.5 × IQR; points beyond are outliers.'),
        nb_nuclei=metadata_nb_nuclei,
    )

    save_fig(fig, output_folder, title + '.png', metadata_boxplot)
