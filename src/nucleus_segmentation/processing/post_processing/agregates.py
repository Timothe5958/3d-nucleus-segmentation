import numpy as np
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.morphology import remove_small_objects
from skimage.segmentation import watershed


def split_agregate_local(int_map, binary_image, min_distance=10):
    binary_image = binary_image.astype(bool)

    # distance map
    distance = ndimage.distance_transform_edt(binary_image)
    distance *= int_map

    # detection of peaks
    coords = peak_local_max(
        distance,
        min_distance=min_distance,
        labels=binary_image,
        exclude_border=False,
    )

    # peak's centers
    peaks = np.zeros(binary_image.shape, dtype=bool)
    peaks[tuple(coords.T)] = True
    markers, _ = ndimage.label(peaks)

    # watershed
    labels = watershed(
        -distance,
        markers,
        mask=binary_image,
    )

    return np.array(labels)


def split_agregates(data_segmented, data_raw):
    intensity_map = data_raw * (data_segmented > 0)

    big_objects = remove_small_objects(data_segmented, max_size=28000)
    small_objects = data_segmented & ~big_objects

    small_objects_labeled, nb_small = ndimage.label(small_objects)
    big_objects_labeled, _ = ndimage.label(big_objects)

    slices = ndimage.find_objects(big_objects_labeled)

    final_labeled = small_objects_labeled.astype(np.int32, copy=True)

    next_start_label = nb_small
    for i, slc in enumerate(slices, start=1):
        local_mask = big_objects_labeled[slc] == i
        local_int_map = intensity_map[slc]

        split_labels = split_agregate_local(
            local_int_map,
            local_mask,
        )
        split_labels[split_labels > 0] += next_start_label

        local_output = final_labeled[slc]
        local_output[local_mask] = split_labels[local_mask]
        final_labeled[slc] = local_output

        next_start_label = split_labels.max()

    return final_labeled
