from pathlib import Path

import matplotlib.pyplot as plt
import napari

from ..geometry.origin import find_axis_origin


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


def _create_3d_view(data, camera_rotation, mode, show=False):
    viewer = napari.Viewer(show=show, ndisplay=3)

    viewer.add_image(
        data,
        opacity=1.0,
        scale=(1, 1, 1),
        rendering=mode,
        iso_threshold=0,
    )

    # Add axis
    viewer.dims.set_axis_label(0, 'Z')
    viewer.dims.set_axis_label(1, 'X')
    viewer.dims.set_axis_label(2, 'Y')
    viewer.axes.visible = True

    viewer.scene.camera.angles = camera_rotation

    return viewer


def open_3d_view(data, camera_rotation):
    viewer = _create_3d_view(
        data,
        camera_rotation,
        show=True,
    )

    # Add origin to the view
    origin = find_axis_origin(data)
    viewer.add_points(
        [origin],
        size=4,
        symbol='cross',
        face_color='white',
    )

    napari.run()


def save_projected_view(data, name, mode='mip', camera_rotation=(95, 0, -70)):
    output_path = Path('outputs/3d_previews/projected_' + name + '.png')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    viewer = _create_3d_view(
        data,
        camera_rotation,
        mode,
        show=True,
    )

    # take the image with a set angle of view
    viewer.screenshot(
        path=output_path,
        canvas_only=True,
    )

    viewer.close()
