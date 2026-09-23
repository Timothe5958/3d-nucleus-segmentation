"""CZI Reader"""

import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from czifile import CziFile


class CziReader:
    """
    This class is used to make the access to data from the czi files easier.
    """

    def __init__(self, path_str):
        self.path = Path(path_str)

        with CziFile(self.path) as czi:
            self.scene = czi.scenes[0]
            self.raw_data = self.scene.asarray()
            self.parsed_metadata = ET.fromstring(czi.metadata())

    def get_raw_slice(self, slice_id):
        """Returns a slice of the data not resampled."""
        return self.raw_data[slice_id,:,:]

    def get_raw_segment(self, start_id, stop_id):
        """Returns a segment of the data not resampled."""
        return self.raw_data[start_id:stop_id, :, :]

    def get_raw_data_dimensions(self):
        height = int(self.parsed_metadata.find('.//CameraFrameHeight').text)
        width = int(self.parsed_metadata.find('.//CameraFrameWidth').text)
        depth = int(self.parsed_metadata.find('.//DimensionZ').text)
        return (depth, height, width)

    def get_voxels_size(self):
        x = float(self.parsed_metadata.find('.//ScalingX').text)
        y = float(self.parsed_metadata.find('.//ScalingY').text)
        z = float(self.parsed_metadata.find('.//ScalingZ').text)
        return np.array([z, x, y])
