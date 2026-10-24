import matplotlib.pyplot as plt
import numpy as np

from ..save_figure import save_fig


def save_boxplot(values, output_folder, title, labels):

    fig = plt.figure(figsize=(6, 8))
    plt.boxplot(
        values,
        vert=True,
        patch_artist=True,
        boxprops={'facecolor': '#2A9D8F', 'edgecolor': 'black', 'alpha': 0.7},
        medianprops={'color': 'black', 'linewidth': 2},
        whiskerprops={'color': 'black'},
        capprops={'color': 'black'},
    )

    x_jitter = np.random.normal(1, 0.04, size=len(values))
    plt.scatter(x_jitter, values, alpha=0.4, color='gray', s=15, zorder=3)

    plt.title(title)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])

    save_fig(fig, output_folder, title + '.png')
