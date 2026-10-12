import matplotlib.pyplot as plt
import napari
import numpy as np

from ..geometry.origin import find_axis_origin


def _create_3d_view(data, camera_rotation, mode='mip', is_label=False, cmap='turbo'):
    viewer = napari.Viewer(show=True, ndisplay=3)

    if is_label:
        # preparation of the color map
        num_labels = data.max()
        colors = plt.colormaps[cmap](np.linspace(0, 1, max(num_labels, 1)))

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
            rendering=mode,
            iso_threshold=0,
        )

    # Add axis
    viewer.dims.set_axis_label(0, 'Z')
    viewer.dims.set_axis_label(1, 'X')
    viewer.dims.set_axis_label(2, 'Y')
    viewer.axes.visible = True

    viewer.scene.camera.angles = camera_rotation

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
