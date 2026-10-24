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

    raw_data = observation.get_raw_data()

    pipeline_results = {'raw_data': raw_data}

    report_step('denoising')
    pipeline_results['denoised_data'] = pre_processing.gaussian_denoise(
        raw_data,
        ksize=options.gaussian_ksize,
    )

    report_step('cropping')
    pipeline_results['cropped_data'] = pre_processing.crop_background(
        pipeline_results['denoised_data'],
    )

    report_step('resampling')
    pipeline_results['resampled_data'] = pre_processing.resample_isotropic(
        pipeline_results['cropped_data'],
        observation.get_voxel_dims(),
    )

    report_step('normalizing')
    pipeline_results['normalized_data'] = pre_processing.normalize_intensity_shift_method(
        pipeline_results['resampled_data'],
        cube_size=options.cube_size,
        sigma=options.sigma,
        alpha=options.alpha,
    )

    report_step('segmentation')
    pipeline_results['segmented_data'] = segmentation.binarization_multiotsu(
        pipeline_results['normalized_data'],
        classes=3,
    )

    report_step('cleanup')
    pipeline_results['segmented_cleaned_data'] = post_processing.remove_small_artefacts(
        pipeline_results['segmented_data'],
        max_size=options.min_cell_size,
    )

    report_step('labeling')
    pipeline_results['labelled_data'] = post_processing.get_labelled_cells(pipeline_results['segmented_cleaned_data'])

    return pipeline_results


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
