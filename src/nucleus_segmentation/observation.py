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
        self._raw_data = None
        self._parsed_metadata = None
        self._scene = None

    def get_raw_data(self):
        if self._raw_data is None:
            with CziFile(self.path) as czi:
                self._scene = czi.scenes[0]
                self._raw_data = self.scene.asarray()
                self._parsed_metadata = ET.fromstring(czi.metadata())

        return self._raw_data

    def get_raw_slice(self, slice_id):
        """Returns a slice of the data not resampled."""
        return self.get_raw_data()[slice_id,:,:]

    def get_raw_segment(self, start_id, stop_id):
        """Returns a segment of the data not resampled."""
        return self.self.get_raw_data()[start_id:stop_id, :, :]

    def get_raw_data_dimensions(self):
        if self._parsed_metadata is None:
            self.get_raw_data()

        height = int(self.parsed_metadata.find('.//CameraFrameHeight').text)
        width = int(self.parsed_metadata.find('.//CameraFrameWidth').text)
        depth = int(self.parsed_metadata.find('.//DimensionZ').text)
        return (depth, height, width)

    def get_voxels_size(self):
        if self._parsed_metadata is None:
            self.get_raw_data()

        x = float(self.parsed_metadata.find('.//ScalingX').text)
        y = float(self.parsed_metadata.find('.//ScalingY').text)
        z = float(self.parsed_metadata.find('.//ScalingZ').text)
        return np.array([z, x, y])

    def get_resampled_voxel_size(self):
        return np.min(self.get_voxels_size())


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

