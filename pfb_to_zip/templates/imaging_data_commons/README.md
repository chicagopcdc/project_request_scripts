https://portal.imaging.datacommons.cancer.gov/

# Download instructions
- `cd src`
- make sure you have python 3.10 or greater 
	- `python -m venv env`
	- `source env/bin/activate`
	- `pip install --upgrade pip`
	- `pip install poetry`
	- `poetry install`
	- edit the `patient_ids` list with the IDs you want to download
	- `python main.py`
- more information about the script and output here: 
	- https://discourse.canceridc.dev/t/creating-cohort-in-portal-from-a-list-of-patientids/747/6
	- https://idc-index.readthedocs.io/en/latest/column_descriptions.html#index
