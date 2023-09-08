import pandas as pd
import csv
import json
import os
import datetime

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
        return rows, len(rows)

def get_lpsd_pricingdata():
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

    folder_location = "C:\\Users\\e1176752\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\PRICING\\"
    for filenames in os.listdir(folder_location):
        files.append(filenames)

    df1 = pd.read_excel(folder_location + files[0])
    df2 = pd.read_excel(folder_location + files[0],sheet_name=1)
    
    while df1.shape[1] != df2.shape[1]:
        print("df1 shape: {}, df2 shape: {}".format(df1.shape, df2.shape))
        if df1.shape[1] > df2.shape[1]:
            df1.drop(columns=df1.columns[-1], axis = 1, inplace = True)
        else:
            df2.drop(columns=df2.columns[-1], axis = 1, inplace = True)

    df_f = pd.concat([df1, df2], axis = 0)
    
    df3 = pd.read_excel(folder_location + files[1])
    while df_f.shape[1] != df3.shape[1]:
        print("df1 shape: {}, df2 shape: {}".format(df_f.shape, df3.shape))
        df3.drop(columns=df3.columns[-1], axis = 1, inplace = True)

    print(df3)


"""
# Load in existing LPSD data from backup
lpsd_pricing = csv_read(get_lpsd_pricingdata())

df_lpsd = pd.DataFrame(lpsd_pricing[0][1:len(lpsd_pricing[0])])
df_lpsd.columns = lpsd_pricing[0][0]

"""
get_newpricingdata()