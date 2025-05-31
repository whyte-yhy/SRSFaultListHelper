import json
import os
import sys

from lib.Util import log

class ConfigHelper:

    def __init__(self):
        self.load_dict = dict()
    
    def _load_cfg(self):
        with open(os.path.join(os.getcwd(), "FaultListHelperCFG.json"),'r', encoding='UTF-8') as f:
            self.load_dict = json.load(f)

    def getAttrColNum(self, category, attrName):
        try:
            return self.load_dict[category][attrName]
        except:
            print('accessed attribute not exists in FaultListHelperCFG.json: ' + category + ': ' + attrName)
    
    def getAttributesDict(self, category):
        try:
            return self.load_dict[category]
        except:
            log.Error('Non-supported req type:' + category)


configLoader = ConfigHelper()
configLoader._load_cfg()
