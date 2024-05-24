import pandas as pd
import csv
import json
import os
import datetime
# import openpyxl

# OUTPUT CSV MUST BE IN THE FOLLOWING FORM
# Part Number | Region | Currency | Description | List Price | Unit of Measurement | Order Min

# Part Number           :   str
# Region                :   Australia|Canada|China|Europe|United States|Asia
# Currency              :   AUD||CHF|CNY|DKK|EUR|GBP|NOK|SEK|USD    = ! WARNING:CDN NOT INCLUDED is written as CAD instead
# Description           :   str
# List Price            :   float
# Unit of Measurement   :   EA|FT|MT
# Order Min             :   int

def csv_read(csv_name):

    rows = []

    with open(csv_name, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows

# Receives sheetname, data structure as dictionary, TODO: Terminals, Summary
# Generates XL sheet
def excel_write(sheetname, data, writer):
    df = pd.DataFrame(data[1::][:], columns = data[0][:])
    df.to_excel(writer, sheet_name = sheetname, index = False)

def lpsd_pricingdata_location():
    # determine proper folder location in Downloads
    folder_location = "C:\\Users\\e1176752\\Downloads\\"
    folder_name = datetime.datetime.now().strftime("%Y-%m-%d")

    directory_name = folder_location + folder_name
    if  os.path.exists(directory_name):
        print("Directory {} found!".format(directory_name))
        return(directory_name + "\\PricingData.csv")
    else:
        try:
            print("Looking for folder with name {} in Downloads folder".format(folder_name))
            found = []
            for dirnames in os.listdir(folder_location):
                if folder_name in dirnames:
                    print("Found folder {}".format(dirnames))
                    found.append(dirnames)
            for number, folder in enumerate(found,1):
                print(number, "->", folder)
            while True:
                try:
                    userSelect = int(input("> "))
                    if 0 < userSelect <= len(found):
                        break
                    raise ValueError("Selection out of range")
                except ValueError as ve:
                        print(ve)
            print(f'{found[userSelect - 1]} selected')
            return(folder_location + found[userSelect-1] + "\\PricingData.csv")
        except:
            raise ValueError("Error: Pricing data was not found in the directory")
        
def get_newpricingdata():
    files = []

    folder_location = "C:\\Users\\E1176752\\OneDrive - nVent Management Company\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\PRICING\\"
    for filenames in os.listdir(folder_location):
        files.append(filenames)

    df1 = pd.read_excel(folder_location + files[0])
    df2 = pd.read_excel(folder_location + files[0],sheet_name=1)
    
    while df1.shape[1] != df2.shape[1]:
        if df1.shape[1] > df2.shape[1]:
            df1.drop(columns=df1.columns[-1], axis = 1, inplace = True)
        else:
            df2.drop(columns=df2.columns[-1], axis = 1, inplace = True)

    df_f = pd.concat([df1, df2], axis = 0)
    print("Read data from {}".format(files[0]))
    df3 = pd.read_excel(folder_location + files[1])
    while df_f.shape[1] != df3.shape[1]:
        df3.drop(columns=df3.columns[-1], axis = 1, inplace = True)

    print("Read data from {}".format(files[1]))
    df3.set_index('Part Number', inplace=True, drop=True)

    df4 = pd.concat([df_f, df3], axis = 0)
    df4.set_index('Part Number', inplace=True, drop=True)

    #print(df4.size)
    return(df4)

# Pull data after backup_lpsd.py has been ran
# Pricing data is stored in Downloads as a .csv file and will need to be uploaded in this format
LPSD_PricingData_CSV = csv_read(lpsd_pricingdata_location())
data = get_newpricingdata()

final_pricing = []
final_pricing.append(LPSD_PricingData_CSV[0][:])
print("Updating {} parts on csv file with {} parts from pricing".format(len(LPSD_PricingData_CSV), data.size))
print(len(LPSD_PricingData_CSV))
for k in range(1,len(LPSD_PricingData_CSV)):
    #print("Looking for part # {}".format(LPSD_PricingData_CSV[0][k][0]))
    try:
        current_data = data.loc[LPSD_PricingData_CSV[k][0]]

        currency = current_data['Currency'].to_numpy()
        currency[currency == "CDN"] = "CAD" # replace CDN with CAD to align on one currency definition
        
        list_price = current_data['List Price'].to_numpy()

        region = current_data['Region'].to_numpy()

        l = 0
        for j in currency:
            if j == LPSD_PricingData_CSV[k][2] and region[l] == LPSD_PricingData_CSV[k][1]:
                final_pricing.append(LPSD_PricingData_CSV[k][:])
                #print("Updating {} to {} on part {}".format(final_pricing[-1][4], list_price[l], LPSD_PricingData_CSV[0][k][0]))
                final_pricing[-1][4] = list_price[l]
                break
            if j == currency[-1]:
                #print("currency not found for {}".format(LPSD_PricingData_CSV[0][k][0]))
                final_pricing.append(LPSD_PricingData_CSV[k][:])
            l = l + 1

    except:
        #print("Could not find part # {}".format(LPSD_PricingData_CSV[0][k][0]))
        final_pricing.append(LPSD_PricingData_CSV[k][:])

#TODO: Change pathing to local pathing for scaleability
folder_location = "C:\\Users\\E1176752\\OneDrive - nVent Management Company\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\PRICING\\"
path = folder_location + "PricingData.xlsx"

writer = pd.ExcelWriter(path, engine = 'xlsxwriter')

excel_write("pricing", final_pricing, writer)

writer.close()
