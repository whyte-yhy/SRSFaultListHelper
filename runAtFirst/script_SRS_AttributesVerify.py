import pandas as pd
import re

# define inputs and outputs
sourceReqExcel_CRS = 'input/CRS.xls'
sourceReqExcel_SRS = 'input/SRS_base.xls'
updateScript_filepath = 'custlib/UpdateAttributes.py'

# read Excel and update header_dict
def read_excel_headers(file_path):
    df = pd.read_excel(file_path, sheet_name=1, header=1)  # read the second sheet，header is in the second row
    headers = df.columns.tolist()
    return headers

def read_script_attrs(file_path, pattern):
    tmp_attr_list = list()
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.find(pattern) != -1:
                tmp_attr_list.append(line[line.find(pattern):].split("'")[1])
    return tmp_attr_list


# read CRS and SRS
SRS_header_set = set(read_excel_headers(sourceReqExcel_SRS))
SRS_attr_set = set(read_script_attrs(updateScript_filepath, "attrName == '"))

CRS_header_set = set(read_excel_headers(sourceReqExcel_CRS))
CRS_attr_set = set(read_script_attrs(updateScript_filepath, "curDTC_crs.getAttr('"))

# output debug info
print(f"attr only in SRS (need enhance script): {SRS_header_set - SRS_attr_set}")
print(f"attr only in script (need add attr to SRS view):{SRS_attr_set - SRS_header_set}")
print()
print(f"attr only in CRS (need enhance script): {CRS_header_set - CRS_attr_set}")
print(f"attr only in script (need add attr to CRS view):{CRS_attr_set - CRS_header_set}")