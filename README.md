3D Nucleus Segmentation
=========================

Local development
-----------------
Clone this repo:
```bash
git clone https://git.ias.u-psud.fr/majis_sgs/quick-look/majis-ql-geometry
cd majis-ql-geometry
```

Install the package and its the required dependencies:
```bash
python -m venv venv
source venv/bin/activate
# For Windows (PowerShell): venv\Scripts\Activate.ps1
python -m pip install -e .[dev] --extra-index-url https://repositories.forge.ias.u-psud.fr/repository/pipy-ias/simple
```

Build the documentation
-----------------------
```bash
jupyter-book build docs/
```
The documentation can be find here: https://majis_sgs.io.ias.u-psud.fr/quick-look/majis-ql-geometry