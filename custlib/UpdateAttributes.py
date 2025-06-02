#Remark: SFT: LfmTriggerLifeTimeFault, LfmCounterLimit, PFT Reprogrammable, PFT External Filtering Cycles, PFT FaultEvaluation
#TODO: LfmTriggerLifeTimeFault, LfmCounterLimit are in SFT, need implement; LfmCounterLimit cannot be imported, notice
from lib.Util import log

noValidResolveTime_list = list()

## dtc name, attribute name, external/erasableInternal/non-erasableInternal, crs, srs
def get_updated_srs_excel_cell_value(dtcName, attrName, attr_DemRbEventCategoryRef, CRS_obj, SRS_obj, setState=False, updateDocFlag=False):
    # if attr_DemRbEventCategoryRef not in ('ExternalFault'):
    #     return None
    #     log.Error(dtcName + ': DemRbEventCategoryRef is not valid')
    
    curDTC_crs = CRS_obj.getDTC(dtcName) if dtcName in CRS_obj.dtcName_list else None
    curDTC_srs = SRS_obj.getDTC(dtcName)

    ############################
    ### dem attribute update ###
    ############################
    if curDTC_crs is None:  # if not in crs, skip; update part of attributes, others don't change
        if attrName not in ('DemEventAvailable'):
            return None

    if attrName == 'ID':
        return None
    elif attrName == 'Type_FL':
        return None
    elif attrName == 'State':
        return 'proposed' if setState else None
    elif attrName == 'Variants':
        return None
    elif attrName == 'DemEvent':
        return dtcName  # set stripped name
    elif attrName == 'DemDTCRef':
        tempRes = None
        if attr_DemRbEventCategoryRef == 'ExternalFault':
            tempRes =  curDTC_crs.getAttr('DTC Number').replace('0x', 'DTC')
        if curDTC_srs.getAttr('DemEvent') == 'rb_edr_DataAreaFull_flt':
            tempRes =  'DTC927F47'
        elif curDTC_srs.getAttr('DemEvent') == 'rb_sft_ClockMonitoring_flt':
            tempRes =  'ECULifeTimeFailure'
        if tempRes is None:
            log.Warning("internal fault not supported: " + dtcName)
        return tempRes
    elif attrName == 'DemDTCSeverity':
        return None
    elif attrName == 'DemDTCSignificance':
        return None
    elif attrName == 'DemDtcValue':
        if dtcName == 'rb_edr_DataAreaFull_flt':
            return '0x927F47'
        elif dtcName == 'rb_sft_ClockMonitoring_flt':
            return '0x92511F'
        else:
            return curDTC_crs.getAttr('DTC Number')
    elif attrName == 'DemEventAvailable':
        if attr_DemRbEventCategoryRef != 'ExternalFault':
            return None
        return 'True' if curDTC_crs is not None else 'False'
    elif attrName == 'DemEventMemoryEntryFdcThresholdStorageValue':
        return None
    elif attrName == 'DemEventKind':
        return None
    elif attrName == 'DemEventFailureCycleCounterThreshold':
        return None
    elif attrName == 'DemEnableConditionGroupRef':
        return None
    elif attrName == 'DemDTCPriority':
        return curDTC_crs.getAttr('Priority')
    elif attrName == 'DemDebounceCounterBasedClassRef':
        return None  # TODO: if quali/dequali changed, remind user check this value
    elif attrName == 'DeActTrigger':
        if curDTC_crs.getAttr('WL Behavior') == 'WL not on':
            return 'NO_INDICATOR'
        elif curDTC_crs.getAttr('WL Behavior') == 'WL on filtered fault':
            return 'DEACT_TF'
        elif curDTC_crs.getAttr('WL Behavior') == 'WL on latched fault':
            return 'DEACT_TFTOC'
        elif curDTC_crs.getAttr('WL Behavior') == 'WL on stored fault':
            return 'DEACT_ON_CONFIRMED'
        else:
            log.Error('none supported WL Behavior for ' + dtcName)
    elif (attrName == 'DemCallbackEventStatusChangedRBRef' 
        or attrName == 'DEMTriggerSysReaction'):  # DEMTriggerSysReaction is for M05
        if curDTC_crs.getAttr('PFT System Reaction') in (None, '', 'None', 'Disable feature within module', 'Disable feature permanently within module'):
            return 'STATUS_CHANGE_ALLEVENTS' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'NO_SYSTEM_REACTION'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable Algo Complete'):
            return 'STATUS_CHANGE_DISABLEALLALGO' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLEALLALGO'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable Algo FrontRear'):
            return 'STATUS_CHANGE_DISABLEFRONTANDREARALGO' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLEFRONTANDREARALGO'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable Algo Side'):
            return 'STATUS_CHANGE_DISABLESIDEALGO' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLESIDEALGO'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable Algo Rollover'):
            return 'STATUS_CHANGE_DISABLEROSEALGO' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLEROSEALGO'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable Algo EPP'):
            return 'STATUS_CHANGE_DISABLEEPPALGO' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLEEPPALGO'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable SW Firing'):
            return 'STATUS_CHANGE_DISABLESWFIRING' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLESWFIRING'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Idle Mode For Current Pon'):
            return 'STATUS_CHANGE_IDLEMODEFORCURRENTPON' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_IDLEMODEFORCURRENTPON'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Permanent Idle Mode'):
            return 'STATUS_CHANGE_PERMANENTIDLEMODE' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_PERMANENTIDLEMODE'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable Algo StaticRollover'):
            return 'STATUS_CHANGE_DISABLE_STATICROLLOVERALGO' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLE_STATICROLLOVERALGO'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable Algo AllRollover'):
            return 'STATUS_CHANGE_DISABLE_ALLROLLOVERALGO' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLE_ALLROLLOVERALGO'
        elif curDTC_crs.getAttr('PFT System Reaction') in ('FLM: Disable Algo Pitchover'):
            return 'STATUS_CHANGE_DISABLE_PITCHOVERALGO' if attrName == 'DemCallbackEventStatusChangedRBRef' else 'STATUS_CHANGE_DISABLE_PITCHOVERALGO'
        else:
            log.Error('non supported system reaction for ' + dtcName)
    elif attrName == 'DemCallbackEventDataChangedFnc':
        return None
    elif attrName == 'DemCallbackInitMForEFnc':
        return None
    elif attrName == 'DemRbEventCategoryRef':
        return attr_DemRbEventCategoryRef
    elif attrName == 'DemAgingAllowed':
        if curDTC_crs.getAttr('AgingAllow') == 'Yes':
            return 'True'
        elif curDTC_crs.getAttr('AgingAllow') == 'No':
            return 'False'
        log.Error('invalid agingAllow in crs: ' + curDTC_crs.getAttr('AgingAllow'))
    elif attrName == 'DemAgingCycleCounterThreshold':
        if curDTC_crs.getAttr('AgingAllow') == 'No':  # no aging then give default value
            return '1'
        elif 'AgingCounterCycles' in curDTC_crs.getAttrName_List():
            return curDTC_crs.getAttr('AgingCounterCycles')
        elif 'AgingCounter' in curDTC_crs.getAttrName_List():
            return curDTC_crs.getAttr('AgingCounter')
        elif 'AgingCounter_5.0' in curDTC_crs.getAttrName_List():
            return curDTC_crs.getAttr('AgingCounter_5.0')
        else:
            return None  #TODO: if crs don't have this col, remind user check this
    elif attrName == 'DemAgingCycleCounterThresholdForTFSLC':
        return None
    elif attrName == 'DemAgingCycleRef':
        return None  # default PowerCycle
    elif attrName == 'DemExtendedDataClassRef':
        return None  # default ExtendedData
    elif attrName == 'DemFFPrestorageSupported':
        return None  # default False
    elif attrName == 'DemFreezeFrameClassRef':
        return None  # default DemFreezeFrameClass_0
    elif attrName == 'DemFreezeFrameRecNumClassRef':
        return None  # default RecordNumber_1
    elif attrName == 'DemMaxNumberFreezeFrameRecords':
        return None  # default DemMaxNumberFreezeFrameRecords
    elif attrName == 'DemStorageConditionGroupRef':
        return None  # default blank
    elif attrName == 'DemRbEventRecoverableInSameOperationCycle':
        return 'True'  #TODO: default True, Change only with an explicit requirement from customer
    elif attrName == 'DemRbEventDescription':
        return None
    elif attrName == 'DemRbAlternativeDTC':
        return None  # default blank
    elif attrName == 'DemOperationCycleRef':
        return None  # default PowerCycle
    elif attrName == 'DemMemoryDestinationRef':
        return None  # default DemPrimaryMemory
    elif attrName == 'DemImmediateNvStorage':
        return None  # default True
    elif attrName == 'DemReportBehavior':
        return None  # Most are REPORT_AFTER_INIT, except rb_mem_ExternalEEPROM_flt, rb_mem_ExternalNOR_flt
    #####################################
    ###  CustAttribute and non enum   ###
    #####################################
    # elif attrName == 'CustDTCUploadNum':
    #     if str(curDTC_crs.getAttr('FaultNum(for DTC Upload)')).find('0x') != -1:
    #         return curDTC_crs.getAttr('FaultNum(for DTC Upload)')
    #     else:
    #         return '0x' + curDTC_crs.getAttr('FaultNum(for DTC Upload)')
    #######################
    ### document update ###
    #######################
    elif updateDocFlag is False:
        return None
    elif updateDocFlag:
        if (str(curDTC_crs.getAttr('Qualification Time')).lower().find('init') == -1 and str(curDTC_crs.getAttr('Qualification Time')).lower().find('cyc') == -1) or (str(curDTC_crs.getAttr('Dequalification Time')).lower().find('init') == -1 and str(curDTC_crs.getAttr('Dequalification Time')).lower().find('cyc') == -1):
            noValidResolveTime_list.append(dtcName)
            return None
        if attrName == 'Cust init. qualification time':
            for line in str(curDTC_crs.getAttr('Qualification Time')).splitlines():
                if line.lower().find('init') != -1:
                    try:
                        return line.split(':')[1].strip()
                    except:
                        noValidResolveTime_list.append(dtcName)
            return "NA"
        elif attrName == 'Cust init. dequalification time':
            for line in str(curDTC_crs.getAttr('Dequalification Time')).splitlines():
                if line.lower().find('init') != -1:
                    try:
                        return line.split(':')[1].strip()
                    except:
                        noValidResolveTime_list.append(dtcName)
            return "NA"
        elif attrName == 'Cust cyc. qualification time':    # default cyc detection
            for line in str(curDTC_crs.getAttr('Qualification Time')).splitlines():
                if line.lower().find('cyc') != -1:
                    try:
                        return line.split(':')[1].strip()
                    except:
                        noValidResolveTime_list.append(dtcName)
            return "NA"
        elif attrName == 'Cust cyc. dequalification time':    # default cyc detection
            for line in str(curDTC_crs.getAttr('Dequalification Time')).splitlines():
                if line.lower().find('cyc') != -1:
                    try:
                        return line.split(':')[1].strip()
                    except:
                        noValidResolveTime_list.append(dtcName)
            return "NA"
        elif attrName == 'targetLinkTag':
            return curDTC_crs.getAttr('ID').replace('FLT_', '')  # cust attr, used for create doors link
        elif attrName == 'Object Text':
            return None  #TODO
        elif attrName == 'Original_ASIL_Classification':
            return curDTC_crs.getAttr('original ASIL-Classification')
        elif attrName == 'ASIL Classification':
            return curDTC_crs.getAttr('ASIL-Classification')
        elif attrName == 'PFT Reprogrammable':
            return None  #TODO: remind SFT provide
        elif attrName == 'Source_CQ_ID':
            return None  #TODO
        elif attrName == 'Remark':
            return None  #TODO
        elif attrName == 'Reprogrammable':
            return None  #TODO: depend on SFT
        elif attrName == 'PFT WL behavior':
            if curDTC_crs.getAttr('WL Behavior') == 'WL not on':
                return 'None'
            return curDTC_crs.getAttr('WL Behavior')
        elif attrName == 'PFT System Reaction':
            return curDTC_crs.getAttr('PFT System Reaction')
        elif attrName == 'PFT Quali/Dequalification time':
            return 'Qualification:\n' + curDTC_crs.getAttr('Qualification Time') + '\n\n' + 'Dequalification:\n' + curDTC_crs.getAttr('Dequalification Time')
        elif attrName == 'PFT FaultEvaluation':
            return None  #TODO: need SFT
        elif attrName == 'PFT FaultDequaliClass':
            return None  #TODO: maybe need SFT
        elif attrName == 'PFT Fault Type':
            if attr_DemRbEventCategoryRef == 'ExternalFault':
                return 'Mandatory External'
            else:
                return None
        elif attrName == 'PFT Fault Creation':
            if curDTC_srs.getAttr('PFT Fault Creation') is not None:
                return None
            return curDTC_crs.getAttr('Qualify Condition')
        elif attrName == 'PFT FailSafeLimit':
            return None  #TODO: need sft
        elif attrName == 'PFT External Filtering Cycles':
            return None  #TODO: need sft
        elif attrName == 'PFT DetailedSystemReaction':
            return None  # DXL has bug
            return curDTC_crs.getAttr('PFT System Reaction')
        elif attrName == 'PFT Battery voltage dependent':
            return curDTC_crs.getAttr('Battery Voltage Dependence')
        elif attrName == 'Battery voltage dependent':
            if curDTC_crs.getAttr('Battery Voltage Dependence') == 'Yes':
                return 'True'
            elif curDTC_crs.getAttr('Battery Voltage Dependence') == 'No':
                return 'False'
            else:
                return None
    #####################################
    ### mismatch with every attribute ###
    #####################################
    else:
        print('None supported attr: ' + attrName)
        return None

