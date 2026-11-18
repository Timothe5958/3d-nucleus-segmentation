import numpy as np
from scipy.spatial import cKDTree


class NucleiCollection:
    def __init__(self, nuclei, labelled_data, voxel_size_um, density_mask, options):
        self.nuclei = nuclei
        self.labelled_data = labelled_data
        self.voxel_size_um = voxel_size_um
        self.options = options
        self.density_mask = density_mask
        self.neighbours_distances = None

    def __len__(self):
        return len(self.nuclei)

    def __iter__(self):
        return iter(self.nuclei)

    def append(self, nucleus):
        self.nuclei.append(nucleus)

    @property
    def centroids(self):
        return np.array([nucleus.centroid for nucleus in self.nuclei])

    @property
    def volumes(self):
        return np.array([nucleus.volume for nucleus in self.nuclei])

    @property
    def minor_axes(self):
        return np.array([nucleus.minor_axis for nucleus in self.nuclei])

    @property
    def major_axes(self):
        return np.array([nucleus.major_axis for nucleus in self.nuclei])

    @property
    def elongations(self):
        return np.array([nucleus.elongation for nucleus in self.nuclei])

    @property
    def equivalent_diameters(self):
        return np.array([nucleus.equivalent_diameter for nucleus in self.nuclei])

    @property
    def sphericities(self):
        return np.array([nucleus.sphericity for nucleus in self.nuclei])

    def get_densities(self):
        bin_width = self.options.centroids_density_bin_with
        centroids = self.centroids

        max_height = (bin_width * np.max(centroids[:, 0])) // bin_width + 1
        bins = np.arange(np.min(centroids[:, 0]), max_height + bin_width, bin_width)

        nuclei_counts, bin_edges = np.histogram(centroids[:, 0], bins=bins)
        bin_centers = bin_edges[:-1] + (bin_width / 2)

        bin_volume = bin_width # --------- TO DO ---------

        densities_per_100um_cubes = nuclei_counts / (bin_volume * 1e-6)
        return densities_per_100um_cubes, bin_centers

    def _compute_neighbours(self):
        tree = cKDTree(self.centroids)

        distances, indices = tree.query(
            self.centroids,
            k=self.options.neighbours_nb_max + 1,
            distance_upper_bound=self.options.neighbours_dist_max,
        )

        self.neighbours_indices = indices[:, 1:]
        self.neighbours_distances = distances[:, 1:]
        self.neighbour_counts = np.sum(self.neighbours_distances != np.inf, axis=1)

    def get_neighbours_distances(self):
        # compute for the first time or compute again
        if self.neighbours_distances is None:
            self._compute_neighbours()

        return (
            self.neighbours_indices,
            self.neighbours_distances,
            self.neighbour_counts,
        )

    def get_nearest_neighbours(self):
        # compute for the first time or compute again if new distance max
        if self.neighbours_distances is None:
            self._compute_neighbours()

        return self.neighbours_distances[:, 0]

    def get_nearest_distances(self):
        """Returns the distance of the closest centroid for each centroid
        that has another centroid in his range."""

        nearest_distances = self.get_nearest_neighbours()
        return nearest_distances[nearest_distances != np.inf]
