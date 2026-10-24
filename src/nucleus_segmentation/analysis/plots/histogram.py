import matplotlib.pyplot as plt
import numpy as np

from ..save_figure import save_fig


def save_histogram(values, output_folder, title, labels):

    mean = np.mean(values)
    median = np.median(values)
    std = np.std(values)

    fig = plt.figure()
    plt.hist(values, bins='fd', color='skyblue', edgecolor='black', alpha=0.6, label='Distribution')

    plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean:.1f}')
    plt.axvline(median, color='green', linestyle='-', linewidth=2, label=f'Median: {median:.1f}')
    plt.axvspan(mean - std, mean + std, color='red', alpha=0.1, label='Standard deviation')

    plt.title(title)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.legend()

    filename = title.replace(' ', '_') + '.png'
    save_fig(fig, output_folder, filename)
