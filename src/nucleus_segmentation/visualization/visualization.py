import gc
from pathlib import Path

import matplotlib.pyplot as plt
import napari


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

    @staticmethod
    def save_2d_view(data, output_path, camera_rotation):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        viewer = napari.Viewer(show=True, ndisplay=3)
        viewer.add_image(data, opacity=1.0, scale=(1, 1, 1))

        viewer.scene.camera.angles = camera_rotation
        viewer.scene.camera.zoom = 1
        viewer.screenshot(path=output_path, canvas_only=True)

        # Close
        # viewer.close()

        # Free memory
        del viewer
        gc.collect()
