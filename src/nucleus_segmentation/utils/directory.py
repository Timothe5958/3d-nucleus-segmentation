from pathlib import Path


def create_dir(output_folder, title):
    output_path = Path(output_folder + title + '.png')
    output_path.parent.mkdir(parents=True, exist_ok=True)
