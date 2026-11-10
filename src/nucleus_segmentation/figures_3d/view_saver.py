from pathlib import Path

from .napari_viewer import _create_3d_view
from .view_config import ViewConfig


def save_image_view(image, path, config: ViewConfig):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    viewer = _create_3d_view(
        image,
        config,
    )
    viewer.screenshot(
        path=output_path,
        canvas_only=True,
    )
    viewer.close()
