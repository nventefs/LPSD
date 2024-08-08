from pathlib import Path
import os
import datetime

TODAYS_DATE_STRING = datetime.datetime.now().strftime("%Y-%m-%d") 

PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.parent
S1000_ARCHIVE_FOLDER = PROJECT_ROOT_DIR / "Archive" / "S1000"
S1000_CURRENT_JSON_FOLDER = S1000_ARCHIVE_FOLDER / "JSON" / TODAYS_DATE_STRING
S1000_RESULTS_FOLDER = S1000_ARCHIVE_FOLDER / "Results"
S1000_CURRENT_RESULTS_FILE = S1000_RESULTS_FOLDER / (TODAYS_DATE_STRING + ".csv")
S1000_RADIUS_PARAMETER_FILE = S1000_ARCHIVE_FOLDER / "S1000 Parameters.csv"
S1000_POINT_PROTECTION_PARAM_FILE = S1000_ARCHIVE_FOLDER / "point_protection_values.json"
S1000_INCORRECT_POINTS_FILE = S1000_RESULTS_FOLDER / (TODAYS_DATE_STRING + "_incorrect_guids.txt")

S2000_ARCHIVE_FOLDER = PROJECT_ROOT_DIR / "Archive" / "S2000"
S2000_CURRENT_JSON_FOLDER = S2000_ARCHIVE_FOLDER / "JSON" / TODAYS_DATE_STRING
S2000_POINT_PROTECTION_PARAM_FILE_HALF_METER = S2000_ARCHIVE_FOLDER / "point_protection_values_half_meter.json"
S2000_POINT_PROTECTION_PARAM_FILE_ONE_METER = S2000_ARCHIVE_FOLDER / "point_protection_values_one_meter.json"
S2000_RESULTS_FOLDER = S2000_ARCHIVE_FOLDER / "Results"
S2000_INCORRECT_POINTS_FILE = S2000_RESULTS_FOLDER / (TODAYS_DATE_STRING + ".txt")