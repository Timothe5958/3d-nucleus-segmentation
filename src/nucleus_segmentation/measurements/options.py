from dataclasses import dataclass


@dataclass
class MeasurementOptions:
    neighbours_dist_max: int = 50
    neighbours_nb_max: int = 40
    centroids_density_bin_with: int = 15
