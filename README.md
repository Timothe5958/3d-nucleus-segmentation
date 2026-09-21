# 3D Nucleus Segmentation

## Local development

Clone this repository:

git clone https://github.com/Koot5958/3d-nucleus-segmentation.git
cd 3d-nucleus-segmentation

Create and activate a virtual environment:

### Windows (PowerShell)

python -m venv .venv
.venv\Scripts\Activate.ps1

### Linux / macOS

python -m venv .venv
source .venv/bin/activate

Install the package and its development dependencies:

python -m pip install -e ".[dev]"

## Development

Run the linter:

ruff check .

Run the tests:

pytest

## Documentation

Documentation will be added here as the project develops.