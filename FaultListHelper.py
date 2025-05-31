###
## Mandatory: search "TODO:" and do all the needed configuration/implementation
###


import win32com.client
import os
import sys
import time


# ========external obj========
from lib.LoadCfg import configLoader
from lib.Util import log, util
from lib.Model import REQ, DTC, ExcelHelper
from custlib.UpdateAttributes import get_updated_srs_excel_cell_value, noValidResolveTime_list
# ========external obj end========

# ========#define========
getAtrCol = configLoader.getAttrColNum
remove_file = util.remove_file
close_excel_file = util.close_excel_file
getColNum = util.getColNum
error = log.Error
warning = log.Warning
result = log.Result
# ========#define end========

'''
TODO: Below need to be configured by every project
'''        
DemRbEventCategoryRef_DTC_Dict_Val_Key = {
    'NonErasableInternalFlt' : '0x925149',
    'ErasableInternalFlt' : '0x92511F',
}
DemRbEventCategoryRef_DTC_Dict_Key_Val = {
    '0x925149': 'NonErasableInternalFlt', #'Bosch Internal fault without FailSafe and Internal FailSafe faults with aging disable',
    '0x92511F': 'ErasableInternalFlt', #'Bosch Internal Failsafe fault with aging enable',
}

CRS_path = os.path.join(os.getcwd(), 'input/CRS.xls')
SRS_path = os.path.join(os.getcwd(), 'input/SRS_base.xls')

SRS_Updated_path = os.path.join(os.getcwd(), 'output/1_SRS_FaultList_updated.xls')
AdditionalDebugInfo_path = os.path.join(os.getcwd(), 'output/2_AdditionalDebugInfo.txt')

RelevantProject = 'D01'  # current RelevantProject
VariantsInSRS = 'P1x (ISU)'  # HW variants

xls_Format_code = 56

# just to remind if there are special DTCs
# TODO: Notice it when it is not NULL!!!!!
special_DTC_Dict = {
    'rb_edr_DataAreaFull_flt':'It is an internal fault, but it is described in CRS, so check the DTC number and other attributes',
    'rb_sqm_LowsidePowerstage':'These faults are remarked as ErasableInternal, but other attributes follow NonErasable in CA',                
    'rb_sft_ClockMonitoring_flt': 'DTCRef recover to ECULifeTimeFailure',
    'rb_COM_systemwarninglamp_flt': 'CRS name are inconsistent, variant1 does not have this fault',
                    }


"""
Simple methods defined
"""
# return 'ExternalFault', 'ErasableInternalFlt' or 'NonErasableInternalFlt' in the future
def getDemRbEventCategoryRef(crsDtc):
    if crsDtc is None:
        return None
    if crsDtc.getAttr('External/Internal').strip() == 'External':
        return 'ExternalFault'
    elif crsDtc.getAttr('External/Internal').strip() == 'Internal':
        error('Internal fault is not supported in standard script, please check: ' + crsDtc.getAttr('Bosch_Name(For SRS FL)'))
def crs_getAtrCol(attr):
    return getAtrCol('CRS', attr)
def srs_getAtrCol(attr):
    return getAtrCol('SRS', attr)


