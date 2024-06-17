# Selector for .json file names based on their test case
# "type" should be "S1000" for system 1000 or "S2000" for system 2000
def json_filename(type, test_case):
    # test cases for system 1000
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
    # test cases for system 2000
    s2000_tc = {
        1: "S2000 TC1.json",
        2: "S2000 TC2.json",
        3: "S2000 TC3.json",
        4: "S2000 TC4.json",
        5: "S2000 TC5.json",
        6: "S2000 TC6.json",
        7: "S2000 TC7.json",
        8: "S2000 TC8.json",
        9: "S2000 TC9.json",
        10: "S2000 TC10.json",
        11: "S2000 TC11.json",
        12: "S2000 TC12.json",
        13: "S2000 TC13.json",
        14: "S2000 TC14.json",
        15: "S2000 TC15.json",
        16: "S2000 TC16.json",
    }
    match (type):
        case "S1000":
            return s1000_tc.get(test_case)
        case "S2000":
            return s2000_tc.get(test_case)

        
# Selector for names of tests based on their type
# "type" should be "S1000" for system 1000 or "S2000" for system 2000
def name(type, test_case):
    # System 1000
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

    # System 2000
    s2000_tc = {
        1: "RSM IEC L1 PARAPET TEST METRIC",
        2: "RSM IEC L1 PARAPET TEST METRIC",
        3: "RSM IEC L2 PARAPET TEST METRIC",
        4: "RSM IEC L2 PARAPET TEST METRIC",
        5: "RSM IEC L3 PARAPET TEST METRIC",
        6: "RSM IEC L3 PARAPET TEST METRIC",
        7: "RSM IEC L4 PARAPET TEST METRIC",
        8: "RSM IEC L4 PARAPET TEST METRIC",
        9: "IEC L1 GABLE TEST METRIC",
        10: "IEC L1 GABLE TEST METRIC",
        11: "IEC L2 GABLE TEST METRIC",
        12: "IEC L2 GABLE TEST METRIC",
        13: "IEC L3 GABLE TEST METRIC",
        14: "IEC L3 GABLE TEST METRIC",
        15: "IEC L4 GABLE TEST METRIC",
        16: "IEC L4 GABLE TEST METRIC",
    }

    match (type):
        case "S1000":
            return s1000_tc.get(test_case)
        case "S2000":
            return s2000_tc.get(test_case)