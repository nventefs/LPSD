from Automation import backup_lpsd
from Automation import get_json
from Multiplicative import multiplicative_calculate
from Reductive import reductive_calculate

import pandas as pd
import xlsxwriter

# Receives sheetname, data structure as dictionary, type: Reductive, Multiplicative, TODO: Terminals, Summary
# Generates XL sheet
def excel_write(sheetname, data, writer, type):
    df = pd.DataFrame(data)
    if(type == "multiplicative"):
          df.columns = ["POI", "xl_x", "xl_y", "xl_z", "json_x", "json_y", "json_z", "GUID", "xl_multi", "json_multi", "vs_multi", "eq3_val", "eq3_letter", "eq4_val", "eq4_letter", "eq5_val", "eq5_letter"]
    if(type == "reductive"):
        df.columns = ["POI", "xl_x", "xl_y", "xl_z", "json_x", "json_y", "json_z", "GUID", "mp_GUID", "xl_reduc", "json_reduc", "vs_reduc"]
    if(type == "multi_summary"):
        df.columns = ["TC1_Mutli", "TC2_Multi", "TC3_Mutli", "TC4_Multi", \
                    "TC5_Mutli", "TC6_Multi", "TC7_Mutli"]
    if(type == "reduc_summary"):
        df.columns = ["TC1_Reduc", "TC2_Reduc", "TC3_Reduc", "TC4_Reduc", \
                        "TC5_Reduc", "TC6_Reduc",  "TC7_Reduc"]
    df.to_excel(writer, sheet_name = sheetname, index = False)

# Pads checklist with padel value to allow for pandas dataframe
def pad_dict_list(dict_list, padel):
    lmax = 0
    for name in dict_list.keys():
        lmax = max(lmax, len(dict_list[name]))
    for name in dict_list.keys():
        ll = len(dict_list[name])
        if ll < lmax:
            dict_list[name] += [padel] * (lmax - ll)
    return dict_list


test_cases = range(1,8)
reduc = {}
multi = {}
reduc_summary = {}
multi_summary = {}
path = r"C:\Users\e1176752\Documents\VSCode\Projects\LPSD\LPSD\test.xlsx"
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
"""
backup_lpsd.backup_lpsd()

for k in test_cases:
    get_json.get_json(k)
"""
for k in test_cases:

    # Multiplicative calculations and added to excel workbook
    multi[k] = multiplicative_calculate.calc_multi(k)
    sheetname = "TC" + str(k) + "_Multi"
    excel_write(sheetname, multi[k], writer, "multiplicative")

    # Reductive calculations and added to excel workbook
    reduc[k] = reductive_calculate.calc_reduc(k)
    sheetname = "TC" + str(k) + "_Reduc"
    excel_write(sheetname, reduc[k], writer, "reductive")

for k in test_cases:
    reduc_summary[k] = reductive_calculate.check_reduc(reduc[k])
    multi_summary[k] = multiplicative_calculate.check_multi(multi[k])

reduc_summary_padded = pad_dict_list(reduc_summary, "N/A")
multi_summary_padded = pad_dict_list(multi_summary, "N/A")

sheetname = "rSummary"
excel_write(sheetname, reduc_summary_padded, writer, "reduc_summary")

sheetname = "mSummary"
excel_write(sheetname, multi_summary_padded, writer, "multi_summary")

writer.save()
