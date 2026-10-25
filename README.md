3D Nucleus Segmentation
=========================

Local development
-----------------
Clone this repo:
```bash
git clone https://github.com/Koot5958/3d-nucleus-segmentation.git
cd 3d-nucleus-segmentation
```

Install the package and its the required dependencies:
```bash
python -m venv venv
source venv/bin/activate
# For Windows (PowerShell): .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Generate the .exe file:
```
python -m PyInstaller --clean --noconfirm --onedir --console --paths .\src --name NucleusSegmentation --icon .\app.ico --add-data ".\app.ico;." --collect-all napari --collect-all napari_svg --collect-all napari_builtins --collect-all napari_resources --collect-all vispy .\app_runner.py
```