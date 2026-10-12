from pathlib import Path

from .visualization import save_projected_view


class OutputManager:
    def __init__(self, output_folder):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def save_outputs(self, results, options, observation):
        observation_folder = self.output_folder / observation.path.stem
        observation_folder.mkdir(parents=True, exist_ok=True)

        outputs = {
            'raw': options.save_raw,
            'resampled': options.save_resampled,
            'denoised': options.save_denoised,
            'cropped': options.save_cropped,
            'normalized': options.save_normalized,
            'segmented': options.save_segmented,
            'segmented_clean': options.save_segmented_clean,
            'labelled': options.save_labelled,
        }

        for name, should_save in outputs.items():
            if should_save:
                save_projected_view(
                    results[name],
                    observation_folder / (name + '.png'),
                )
