from dataclasses import dataclass

from . import post_processing, pre_processing, segmentation


@dataclass
class ProcessingOptions:
    gaussian_ksize: int = 2
    cube_size: int = 60
    alpha: float = 0.3
    sigma: int = 8
    min_cell_size: int = 1000


def process_observation(observation, options, progress_callback):
    def report_step(step_name):
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
