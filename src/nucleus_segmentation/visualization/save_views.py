from pathlib import Path

from .napari_viewer import _create_3d_view


def save_image_view(image, path, mode='mip', camera_rotation=(95, 0, -70)):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    viewer = _create_3d_view(
        image,
        camera_rotation,
        mode=mode,
        is_label=False,
    )
    viewer.screenshot(
        path=output_path,
        canvas_only=True,
    )
    viewer.close()


def save_label_view(labels, path, camera_rotation=(95, 0, -70), cmap='turbo'):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    viewer = _create_3d_view(
        labels,
        camera_rotation,
        is_label=True,
        cmap=cmap,
    )
    viewer.screenshot(
        path=output_path,
        canvas_only=True,
    )
    viewer.close()
