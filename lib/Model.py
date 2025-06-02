import sys
from lib.Util import log
import win32com.client

"""
Help store SRS/CRS requirement.
"""
class REQ:

    __supportedReqType = list(('SRS', 'CRS'))

    dtcName_list = list()
    dtc_Dict = dict()
    reqType = ''

    def __init__(self, reqType):
        if reqType not in self.__supportedReqType:
            sys.exit('not supported requirement type: ' + reqType) 
        self.reqType = reqType
        self.dtcName_list = list()
        self.dtc_Dict = dict()
    
    def _Update_DTC_Name_List(self):  # must be called after complete operation
        self.dtcName_list = self.dtc_Dict.keys()

    def appendDTC(self, dtc):
        try:
            self.dtc_Dict[dtc.dtcName] = dtc
        except:
            log.Error('dtc must have a "DTCName"')

    def getDTC(self, dtcName):
        try:
            return self.dtc_Dict[dtcName]
        except:
            log.Error(self.reqType + ' dont have a DTC named: ' + dtcName)


"""
Help store DTC information.
"""
class DTC:

    dtcName = ''
    attrName_List = list()
    dtcAttr_Dict = dict()

    def __init__(self, dtcName):  # must have 'DTCName'
        self.dtcName = dtcName
        self.attrName_List = list() # must re-init here
        self.dtcAttr_Dict = dict()
        self.Append_Update_Attr('DTCName', dtcName)
    
    def Append_Update_Attr(self, key, val):
        self.dtcAttr_Dict[key] = val
        return self  # enable dtc.Append_Update_Attr().Append_Update_Attr()...
        
    def getAttrName_List(self):
        return self.dtcAttr_Dict.keys()

    """
    Get the value of a specified attribute from the DTC attribute dictionary.
    Args:
        attr (str): The name of the attribute to retrieve.
    Returns:
        The value of the requested attribute if it exists in the dictionary.
        Logs an error message if the attribute does not exist.
    Note:
        This method will silently fail (with error logging) if the attribute is not found.
    """
    def getAttr(self, attr):
        try:
            return self.dtcAttr_Dict[attr]
        except:
            log.Error(self.dtcName + ' dont have attribute: ' + attr)
    

class ExcelHelper:
    def __init__(self, CRS_path):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.CRS_path = CRS_path
        self.workbook = self.excel.Workbooks.Open(CRS_path)
        self.sheet = self.workbook.Sheets(2)
        self.max_row = self.sheet.UsedRange.Rows.Count