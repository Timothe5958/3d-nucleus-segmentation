from datetime import datetime
from pathlib import Path

from .visualization import save_image_view, save_label_view


class OutputManager:
    def __init__(self, output_folder):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def save_outputs(self, results, options, observation):
        date = datetime.now().strftime('%Y%m%d_%H%M%S')
        observation_folder = self.output_folder / (observation.path.stem + '_' + date)
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
                if 'labelled' in name:
                    save_label_view(
                        results[name],
                        observation_folder / (name + '.png'),
                        cmap='cividis',
                    )
                elif 'segmented' in name:
                    save_image_view(
                        results[name],
                        observation_folder / (name + '.png'),
                        mode='iso',
                    )
                else:
                    save_image_view(
                        results[name],
                        observation_folder / (name + '.png'),
                    )
