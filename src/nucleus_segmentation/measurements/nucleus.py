import numpy as np
from skimage import measure


class NucleusMeasurements:
    def __init__(self, region, voxel_size_um, label):
        self.region = region
        self.voxel_size_um = voxel_size_um
        self.label = label
        self.centroid = region.centroid # coordinates in voxel

        # -- properties --
        self.volume = region.area * voxel_size_um ** 3
        self.major_axis = region.axis_major_length * voxel_size_um
        self.minor_axis = region.axis_minor_length * voxel_size_um
        self.elongation = self.major_axis / self.minor_axis
        self.equivalent_diameter = region.equivalent_diameter_area * voxel_size_um

        # -- sphericity property --
        nucleus = np.pad(region.image, 1, constant_values=False)
        # compute 3D surface mesh
        verts, faces, _, _ = measure.marching_cubes(
            nucleus, level=0.5,
        )
        surface = measure.mesh_surface_area(verts, faces)
        self.sphericity = np.pi**(1/3) * (6 * region.area)**(2/3) / surface

    def distance_to_scaffold(self, distance_map):
        return distance_map[int(self.centroid[0]), int(self.centroid[1])]
