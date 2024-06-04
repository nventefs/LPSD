from pathlib import Path
import os
import datetime

# Selector for .json file names
def json_filename(type, test_case):
    cvm_tc = {
        1: "CVM Test Case 1 metric_CVMResults.json",
        2: "CVM Test Case 2_CVMResults.json",
        3: "CVM Test Case 3 Rev B_CVMResults.json",
        4: "CVM Test Case 4_CVMResults.json",
        5: "CVM Test Case 5_CVMResults.json",
        6: "CVM Test Case 6 Rev F_CVMResults.json",
        7: "CVM Test Case 7_CVMResults.json",
    }
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

    match (type):
        case "CVM":
            return cvm_tc.get(test_case)
        case "S1000":
            return s1000_tc.get(test_case)
        
# Selector for names of test cases based on their type
def string(type, test_case):
    cvm_tc = {
        1: "CVM Test Case 1 metric",
        2: "CVM Test Case 2",
        3: "CVM Test Case 3 Rev B",
        4: "CVM Test Case 4",
        5: "CVM Test Case 5",
        6: "CVM Test Case 6 Rev F",
        7: "CVM Test Case 7"
    }
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

    match (type):
        case "CVM":
            return cvm_tc.get(test_case)
        case "S1000":
            return s1000_tc.get(test_case)
        
# Generates a folder based on the given type and test case and checks to see if a file for the 
#   specific test case does or does not exist. If it does, it provides the option to end the 
#   function or delete the file
def folder_location(type, test_case = None):

    # Generate a folder within archive/s1000/json for the current test case
    #Get directory of //LPSD
    root_dir = Path(__file__).resolve().parent.parent.parent

    #Add the rest of the path to the file, more cases for the type variable can be added to easily support more situations
    match (type):
        case "S1000 TEST":
            file_directory = root_dir / "Archive" / "S1000" / "JSON" / datetime.datetime.now().strftime("%Y-%m-%d")
            if test_case == None:
                return (file_directory)
            file_path = file_directory / json_filename ("S1000", test_case)
        case "S1000 OUTPUT":
            file_directory = root_dir / "Archive" / "S1000" / "Results"
            file_path = file_directory / (datetime.datetime.now().strftime("%Y-%m-%d") + ".csv")
        case "S1000 PARAMS":
            file_directory = root_dir / "Archive" / "S1000"
            return (file_directory)
        case "CVM":
            file_directory = root_dir / "JSON" / datetime.datetime.now().strftime("%Y-%m-%d")
            file_path = file_directory / json_filename ("CVM", test_case)

    #make directory if it does not already exist
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)
        print(f"Directory '{file_directory}' created successfully.")
        return(file_directory)
    #if the file already exists, present user with option to replace file or quit
    else:
        print(f"Directory '{file_directory}' already exists")
        
        if os.path.isfile(file_path):
            print(str(file_path) + "  exists!")
            x = input("\nContinue to use this file (yes/no)? If yes, the current file will be " + '\033[31m' + "overwritten. " + '\033[0m') 
            if(x.lower() == "no"):
                return
            elif(x.lower() == "yes"):
                os.remove(file_path)
                return(file_directory)
            else:
                print("Input not recognized.")
        else:
            return(file_directory)