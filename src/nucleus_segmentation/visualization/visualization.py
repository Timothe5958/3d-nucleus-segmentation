import gc
from pathlib import Path

import matplotlib.pyplot as plt
import napari

from ..geometry.origin import find_axis_origin


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

        # Adding the axis
        viewer.dims.set_axis_label(0, 'Z')
        viewer.dims.set_axis_label(1, 'X')
        viewer.dims.set_axis_label(2, 'Y')
        viewer.axes.visible = True

        # Adding the origin
        origin = find_axis_origin(data)
        viewer.add_points(
            [origin],
            size=3,
            symbol='cross',
            face_color='white',
        )

        viewer.scene.camera.angles = camera_rotation
        viewer.scene.camera.zoom = 1
        viewer.screenshot(path=output_path, canvas_only=True)

        # Close
        # viewer.close()

        # Free memory
        del viewer
        gc.collect()
