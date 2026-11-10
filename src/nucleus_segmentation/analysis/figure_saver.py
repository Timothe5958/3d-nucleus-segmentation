from dataclasses import astuple
from pathlib import Path
from textwrap import fill

import matplotlib.pyplot as plt


def save_fig(fig, output_folder, filename, metadata):
    output_path = Path(output_folder) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        (label, fill(value, width=80))
        for label, value in astuple(metadata)
        if label is not None and value is not None
    ]

    ax_metadata = fig.get_axes()[1]
    ax_metadata.axis('off')

    table = ax_metadata.table(
        cellText=lines,
        colLabels=None,
        colWidths=[0.25, 0.75],
        cellLoc='left',
        loc='center',
    )

    table.auto_set_font_size(True)
    table.scale(1, 1.5)
    for (_, col), cell in table.get_celld().items():
        if col == 0:
            cell.set_text_props(weight='bold')

    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
