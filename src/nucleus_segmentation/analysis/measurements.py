import numpy as np
from scipy.spatial import cKDTree
from skimage import measure


class NucleiMeasurements:
    def __init__(self, labelled_data, observation):
        self.labelled_data = labelled_data
        self.voxel_size_um = observation.get_resampled_voxel_size() * 1e6
        self.volumes = self._get_volumes(labelled_data, self.voxel_size_um)
        self._compute_properties()
        self.neighbours_distances = None


    @staticmethod
    def _get_volumes(labelled_data, voxel_size_um):
        _, volumes = np.unique(labelled_data, return_counts=True)
        return volumes[1:] * voxel_size_um**3


    @property
    def get_y_bounds(self):
        return (0, self.labelled_data.shape[2])


    def _compute_properties(self):
        regions = measure.regionprops(self.labelled_data)

        major_axes = []
        minor_axes = []
        elongations = []
        centroids = []
        equivalent_diameters = []
        sphericities = []

        for region in regions:
            # computer major and minor axis, and elongation
            major_axis = region.axis_major_length
            minor_axis = region.axis_minor_length

            major_axes.append(major_axis)
            minor_axes.append(minor_axis)
            elongations.append(major_axis / minor_axis)

            # compute centroid
            centroids.append(region.centroid)

            # compute equivalent diameter
            equivalent_diameter = region.equivalent_diameter_area
            equivalent_diameters.append(equivalent_diameter)

            # --- sphericity --- #
            # extract local mask
            nucleus = np.pad(region.image, 1, constant_values=False)

            # compute 3D surface mesh
            verts, faces, _, _ = measure.marching_cubes(
                nucleus, level=0.5
            )
            surface = measure.mesh_surface_area(verts, faces)

            # compute sphericity
            sphericity = ((np.pi * equivalent_diameter**2) / surface)
            sphericities.append(sphericity)

        self.major_axes = np.array(major_axes) * self.voxel_size_um
        self.minor_axes = np.array(minor_axes) * self.voxel_size_um
        self.elongations = np.array(elongations)
        self.centroids = np.array(centroids) * self.voxel_size_um
        self.equivalent_diameters = np.array(equivalent_diameters) * self.voxel_size_um
        self.sphericities = np.array(sphericities)

    def get_densities(self, bin_width):
        centroids = self.centroids

        max_height = int(bin_width * (np.max(centroids[:, 0]) // bin_width + 1))
        bins = np.arange(np.min(centroids[:, 0]), max_height + bin_width, bin_width)

        nuclei_counts, bin_edges = np.histogram(centroids[:, 0], bins=bins)
        bin_centers = bin_edges[:-1] + (bin_width / 2)

        y_min, y_max = self.get_y_bounds
        bin_surface = (bin_width / np.cos(np.pi / 4)) * (y_max - y_min) * 2

        densities_per_cm2 = nuclei_counts / (bin_surface * 1e-8)
        return densities_per_cm2, bin_centers


    def _compute_neighbours(self, distance_max, num_neighbours_max):
        tree = cKDTree(self.centroids)

        distances, indices = tree.query(
            self.centroids,
            k=num_neighbours_max + 1,
            distance_upper_bound=distance_max,
        )

        self.neighbours_indices = indices[:, 1:]
        self.neighbours_distances = distances[:, 1:]
        self.neighbour_counts = np.sum(self.neighbours_distances != np.inf, axis=1)

    def get_neighbours_distances(self, distance_max=None, num_neighbours_max=None):
        # compute for the first time or compute again if new distance max
        if self.neighbours_distances is None or distance_max is not None:
            self._compute_neighbours(distance_max, num_neighbours_max)

        return (
            self.neighbours_indices,
            self.neighbours_distances,
            self.neighbour_counts,
        )

    def get_nearest_neighbours(self, distance_max=None, num_neighbours_max=None):
        # compute for the first time or compute again if new distance max
        if self.neighbours_distances is None or distance_max is not None:
            self._compute_neighbours(distance_max, num_neighbours_max)

        return self.neighbours_distances[:, 0]

    def get_nearest_distances(self, distance_max=None, num_neighbours_max=None):
        """Returns the distance of the closest centroid for each centroid
        that has another centroid in his range."""

        nearest_distances = self.get_nearest_neighbours(
            distance_max=distance_max,
            num_neighbours_max=num_neighbours_max,
        )
        return nearest_distances[nearest_distances != np.inf]
