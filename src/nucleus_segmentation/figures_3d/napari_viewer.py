import matplotlib.pyplot as plt
import napari
import numpy as np
from napari.utils.colormaps import DirectLabelColormap

from ..processing.geometry.origin import find_axis_origin
from .view_config import ViewConfig


def add_x_scale_to_viewer(viewer, data, voxel_size, length_um, top_view=None):
    _, x_size, _ = data.shape
    length_px = int(length_um / (voxel_size * 1e6))

    # Trait placé à Z_min et Y_min, orienté suivant X
    line_data = np.zeros(data.shape, dtype=np.uint8)
    line_data[0:5, x_size - length_px - 1 : x_size, 0:5] = 1

    viewer.add_labels(
        line_data,
        scale=(1, 1, 1),
        colormap=DirectLabelColormap(
            color_dict={
                None: 'transparent',
                1: 'white',
            }
        ),
        opacity=1.0,
    )

    # Valeur physique de la longueur
    label = f'{length_um} µm'

    # Texte
    txt_coords = [
        0 if top_view else 30,
        x_size - length_px / 2,
        40 if top_view else 0,
    ]

    text_layer = viewer.add_points(
        np.array([txt_coords], dtype=float),
        name='X scale label',
        size=1,
        face_color='transparent',
        border_width=0,
        text={
            'string': [label],
            'size': 6,
            'color': 'white',
            'anchor': 'center',
        },
    )

    return text_layer



def _create_3d_view(data, config: ViewConfig):
    viewer = napari.Viewer(show=True, ndisplay=3)

    if config.is_label:
        # preparation of the color map
        num_labels = data.max()
        colors = plt.colormaps[config.cmap](np.linspace(0, 1, max(num_labels, 1)))

        # shuffle the colors to avoid having same color for neighbours
        rng = np.random.default_rng(42)
        rng.shuffle(colors)

        color_dict = {None: 'transparent'}
        color_dict.update({
            i: tuple(colors[i - 1])
            for i in range(1, num_labels + 1)
        })
        colormap = napari.utils.colormaps.DirectLabelColormap(color_dict=color_dict)

        # add the labels to the napari viewer
        layer = viewer.add_labels(
            data,
            opacity=1.0,
            scale=(1, 1, 1),
            colormap=colormap,
        )
    else:
        layer = viewer.add_image(
            data,
            opacity=1.0,
            scale=(1, 1, 1),
            rendering=config.mode,
            iso_threshold=0,
        )

    # Add axis
    viewer.dims.set_axis_label(0, 'Z')
    viewer.dims.set_axis_label(1, 'X')
    viewer.dims.set_axis_label(2, 'Y')
    viewer.axes.visible = True

    if config.voxel_size:
        add_x_scale_to_viewer(
            viewer,
            data,
            voxel_size=config.voxel_size,
            length_um=10,
            top_view=config.top_view,
        )

    viewer.scene.camera.angles = config.camera_rotation

    viewer.fit_to_view(layers=[layer], margin=0.05)

    return viewer


def open_3d_view(data, camera_rotation):
    viewer = _create_3d_view(
        data,
        camera_rotation,
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
