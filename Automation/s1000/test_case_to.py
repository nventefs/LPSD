from pathlib import Path
import os
import datetime
import time

# Selector for .json file names based on their test case
# "type" variable can be used to support other systems in the future like CVM
def json_filename(type, test_case):
    s1000_tc = {
        1: "S1000 QA TC1_ESEResults.json",
        2: "S1000 QA TC2_ESEResults.json",
        3: "S1000 QA TC3_ESEResults.json",
        4: "S1000 QA TC4_ESEResults.json",
        5: "S1000 QA TC5_ESEResults.json",
        6: "S1000 QA TC6_ESEResults.json",
        7: "S1000 QA TC7_ESEResults.json",
        8: "S1000 QA TC8_ESEResults.json",
        9: "S1000 QA TC9_ESEResults.json",
        10: "S1000 QA TC10_ESEResults.json",
        11: "S1000 QA TC17_ESEResults.json",
        12: "S1000 QA TC12_ESEResults.json",
        13: "S1000 QA TC18_ESEResults.json",
        14: "S1000 QA TC14_ESEResults.json",
        15: "S1000 QA TC15_ESEResults.json",
        16: "S1000 QA TC19_ESEResults.json",
    }
    s2000_half_tc = {
        1: "S2000 TC1 HALF.json",
        2: "S2000 TC2 HALF.json",
        3: "S2000 TC3 HALF.json",
        4: "S2000 TC4 HALF.json",
    }
    s2000_one_tc = {
        1: "S2000 TC1 ONE.json",
        2: "S2000 TC2 ONE.json",
        3: "S2000 TC3 ONE.json",
        4: "S2000 TC4 ONE.json",
    }
    s2000_old = {
        1: "RSM IEC L1 PARAPET TEST METRIC_RSResults.json",
        2: "RSM IEC L2 PARAPET TEST METRIC_RSResults.json",
        3: "RSM IEC L3 PARAPET TEST METRIC_RSResults.json",
        4: "RSM IEC L4 PARAPET TEST METRIC_RSResults.json",
    }

    match (type):
        case "S1000":
            return s1000_tc.get(test_case)
        case "S2000 HALF":
            return s2000_half_tc.get(test_case)
        case "S2000 ONE":
            return s2000_one_tc.get(test_case)
        case "S2000 OLD":
            return s2000_old.get(test_case)

        
# Selector for names of test cases based on their type
# "type" variable can be used to support other systems in the future like CVM
def name(type, test_case):
    s1000_tc = {
        1: "S1000 QA TC1",
        2: "S1000 QA TC2",
        3: "S1000 QA TC3",
        4: "S1000 QA TC4",
        5: "S1000 QA TC5",
        6: "S1000 QA TC6",
        7: "S1000 QA TC7",
        8: "S1000 QA TC8",
        9: "S1000 QA TC9",
        10: "S1000 QA TC10",
        11: "S1000 QA TC17",
        12: "S1000 QA TC12",
        13: "S1000 QA TC18",
        14: "S1000 QA TC14",
        15: "S1000 QA TC15",
        16: "S1000 QA TC19",
    }

    s2000_tc = {
        1: "RSM IEC L1 PARAPET TEST METRIC",
        2: "RSM IEC L2 PARAPET TEST METRIC",
        3: "RSM IEC L3 PARAPET TEST METRIC",
        4: "RSM IEC L4 PARAPET TEST METRIC",
    }

    match (type):
        case "S1000":
            return s1000_tc.get(test_case)
        case "S2000":
            return s2000_tc.get(test_case)
        
# Generates a folder based on the given type
# Checks to see if the folder exists, if it does, it returns the path
# if it does not exist, the generative option can greate the folder
def folder_path(type, generative=False):
    # Generate a folder within archive/s1000/json for the current test case
    #Get directory of //LPSD
    root_dir = Path(__file__).resolve().parent.parent.parent

    #Add the rest of the path to the file, more cases for the type variable can be added to easily support more situations
    match (type):
        case "S1000 TEST":
            return_path = root_dir / "Archive" / "S1000" / "JSON"/ datetime.datetime.now().strftime("%Y-%m-%d") 
        case "S1000 OUTPUT":
            return_path = root_dir / "Archive" / "S1000" / "Results"
        case "S1000 PARAMS" | "S1000 PROTECTEDPOINTS":
            return_path = root_dir / "Archive" / "S1000"
        case "S2000 TEST HALF" | "S2000 TEST ONE" | "S2000 TEST":
            return_path = root_dir / "Archive" / "S2000" / "JSON" / datetime.datetime.now().strftime("%Y-%m-%d")



    if not os.path.exists(return_path):
        # make directory if it does not already exist and return it
        if generative:
            os.makedirs(return_path)
            print(f"Directory '{return_path}' created successfully.")
            return(return_path)
        # or just warn user and return None
        else:
            print(f"{return_path} does not exist!")
            return None
        
    return return_path
    
# very similar to folder_path, but gets a file instead of a folder
# has a few more options including test case and removing.
# "removing" = True will remove a file and return its path so a new file can be created (or downloaded in the case of get_json)
def file_path (type, test_case = None, generative=False, removing=False):
    # get the folder path that the file is in, passing generative through
    folder = folder_path(type, generative)
    
    # More options for type can be added in the future
    match type:
        case "S1000 TEST":
            return_path = folder / json_filename ("S1000", test_case)
        case "S1000 OUTPUT":
            return_path = folder / (datetime.datetime.now().strftime("%Y-%m-%d") + ".csv")
        case "S1000 PARAMS":
            return_path = folder / "S1000 Parameters.csv"
        case "S1000 PROTECTEDPOINTS":
            return_path = folder / "point_protection_values.json"
        case "S2000 TEST HALF":
            return_path = folder / json_filename ("S2000 HALF", test_case)
        case "S2000 TEST ONE":
            return_path = folder / json_filename ("S2000 ONE", test_case)

    # if the path does not exist, and generative is true, create the file
    if not os.path.exists(return_path):
        if generative:
            f = open(return_path, "w")
            f.close()
            if not removing:
                print(f"Directory '{return_path}' created successfully.")
        else:
            print(f"{return_path} does not exist!")
            return None
    # if the path does exist and removing is true, remove the file
    if removing:
        os.remove(return_path)
        
    return return_path