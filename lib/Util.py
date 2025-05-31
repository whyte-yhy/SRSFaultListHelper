import os
import win32com.client

'''
Class:
    enhance print function
'''
class PrintUtils:

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

    '''
    Function:
        private method, change color. User should only call other method like "Error(msg)"
    '''
    def __wrapMsg(self, msg, color):
        print(color + str(msg) + self.RESET)
    
    def Error(self, msg):
        self.__wrapMsg('Error: ' + msg, self.RED)
    
    def Result(self, msg):
        self.__wrapMsg('Result: ' + msg, self.GREEN)

    def Warning(self, msg):
        self.__wrapMsg('Warning: ' + msg, self.YELLOW)



class UtilMethods:
    # remove file
    def remove_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"removed file: {file_path}")

    # convert 'D' to 4
    def getColNum(self, charCol):
        return ord(str(charCol).lower()) - ord('a') + 1
    
    # close excel
    def close_excel_file(self, file_path_list):
        excel = win32com.client.Dispatch("Excel.Application")
        for workbook in excel.Workbooks:
            for file_path in file_path_list:
                if workbook.FullName == os.path.abspath(file_path):
                    workbook.Close(SaveChanges=False)
                    print(f"close file: {file_path}")
                    break
        else:
            print("file is not opened")


log = PrintUtils()
util = UtilMethods()