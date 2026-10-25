from datetime import datetime
from pathlib import Path

from .analysis import (
    NucleiMeasurements,
    save_boxplot,
    save_centroids_3d_view,
    save_centroids_density,
    save_centroids_distrib,
    save_centroids_neighbours_distrib,
    save_histogram,
    save_nuclei_axis_lengths_plot,
)
from .output_options import OUTPUT_OPTIONS
from .visualization import ViewConfig, save_image_view


class OutputSaver:
    def __init__(self, observation, pipeline_results, output_folder, output_options):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.observation = observation
        self.pipeline_results = pipeline_results
        self.output_options = output_options
        self.start_date = datetime.now().strftime('%Y%m%d_%H%M%S')

    def send_callback(self, progress_callback, title):
        if progress_callback is not None:
            progress_callback(
                'step',
                self.observation.path.name,
                f'Sauvegarde : {title}',
            )

    def get_dir_name(self, sub_dir):
        folder = self.output_folder / (self.observation.path.stem + '_' + self.start_date) / sub_dir
        return folder

    def save_pipeline_3d_views(self, progress_callback=None):
        folder = self.get_dir_name('Pipeline (Expert only)')

        for name in OUTPUT_OPTIONS['Pipeline (Expert only)']:
            if self.output_options['Pipeline (Expert only)'][name]:

                kwargs = {}
                if 'labelled' in name:
                    kwargs['is_label'] = True
                    kwargs['cmap'] = 'cividis'

                elif 'segmented' in name:
                    kwargs['mode'] = 'iso'

                config = ViewConfig(
                    voxel_size=self.observation.get_resampled_voxel_size(),
                    camera_rotation=(90, 0, -90),
                    **kwargs,
                )
                save_image_view(
                    self.pipeline_results[name],
                    path=folder / (f'{name}.png'),
                    config=config,
                )

                self.send_callback(progress_callback, name.replace('_', ' '))

    def save_boxplots(self, measurements, progress_callback=None):
        folder = self.get_dir_name('Boxplots')

        if self.output_options['Boxplots']['volumes']:
            save_boxplot(
                measurements.volumes,
                output_folder=folder,
                title=f'{self.observation.name} - volumes boxplot',
                labels=[None, 'Volume (µm^3)'],
            )
            self.send_callback(progress_callback, 'volumes boxplot')

        if self.output_options['Boxplots']['elongations']:
            save_boxplot(
                measurements.elongations,
                output_folder=folder,
                title=f'{self.observation.name} - elongations boxplot',
                labels=[None, 'Elongation'],
            )
            self.send_callback(progress_callback, 'elongations boxplot')

        if self.output_options['Boxplots']['sphericities']:
            save_boxplot(
                measurements.sphericities,
                output_folder=folder,
                title=f'{self.observation.name} - sphericities boxplot',
                labels=[None, 'Sphericity'],
            )
            self.send_callback(progress_callback, 'sphericities boxplot')

        if self.output_options['Boxplots']['equivalent_diameters']:
            save_boxplot(
                measurements.equivalent_diameters,
                output_folder=folder,
                title=f'{self.observation.name} - equivalent diameter boxplot',
                labels=[None, 'Equivalent Diameter (µm)'],
            )
            self.send_callback(progress_callback, 'equivalent diameter boxplot')

        if self.output_options['Boxplots']['distance_closest_neighbour']:
            save_boxplot(
                measurements.get_nearest_distances(
                    distance_max=50,
                    num_neighbours_max=40,
                ),
                output_folder=folder,
                title=f'{self.observation.name} - distance to closest neighbor',
                labels=[None, 'Distance to Closest Neighbor (µm)'],
            )
            self.send_callback(progress_callback, 'distance to closest neighbor')

    def save_histograms(self, measurements, progress_callback=None):
        folder = self.get_dir_name('Histograms')

        if self.output_options['Histograms']['volumes']:
            save_histogram(
                measurements.volumes,
                output_folder=folder,
                title=f'{self.observation.name} - volumes histogram',
                labels=['Volume (µm^3)', 'Number of nuclei'],
            )
            self.send_callback(progress_callback, 'volumes histogram')

        if self.output_options['Histograms']['centroid_density']:
            save_centroids_density(
                measurements,
                bin_width=10,
                output_folder=folder,
                title=f'{self.observation.name} - nuclei centroid density',
            )
            self.send_callback(progress_callback, 'nuclei centroid density')

        if self.output_options['Histograms']['elongations']:
            save_histogram(
                measurements.elongations,
                output_folder=folder,
                title=f'{self.observation.name} - elongations histogram',
                labels=['Elongation', 'Number of nuclei'],
            )
            self.send_callback(progress_callback, 'nuclei centroid density')

        if self.output_options['Histograms']['sphericities']:
            save_histogram(
                measurements.sphericities,
                output_folder=folder,
                title=f'{self.observation.name} - sphericities histogram',
                labels=['Sphericity', 'Number of nuclei'],
            )
            self.send_callback(progress_callback, 'sphericities histogram')

        if self.output_options['Histograms']['equivalent_diameters']:
            save_histogram(
                measurements.equivalent_diameters,
                output_folder=folder,
                title=f'{self.observation.name} - equivalent diameters histogram',
                labels=['Equivalent diameter', 'Number of nuclei'],
            )
            self.send_callback(progress_callback, 'equivalent diameters histogram')

        if self.output_options['Histograms']['distance_closest_neighbour']:
            save_histogram(
                measurements.get_nearest_distances(
                    distance_max=50,
                    num_neighbours_max=40,
                ),
                output_folder=folder,
                title=f'{self.observation.name} - distance to closest neighbour histogram',
                labels=['Distance to closest neighbour', 'Number of nuclei'],
            )
            self.send_callback(progress_callback, 'distance to closest neighbour histogram')

    def save_points_cloud(self, measurements, progress_callback=None):
        folder = self.get_dir_name('Points cloud')

        if self.output_options['Points cloud']['centroids_position_3d_view']:
            save_centroids_3d_view(
                measurements,
                output_folder=folder,
                title=f'{self.observation.name} - nuclei centroid 3d view',
                distance_max=50,
                num_neighbours_max=40,
            )
            self.send_callback(progress_callback, 'nuclei centroid 3d view')

        if self.output_options['Points cloud']['nuclei_axis_lengths']:
            save_nuclei_axis_lengths_plot(
                measurements.major_axes,
                measurements.minor_axes,
                output_folder=folder,
                title=f'{self.observation.name} - axis lengths',
            )
            self.send_callback(progress_callback, 'axis lengths')

        if self.output_options['Points cloud']['centroids_distribution']:
            save_centroids_distrib(
                measurements,
                output_folder=folder,
                title=f'{self.observation.name} - nuclei centroid distribution',
            )
            self.send_callback(progress_callback, 'nuclei centroid distribution')

        if self.output_options['Points cloud']['neighbours_distribution']:
            save_centroids_neighbours_distrib(
                measurements,
                output_folder=folder,
                title=f'{self.observation.name} - nuclei centroid neighbours distribution',
                distance_max=50,
                num_neighbours_max=40,
            )
            self.send_callback(progress_callback, 'nuclei centroid neighbours distribution')

    def save_3d_views(self, progress_callback=None):
        folder = self.get_dir_name('3D views')

        if self.output_options['3D views']['raw']:
            config = ViewConfig(
                voxel_size=self.observation.get_resampled_voxel_size(),
                camera_rotation=(90, 0, -90),
            )
            save_image_view(
                self.pipeline_results['raw_data'],
                path=folder / 'raw_3d_view.png',
                config=config,
            )
            self.send_callback(progress_callback, 'raw 3d view')

        if self.output_options['3D views']['labelled']:
            config = ViewConfig(
                voxel_size=self.observation.get_resampled_voxel_size(),
                camera_rotation=(90, 0, -90),
            )
            save_image_view(
                self.pipeline_results['labelled_data'],
                path=folder / 'labelled_3d_view.png',
                config=config,
            )
            self.send_callback(progress_callback, 'labelled 3d view')


    def save_outputs(self, progress_callback=None):
        measurements = NucleiMeasurements(self.pipeline_results['labelled_data'], self.observation)

        self.save_3d_views(progress_callback)
        self.save_boxplots(measurements, progress_callback)
        self.save_histograms(measurements, progress_callback)
        self.save_points_cloud(measurements, progress_callback)
        self.save_pipeline_3d_views(progress_callback)