def readCRS_and_createObject(CRS_path):

    # req instance
    req = REQ('CRS')

    # excel read
    excelHelper = ExcelHelper(CRS_path)

    # load crs
    for row in range(2, excelHelper.max_row + 1):
        # filter1: row is a rqmt
        if excelHelper.sheet.Cells(row, crs_getAtrCol('Type')).Value is None or excelHelper.sheet.Cells(row, crs_getAtrCol('Type')).Value != 'Rqmt':
            continue
        # filter2: row is reviewed
        if excelHelper.sheet.Cells(row, crs_getAtrCol('State')).Value in ('rejected'):
            continue
        # filter3: row should have a DTCName, except special case (ex. internal dtc crs dont have name)
        sheet_dtcName = excelHelper.sheet.Cells(row, crs_getAtrCol('Bosch_Name(For SRS FL)')).Value
        if sheet_dtcName is None or len(sheet_dtcName.strip()) <= 0:
            error('row should have a DTCName, except special case (ex. internal dtc crs dont have name)')
            continue
        # filter4: relevant project check
        if excelHelper.sheet.Cells(row, crs_getAtrCol('Relevant Project')).Value is None:
            continue
        # if sheet.Cells(row, crs_getAtrCol('Relevant Project')).Value.find(RelevantProject) == -1:
        #     continue

        sheet_dtcName = sheet_dtcName.strip()
        dtc = DTC(sheet_dtcName)
        for attr, attrCol in configLoader.getAttributesDict(req.reqType).items():
            if excelHelper.sheet.Cells(row, attrCol).Value is not None:
                dtc.Append_Update_Attr(attr, excelHelper.sheet.Cells(row, attrCol).Value.strip())
            else:
                dtc.Append_Update_Attr(attr, excelHelper.sheet.Cells(row, attrCol).Value)
        
        req.appendDTC(dtc)

    # close excel
    excelHelper.workbook.Close(SaveChanges=False)
    excelHelper.excel.Quit()
    
    return req

def readSRS_and_createObject(SRS_path):

    # req instance
    req = REQ('SRS')

    # excel read
    excelHelper = ExcelHelper(SRS_path)

    # load srs
    for row in range(2, excelHelper.max_row + 1):
        # filter1: row is a rqmt
        if excelHelper.sheet.Cells(row, srs_getAtrCol('Type_FL')).Value is None or excelHelper.sheet.Cells(row, srs_getAtrCol('Type_FL')).Value != 'Rqmt':
            continue
        # filter2: row is reviewed
        if excelHelper.sheet.Cells(row, srs_getAtrCol('State')).Value in ('rejected'):
            continue
        # filter3: row should have a DTCName, except special case (ex. internal dtc crs dont have name)
        sheet_dtcName = excelHelper.sheet.Cells(row, srs_getAtrCol('DemEvent')).Value
        if sheet_dtcName is None or len(sheet_dtcName.strip()) <= 0:
            print('find Blank dtc name in srs')
            continue
        # # filter4: row is needed variant
        # if sheet.Cells(row, srs_getAtrCol('Variants')).Value.find(VariantsInSRS) == -1:
        #     continue

        sheet_dtcName = sheet_dtcName.strip()
        dtc = DTC(sheet_dtcName.strip())
        for attr, attrCol in configLoader.getAttributesDict(req.reqType).items():
            if excelHelper.sheet.Cells(row, attrCol).Value is not None:
                dtc.Append_Update_Attr(attr, excelHelper.sheet.Cells(row, attrCol).Value.strip())
            else:
                dtc.Append_Update_Attr(attr, excelHelper.sheet.Cells(row, attrCol).Value)

        req.appendDTC(dtc)

    # close excel
    excelHelper.workbook.Close(SaveChanges=False)
    excelHelper.excel.Quit()

    return req



