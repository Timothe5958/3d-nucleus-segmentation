"""CZI Reader"""

import xml.etree.ElementTree as ET
from collections import UserList
from pathlib import Path

import numpy as np
from czifile import CziFile


class Observation:
    """
    This class is used to make the access to data from the czi files easier.
    """

    def __init__(self, path):
        self.path = Path(path)
        self.name = self.path.stem
        self._raw_data = None
        self._parsed_metadata = None
        self._scene = None
        self._origin = None

    def get_raw_data(self):
        if self._raw_data is None:
            with CziFile(self.path) as czi:
                self._scene = czi.scenes[0]
                self._raw_data = self._scene.asarray()
                self._parsed_metadata = ET.fromstring(czi.metadata())

        return self._raw_data

    def get_voxel_dims(self):
        if self._parsed_metadata is None:
            self.get_raw_data()

        x = float(self._parsed_metadata.find('.//ScalingX').text)
        y = float(self._parsed_metadata.find('.//ScalingY').text)
        z = float(self._parsed_metadata.find('.//ScalingZ').text)
        return np.array([z, x, y])

    def get_resampled_voxel_size(self):
        return np.min(self.get_voxel_dims())


class ObservationsList(UserList):
    """
    This class is used to have an easy access on many observations from a folder's path. Every observation in this folder will be listed.

    Parameters
    ----------
    path : Path
        This is the path of the folder.

    """

    def __init__(self, folder_path):
        self.path = Path(folder_path)

        observations = []
        for czi_path in self.path.glob('*.czi'):
            observations.append(Observation(path=czi_path))

        self.data = observations

