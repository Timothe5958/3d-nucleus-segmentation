from dataclasses import dataclass

from . import post_processing, pre_processing, segmentation


@dataclass
class ProcessingOptions:
    gaussian_ksize: int = 2
    sigma: int = 8
    min_cell_size: int = 1000


@dataclass
class NormalizationOptions:
    sigma: int = 10
    alpha: float = 1
    ref_th: float | None = None
    ref_var: float = 185
    cube_size: int = 60
    shift: bool = False


def process_observation(observation, options, progress_callback):
    def report_step(step_name):
        progress_callback(
            'step',
            observation.path.name,
            step_name,
        )

    results = {'raw_data': observation.get_raw_data()}

    def run_step(data, step_name, func, *args, **kwargs):
        """Run any step of the pipeline."""
        report_step(step_name)
        return func(data, *args, **kwargs)

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

    """results['resampled_data'] = run_step(
        results['cropped_data'],
        'resampling',
        pre_processing.resample_isotropic,
        voxel_sizes=observation.get_voxel_dims(),
    )"""
    results['resampled_data'] = results['cropped_data']

    results['normalized_data'] = run_step(
        results['resampled_data'],
        'normalizing',
        pre_processing.normalize_intensity_shift_method,
        options=NormalizationOptions(),
    )

    results['segmented_data'] = run_step(
        results['normalized_data'],
        'segmentation',
        segmentation.binarization_otsu,
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
        post_processing.split_agregates,
        data_raw=results['cropped_data'],
    )

    return results
