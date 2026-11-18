from dataclasses import replace

import matplotlib.pyplot as plt
import numpy as np

from ..figure_saver import save_fig


def save_histogram(values, output_folder, title, labels, metadata):

    mean = np.mean(values)
    median = np.median(values)
    std = np.std(values)

    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(3, 2)
    ax = fig.add_subplot(gs[:2, :2])
    fig.add_subplot(gs[2, :])

    ax.hist(values, bins='fd', color='#66C2A5', label='Distribution', linewidth=0, rwidth=0.85)

    # Standard deviation
    ax.axvspan(
        mean - std, mean + std,
        color='#66C2A5',
        alpha=0.18,
        linewidth=0,
        label='Mean ± SD',
    )

    # Mean
    ax.axvline(
        mean,
        color='#333333',
        linestyle='-',
        linewidth=1.2,
        label=f'Mean = {mean:.1f}',
    )

    # Median
    ax.axvline(
        median,
        color='#333333',
        linestyle='--',
        linewidth=1.2,
        label=f'Median = {median:.1f}',
    )

    ax.set_title(title)
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    metadata_histo = replace(
        metadata,
        graph_information=(
            'Graph information',
            f'The solid line indicates the mean ({mean:.1f}); '
            f'The dotted line indicates the median ({median:.1f}); '
            f'the shaded area represents the mean ± standard deviation ({mean:.1f} ± {std:.1f}).'
        ),
    )
    filename = title.replace(' ', '_') + '.png'
    save_fig(fig, output_folder, filename, metadata_histo)
