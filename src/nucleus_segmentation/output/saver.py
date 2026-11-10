from dataclasses import replace
from datetime import datetime
from pathlib import Path

from ..analysis import (
    MeasurementOptions,
    NucleiMeasurements,
    save_boxplot_violin,
    save_centroids_3d_view,
    save_centroids_density,
    save_centroids_distrib,
    save_centroids_neighbours_distrib,
    save_histogram,
    save_nuclei_axis_lengths_plot,
)
from ..figures_3d import ViewConfig, save_image_view
from .options import OUTPUT_OPTIONS

UNIT_DEFINITIONS = {
    'Elongation': 'Measure how stretched or elongated the nucleus is. Formula : major axis / minor axis',
    'Equivalent diameter': 'Diameter of a sphere that has the same volume as the nucleus.',
    'Sphericity': 'Measure how closely the nucleus resembles a perfect sphere. Formula : (π^(1/3) × (6V)^(2/3)) / A (where A is the surface and V the volume)',
    'Centroid': 'Geometric center of the nucleus, calculated as the mean position of all its voxels.',
    'Major (resp. minor) axis': 'Length of the longest (resp. shortest) principal axis of the equivalent ellipsoid.',
}


class OutputSaver:
    def __init__(self, observation, pipeline_results, output_config):
        self.output_folder = Path(output_config.folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.observation = observation
        self.pipeline_results = pipeline_results
        self.output_options = output_config.options
        self.start_date = datetime.now().strftime('%Y%m%d_%H%M%S')

    def send_callback(self, progress_callback, title):
        if progress_callback is not None:
            progress_callback(
                'step',
                self.observation.path.name,
                f'Sauvegarde : {title}',
            )

    def get_dir_name(self, sub_dir):
        folder = self.output_folder / (self.observation.name + '_' + self.start_date) / sub_dir
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
            save_boxplot_violin(
                measurements.volumes,
                output_folder=folder,
                title='volumes boxplot',
                labels=[None, 'Volume (µm³)'],
                metadata=measurements.metadata,
            )
            self.send_callback(progress_callback, 'volumes boxplot')

        if self.output_options['Boxplots']['elongations']:
            save_boxplot_violin(
                measurements.elongations,
                output_folder=folder,
                title='elongations boxplot',
                labels=[None, 'Elongation'],
                metadata=replace(
                    measurements.metadata,
                    definition=('Elongation', UNIT_DEFINITIONS['Elongation']),
                ),
            )
            self.send_callback(progress_callback, 'elongations boxplot')

        if self.output_options['Boxplots']['sphericities']:
            save_boxplot_violin(
                measurements.sphericities,
                output_folder=folder,
                title='sphericities boxplot',
                labels=[None, 'Sphericity'],
                metadata=replace(
                    measurements.metadata,
                    definition=('Sphericity', UNIT_DEFINITIONS['Sphericity']),
                ),
            )
            self.send_callback(progress_callback, 'sphericities boxplot')

        if self.output_options['Boxplots']['equivalent_diameters']:
            save_boxplot_violin(
                measurements.equivalent_diameters,
                output_folder=folder,
                title='equivalent diameter boxplot',
                labels=[None, 'Equivalent Diameter (µm)'],
                metadata=replace(
                    measurements.metadata,
                    definition=('Equivalent diameter', UNIT_DEFINITIONS['Equivalent diameter']),
                ),
            )
            self.send_callback(progress_callback, 'equivalent diameter boxplot')

        if self.output_options['Boxplots']['distance_closest_neighbour']:
            save_boxplot_violin(
                measurements.get_nearest_distances(),
                output_folder=folder,
                title='distance to closest neighbor',
                labels=[None, 'Distance to Closest Neighbor (µm)'],
                metadata=measurements.metadata,
            )
            self.send_callback(progress_callback, 'distance to closest neighbor')

    def save_histograms(self, measurements, progress_callback=None):
        folder = self.get_dir_name('Histograms')

        if self.output_options['Histograms']['volumes']:
            save_histogram(
                measurements.volumes,
                output_folder=folder,
                title='volumes histogram',
                labels=['Volume (µm³)', 'Number of nuclei'],
                metadata=measurements.metadata,
            )
            self.send_callback(progress_callback, 'volumes histogram')

        if self.output_options['Histograms']['centroid_density']:
            save_centroids_density(
                measurements,
                output_folder=folder,
                title='nuclei centroid density',
                metadata=replace(
                    measurements.metadata,
                    definition=('Centroid', UNIT_DEFINITIONS['Centroid']),
                ),
            )
            self.send_callback(progress_callback, 'nuclei centroid density')

        if self.output_options['Histograms']['elongations']:
            save_histogram(
                measurements.elongations,
                output_folder=folder,
                title='elongations histogram',
                labels=['Elongation', 'Number of nuclei'],
                metadata=replace(
                    measurements.metadata,
                    definition=('Elongation', UNIT_DEFINITIONS['Elongation']),
                ),
            )
            self.send_callback(progress_callback, 'nuclei centroid density')

        if self.output_options['Histograms']['sphericities']:
            save_histogram(
                measurements.sphericities,
                output_folder=folder,
                title='sphericities histogram',
                labels=['Sphericity', 'Number of nuclei'],
                metadata=replace(
                    measurements.metadata,
                    definition=('Sphericity', UNIT_DEFINITIONS['Sphericity']),
                ),
            )
            self.send_callback(progress_callback, 'sphericities histogram')

        if self.output_options['Histograms']['equivalent_diameters']:
            save_histogram(
                measurements.equivalent_diameters,
                output_folder=folder,
                title='equivalent diameters histogram',
                labels=['Equivalent diameter (µm)', 'Number of nuclei'],
                metadata=replace(
                    measurements.metadata,
                    definition=('Equivalent diameter', UNIT_DEFINITIONS['Equivalent diameter']),
                ),
            )
            self.send_callback(progress_callback, 'equivalent diameters histogram')

        if self.output_options['Histograms']['distance_closest_neighbour']:
            save_histogram(
                measurements.get_nearest_distances(),
                output_folder=folder,
                title='distance to closest neighbour histogram',
                labels=['Distance to closest neighbour (µm)', 'Number of nuclei'],
                metadata=measurements.metadata,
            )
            self.send_callback(progress_callback, 'distance to closest neighbour histogram')

    def save_points_cloud(self, measurements, progress_callback=None):
        folder = self.get_dir_name('Points cloud')

        if self.output_options['Points cloud']['centroids_position_3d_view']:
            save_centroids_3d_view(
                measurements,
                output_folder=folder,
                title='nuclei centroid 3d view',
                metadata=replace(
                    measurements.metadata,
                    definition=('Centroid', UNIT_DEFINITIONS['Centroid']),
                ),
            )
            self.send_callback(progress_callback, 'nuclei centroid 3d view')

        if self.output_options['Points cloud']['nuclei_axis_lengths']:
            save_nuclei_axis_lengths_plot(
                measurements,
                output_folder=folder,
                title='axis lengths',
                metadata=replace(
                    measurements.metadata,
                    definition=('Major (resp. minor) axis', UNIT_DEFINITIONS['Major (resp. minor) axis']),
                ),
            )
            self.send_callback(progress_callback, 'axis lengths')

        if self.output_options['Points cloud']['centroids_distribution']:
            save_centroids_distrib(
                measurements,
                output_folder=folder,
                title='nuclei centroid distribution',
                metadata=replace(
                    measurements.metadata,
                    definition=('Centroid', UNIT_DEFINITIONS['Centroid']),
                ),
            )
            self.send_callback(progress_callback, 'nuclei centroid distribution')

        if self.output_options['Points cloud']['neighbours_distribution']:
            save_centroids_neighbours_distrib(
                measurements,
                output_folder=folder,
                title='nuclei centroid neighbours distribution',
                metadata=replace(
                    measurements.metadata,
                    definition=('Centroid', UNIT_DEFINITIONS['Centroid']),
                ),
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
        options = MeasurementOptions()
        measurements = NucleiMeasurements(self.pipeline_results['labelled_data'], self.observation, options)

        self.save_3d_views(progress_callback)
        self.save_boxplots(measurements, progress_callback)
        self.save_histograms(measurements, progress_callback)
        self.save_points_cloud(measurements, progress_callback)
        self.save_pipeline_3d_views(progress_callback)
