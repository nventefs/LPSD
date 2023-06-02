from Automation import backup_lpsd
from Automation import get_json
from Multiplicative import multiplicative_calculate
from Reductive import reductive_calculate

import pandas as pd
import xlsxwriter

# Receives sheetname, data structure as dictionary, type: Reductive, Multiplicative, Terminals
# Generates XL sheet
def excel_write(sheetname, data, writer, type):
    df = pd.DataFrame(data)
    if(type == "multiplicative"):
          df.columns = ["POI", "xl_x", "xl_y", "xl_z", "json_x", "json_y", "json_z", "GUID", "xl_multi", "json_multi", "vs_multi", "eq3_val", "eq3_letter", "eq4_val", "eq4_letter", "eq5_val", "eq5_letter"]
    if(type == "reductive"):
        df.columns = ["POI", "xl_x", "xl_y", "xl_z", "json_x", "json_y", "json_z", "GUID", "mp_GUID", "xl_reduc", "json_reduc", "vs_reduc"]
    df.to_excel(writer, sheet_name = sheetname, index = False)

test_cases = range(1,8)
reduc = {}
multi = {}
path = r"C:\Users\e1176752\Documents\VSCode\Projects\LPSD\LPSD\test.xlsx"
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')

backup_lpsd.backup_lpsd()

for k in test_cases:
    get_json.get_json(k)

for k in test_cases:

    # Multiplicative calculations and added to excel workbook
    multi[k] = multiplicative_calculate.calc_multi(k)
    sheetname = "TC" + str(k) + "_Multi"
    excel_write(sheetname, multi[k], writer, "multiplicative")

    # Reductive calculations and added to excel workbook
    reduc[k] = reductive_calculate.calc_reduc(k)
    sheetname = "TC" + str(k) + "_Reduc"
    excel_write(sheetname, reduc[k], writer, "reductive")


writer.save()
