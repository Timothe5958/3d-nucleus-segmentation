from pathlib import Path

import matplotlib.pyplot as plt


class Visualization:

    @staticmethod
    def save_histogram(data, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        plt.figure()
        plt.hist(data.ravel(), bins=512)
        plt.yscale('log')

        plt.xlabel('Intensity')
        plt.ylabel('Number of voxels')
        plt.title('Intensity histogram')
        plt.tight_layout()

        plt.savefig(output_path, dpi=150)
        plt.close()
