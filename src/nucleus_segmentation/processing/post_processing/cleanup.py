from skimage.morphology import remove_small_objects


def remove_small_artefacts(data, max_size=1000):
    return remove_small_objects(data, max_size=max_size)
