"""CZI Reader"""

from pathlib import Path

from czifile import CziFile


class CziReader:
    """
    This class is used to make the access to data from the czi files easier.
    """

    def __init__(self, path_str):
        self.path = Path(path_str)

        with CziFile(self.path) as czi:
            self.scene = czi.scenes[0]
            self.np_image = self.scene.asarray()


    def get_slice(self, slice_id):
        return self.np_image[slice_id,:,:]

