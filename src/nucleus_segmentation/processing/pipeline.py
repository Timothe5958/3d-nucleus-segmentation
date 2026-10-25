from dataclasses import dataclass

from ..outputs_saver import OutputSaver
from . import post_processing, pre_processing, segmentation


@dataclass
class ProcessingOptions:
    gaussian_ksize: int = 2
    cube_size: int = 60
    alpha: float = 0.3
    sigma: int = 8
    min_cell_size: int = 1000


def process_observation(observation, options, progress_callback=None):
    def report_step(step_name):
        if progress_callback is not None:
            progress_callback(
                'step',
                observation.path.name,
                step_name,
            )

    results = {'raw_data': observation.get_raw_data()}

    def run_step(data, step_name, func, **kwargs):
        """Run any step of the pipeline."""
        report_step(step_name)
        return func(data, **kwargs)

    results['denoised_data'] = run_step(
        results['raw_data'],
        'denoising',
        pre_processing.gaussian_denoise,
        ksize=options.gaussian_ksize,
    )

    results['cropped_data'] = run_step(
        results['denoised_data'],
        'cropping',
        pre_processing.crop_background,
    )

    results['resampled_data'] = run_step(
        results['cropped_data'],
        'resampling',
        pre_processing.resample_isotropic,
        voxel_sizes=observation.get_voxel_dims(),
    )

    results['normalized_data'] = run_step(
        results['resampled_data'],
        'normalizing',
        pre_processing.normalize_intensity_shift_method,
        cube_size=options.cube_size,
        sigma=options.sigma,
        alpha=options.alpha,
    )

    results['segmented_data'] = run_step(
        results['normalized_data'],
        'segmentation',
        segmentation.binarization_multiotsu,
        classes=3,
    )

    results['segmented_cleaned_data'] = run_step(
        results['segmented_data'],
        'cleanup',
        post_processing.remove_small_artefacts,
        max_size=options.min_cell_size,
    )

    results['labelled_data'] = run_step(
        results['segmented_cleaned_data'],
        'labeling',
        post_processing.get_labelled_cells,
    )

    return results


def process_observations( # noqa : PLR0917, PLR0913
    observations,
    processing_options,
    output_options,
    output_folder,
    log=False,
    progress_callback=None,
    save_dispatcher=None,
):

    for observation in observations:
        if log:
            print(f'Processing {observation.path.name}...')

        # Compute the results in the second thread (current one)
        pipeline_results = process_observation(
            observation,
            processing_options,
            progress_callback=progress_callback,
        )

        output_manager = OutputSaver(
            observation,
            pipeline_results,
            output_folder,
            output_options,
        )

        # Save pipeline 3d view screenshots in the main thread (Napari viewer requirement)
        if save_dispatcher is not None:
            save_dispatcher(
                output_manager.save_outputs,
                progress_callback=progress_callback,
            )

        if progress_callback is not None:
            progress_callback(
                'observation_done',
                observation.path.name,
                '',
            )
