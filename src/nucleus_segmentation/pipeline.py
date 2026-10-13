from dataclasses import dataclass

from . import post_processing, pre_processing, segmentation
from .output_manager import OutputManager


@dataclass
class ProcessingOptions:
    gaussian_ksize: int = 2
    cube_size: int = 60
    alpha: float = 0.3
    sigma: int = 8
    min_cell_size: int = 1000


def process_observation(observation, options, log=False, reduction=0):
    if reduction == 0:
        raw_data = observation.raw_data
    else:
        raw_data = observation.raw_data[::reduction, ::reduction, ::reduction]

    if log:
        print('resampling...')
    resampled_data = pre_processing.resample_isotropic(
        raw_data,
        observation.get_voxels_size(),
    )

    if log:
        print('denoising...')
    denoised_data = pre_processing.gaussian_denoise(
        resampled_data,
        ksize=options.gaussian_ksize,
    )

    if log:
        print('cropping...')
    cropped_data = pre_processing.crop_background(
        denoised_data,
    )

    if log:
        print('normalizing data...')
    normalized_data = pre_processing.normalize_intensity_shift_method(
        cropped_data,
        cube_size=options.cube_size,
        sigma=options.sigma,
        alpha=options.alpha,
    )

    if log:
        print('segmentation...')
    segmented_data = segmentation.binarization_multiotsu(
        normalized_data,
        classes=3,
    )

    if log:
        print('cleanup process...')
    segmented_clean_data = post_processing.remove_small_artefacts(
        segmented_data,
        max_size=options.min_cell_size,
    )

    if log:
        print('labeling...')
    labelled_data = post_processing.get_labelled_cells(segmented_clean_data)

    return {
        'raw': raw_data,
        'resampled': resampled_data,
        'denoised': denoised_data,
        'cropped': cropped_data,
        'normalized': normalized_data,
        'segmented': segmented_data,
        'segmented_clean': segmented_clean_data,
        'labelled': labelled_data,
    }


def process_observations( # noqa : PLR0917, PLR0913
    observations,
    processing_options,
    output_options,
    output_folder,
    log=False,
    reduction=0,
):
    output_manager = OutputManager(output_folder)

    for observation in observations:
        if log:
            print(f'Processing {observation.path.name}...')

        results = process_observation(
            observation,
            processing_options,
            log=log,
            reduction=reduction,
        )

        output_manager.save_outputs(
            results,
            output_options,
            observation,
        )
