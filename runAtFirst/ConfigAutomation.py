'''
Help me write a Python script:
Function: Read from the second sheet of sourceReqExcel_CRS and sourceReqExcel_SRS, read the second row (the second row is the header), the goal is to obtain the header name of each column and the corresponding column number, and store it as a JSON formatted file.
Input: sourceReqExcel_CRS = '../doc/2024_02_VW_CRS_Fault List.xls', sourceReqExcel_SRS = '.. /doc/doc/2024_SRS_AB12CN_FL_FaultList_VW_VCTC.xls.xls'
The targetConfigFilePath is set to ',,/FaultListHelperCFG.json'. 
Note: Multiple sourceReqExcel files may need to be read. 
For example, if the first column is ID, it should be stored as "ID_col: 1".
'''

#TODO: check duplicate column in CRS and SRS

import pandas as pd
import json

# define inputs and outputs
sourceReqExcel_CRS = 'input/CRS.xls'
sourceReqExcel_SRS = 'input/SRS_base.xls'
targetConfigFilePath = 'FaultListHelperCFG.json'

public_header_dict = {}

# read Excel and update header_dict
def read_excel_headers(file_path):
    # store colum name and its idx
    header_dict = {}
    df = pd.read_excel(file_path, sheet_name=1, header=1)  # read the second sheet，header is in the second row
    headers = df.columns.tolist()
    for index, header in enumerate(headers):
        header_dict[header] = index + 1  # idx starts from 1
    return header_dict

# read CRS and SRS
public_header_dict['CRS'] = read_excel_headers(sourceReqExcel_CRS)
public_header_dict['SRS'] = read_excel_headers(sourceReqExcel_SRS)

# dump to .json
with open(targetConfigFilePath, 'w', encoding='utf-8') as json_file:
    json.dump(public_header_dict, json_file, ensure_ascii=False, indent=4)

print(f"Header configuration saved to {targetConfigFilePath}")