def update_SRS(SRS_path, SRS_Updated_path, CRS_obj, SRS_obj):

    # excel read
    excelHelper = ExcelHelper(SRS_path)

    for row in range(2, excelHelper.max_row + 1):
        # filter1: row is a rqmt
        if excelHelper.sheet.Cells(row, getAtrCol('SRS', 'Type_FL')).Value is None or excelHelper.sheet.Cells(row, getAtrCol('SRS', 'Type_FL')).Value.strip() != 'Rqmt':
            continue
        # filter2: row is valid
        if excelHelper.sheet.Cells(row, getAtrCol('SRS', 'State')).Value.strip() in ('rejected'):
            continue
        # filter3: DemEvent is None
        if excelHelper.sheet.Cells(row, getAtrCol('SRS', 'DemEvent')).Value is None:
            continue
        # filter4: DTC should in crs, except for internal DTC
        # cur dtc
        sheet_dtcName = excelHelper.sheet.Cells(row, getAtrCol('SRS', 'DemEvent')).Value.strip()

        # first read SRS
        sheet_DemRbEventCategoryRef = excelHelper.sheet.Cells(row, getAtrCol('SRS', 'DemRbEventCategoryRef')).Value.strip()
        if sheet_dtcName.strip() == 'rb_sft_ClockMonitoring_flt':
            sheet_DemRbEventCategoryRef = 'NonErasableInternalFlt'
        # then read CRS for verify
        if getDemRbEventCategoryRef(CRS_obj.getDTC(sheet_dtcName)) is not None:
            sheet_DemRbEventCategoryRef = getDemRbEventCategoryRef(CRS_obj.getDTC(sheet_dtcName)) 
        if sheet_DemRbEventCategoryRef == 'not set' or sheet_DemRbEventCategoryRef is None:
            error(sheet_dtcName + ' DemRbEventCategoryRef get invalid value, please check')
        # filter5: row is needed variant
        # if sheet.Cells(row, srs_getAtrCol('Variants')).Value.find(VariantsInSRS) == -1:
        #     continue
        
        # update srs excel
        for attr in configLoader.getAttributesDict('SRS').keys():
            tmp_res = get_updated_srs_excel_cell_value(sheet_dtcName, attr, sheet_DemRbEventCategoryRef, CRS_obj, SRS_obj, False, True)
            if tmp_res is not None:
                excelHelper.sheet.Cells(row, getAtrCol('SRS', attr)).Value = tmp_res
 
    # remove updated file
    remove_file(SRS_Updated_path)
    # save new updated file
    excelHelper.workbook.SaveAs(SRS_Updated_path, FileFormat=xls_Format_code)
    excelHelper.workbook.Close(SaveChanges=True)
    excelHelper.excel.Quit()






if __name__ == "__main__":
    start_time = time.time()

    close_excel_file({CRS_path, SRS_path, SRS_Updated_path, AdditionalDebugInfo_path, SRS_Updated_path})

    crs = readCRS_and_createObject(CRS_path)
    srs = readSRS_and_createObject(SRS_path)
    crs._Update_DTC_Name_List()
    srs._Update_DTC_Name_List()

    update_SRS(SRS_path, SRS_Updated_path, crs, srs)

    ## optional additional debug info
    remove_file(AdditionalDebugInfo_path)
    # 1. dtc in crs but not in srs
    neededDTC = sorted(set(crs.dtcName_list) - set(srs.dtcName_list))
    with open(AdditionalDebugInfo_path, 'w') as adi:
        adi.write('######### 1 need to be added to fault list (dtc in crs but not in srs)' + '\n')
        for item in neededDTC:
            if item is not None and item.strip() != '':
                adi.write(item + '\n')
    # 2. dtc in srs but not in crs
    neededDTC = sorted(set(srs.dtcName_list) - set(crs.dtcName_list))
    with open(AdditionalDebugInfo_path, 'a') as adi:
        adi.write('\n######### 2 maybe CRS missing some faults (dtc in srs but not in crs)' + '\n')
        for item in neededDTC:
            if item is not None and item.strip() != '':
                adi.write(item + '\n')
    # 3. special dtc and reason, need manual check
    with open(AdditionalDebugInfo_path, 'a') as adi:
        adi.write('\n######### 3 special DTCs require check' + '\n')
        for dtc in special_DTC_Dict.keys():
            adi.write(dtc + ': ' + special_DTC_Dict[dtc] + '\n')
    # 4. no valid qualify/dequalify time
    with open(AdditionalDebugInfo_path, 'a') as adi:
        adi.write('\n######### 4 no valid qualify/dequalify time' + '\n')
        for dtc in noValidResolveTime_list:
            adi.write(dtc + '\n')

    end_time = time.time()
    total_time = end_time - start_time
    minutes = total_time // 60
    seconds = total_time % 60

    print(f'totally use {minutes} minutes {seconds:.2f} seconds, update process complete...')
