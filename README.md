KrishiMitra

This repository contains the application source for the Plant Disease Recognition project. Large datasets, trained model binaries, virtual environments and credential files are intentionally excluded from this repo.

Included files:
- `app.py`
- `main.py`
- `download_script.py`
- `test_api.py`
- `requirements.txt`
- `.gitignore`

Excluded (NOT in repo):
- `venv/`, `venv_tf/`
- `New Plant Diseases Dataset(Augmented)/` (dataset and trained models)
- `firebase_credentials.json` (secrets)

To run locally:
1. Create a Python 3.11 virtualenv (recommended for TensorFlow compatibility).
2. Activate venv and install dependencies: `python -m pip install -r requirements.txt`.
3. Run `streamlit run main.py` or `python app.py` for the Flask API.
