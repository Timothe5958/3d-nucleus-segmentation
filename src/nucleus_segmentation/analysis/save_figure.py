from pathlib import Path

import matplotlib.pyplot as plt


def save_fig(fig, output_folder, filename):
    output_path = Path(output_folder) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close(fig)
