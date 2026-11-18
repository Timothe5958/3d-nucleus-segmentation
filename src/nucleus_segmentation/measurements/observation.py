import copy
from collections import UserList
from datetime import datetime

import numpy as np
from scipy.ndimage import distance_transform_edt
from skimage import measure

from ..output.options import PlotMetadata
from ..processing.geometry import global_scaffold
from .nuclei_collection import NucleiCollection
from .nucleus import NucleusMeasurements


class ObservationMeasurements:
    def __init__(self, labelled_data, segmented_data, obs_name, voxel_size, options):
        self.labelled_data = labelled_data
        self.segmented_data = segmented_data
        self.voxel_size_um = voxel_size * 1e6
        self.options = options

        # scaffold & distance map
        self.global_scaffold_2d = global_scaffold(
            segmented_data,
            voxel_size,
            include_bottom=False,
        )

        self.nuclei = NucleiCollection(
            [],
            labelled_data=labelled_data,
            voxel_size_um=self.voxel_size_um,
            density_mask=self.global_scaffold_2d,
            options=self.options,
        )
        self.regions = measure.regionprops(self.labelled_data)
        for region in self.regions:
            # only if the centroid is above the v shape of the scaffold
            if region.centroid[0] > np.where(self.global_scaffold_2d > 0)[0][0]:
                self.nuclei.append(NucleusMeasurements(region, self.voxel_size_um, region.label))

        # metadata
        self.start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.metadata = PlotMetadata(
            obs_name=('Observation name', obs_name),
            date_of_processing=('Date of processing', self.start_date),
            nb_nuclei=('Number of nuclei', str(len(self.nuclei))),
            voxel_size=('Voxel size', f'{round(self.voxel_size_um, 3)} µm'),
        )

    def nuclei_far_from_scaffold(self, distance_um):
        """Returns only the nuclei that are farther from the scaffold than the specifies distance."""
        # -- compute the distance map from scaffold --

        scaffold_contours_2d = np.abs(np.diff(self.global_scaffold_2d, axis=1))
        # add one col because np.diff reduce the shape
        scaffold_contours_2d = np.pad(scaffold_contours_2d, ((0, 0), (1, 0)), mode='constant')

        distance_map = distance_transform_edt(
            scaffold_contours_2d == 0,
            sampling=self.voxel_size_um,
        )

        # filter the nuclei
        nuclei_to_keep = [
            nucleus
            for nucleus in self.nuclei
            if nucleus.distance_to_scaffold(distance_map) >= distance_um
        ]
        labels_to_keep = [nucleus.label for nucleus in nuclei_to_keep]
        labelled_data = copy.deepcopy(self.labelled_data)
        labelled_data[~np.isin(labelled_data, labels_to_keep)] = 0

        return NucleiCollection(
            nuclei_to_keep,
            labelled_data=labelled_data,
            voxel_size_um=self.voxel_size_um,
            density_mask=self.nuclei.density_mask * (distance_map > distance_um),
            options=self.options,
        )

    def nuclei_in_bbox(self, bbox):
        """Returns only the nuclei whose centroid is in the specified bounding box."""

        z_min, x_min, z_max, x_max = bbox
        density_mask = np.zeros_like(self.nuclei.density_mask)
        density_mask[z_min:z_max, x_min:x_max] = 1

        nuclei_to_keep = [
            nucleus
            for nucleus in self.nuclei
            if (
                z_min <= nucleus.centroid[0] < z_max
                and x_min <= nucleus.centroid[1] < x_max
            )
        ]
        labels_to_keep = [nucleus.label for nucleus in nuclei_to_keep]
        labelled_data = copy.deepcopy(self.labelled_data)
        labelled_data[~np.isin(labelled_data, labels_to_keep)] = 0

        return NucleiCollection(
            nuclei_to_keep,
            labelled_data=labelled_data,
            voxel_size_um=self.voxel_size_um,
            density_mask=density_mask,
            options=self.options,
        )

class ObservationsMeasurements(UserList):
    def __init__(self, observations_measurements):
        super().__init__(observations_measurements)
