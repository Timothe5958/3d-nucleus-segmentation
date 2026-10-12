from dataclasses import dataclass


@dataclass
class OutputOptions:
    save_raw: bool = False
    save_resampled: bool = False
    save_denoised: bool = False
    save_cropped: bool = False
    save_normalized: bool = False
    save_segmented: bool = False
    save_segmented_clean: bool = False
    save_labelled: bool = False
