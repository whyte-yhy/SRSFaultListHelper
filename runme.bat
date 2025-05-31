@echo off
setlocal enabledelayedexpansion

REM 0. prepare FaultListHelperCFG.json and do some verifications
python "runAtFirst/ConfigAutomation.py"
python "runAtFirst/script_SRS_AttributesVerify.py"

REM 1. run main function
python FaultListHelper.py

pause