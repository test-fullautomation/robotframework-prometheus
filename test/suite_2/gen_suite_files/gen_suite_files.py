# **************************************************************************************************************
#
#  Copyright 2020-2024 Robert Bosch GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# **************************************************************************************************************
#
# gen_suite_files.py
#
# XC-HWP/ESW3-Queckenstedt
#
# **************************************************************************************************************
#
VERSION      = "0.3.0"
VERSION_DATE = "24.05.2024"
#
# **************************************************************************************************************

# -- import standard Python modules
import os, sys, shlex, subprocess, ctypes, time, platform, json, pprint, itertools
import colorama as col

# -- import own Python modules
from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Folder.CFolder import CFolder
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Utils.CUtils import *

col.init(autoreset=True)

COLBR = col.Style.BRIGHT + col.Fore.RED
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLBG = col.Style.BRIGHT + col.Fore.GREEN
COLBB = col.Style.BRIGHT + col.Fore.BLUE

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printfailure(sMsg, prefix=None):
   if prefix is None:
      sMsg = COLBR + f"{sMsg}!\n\n"
   else:
      sMsg = COLBR + f"{prefix}:\n{sMsg}!\n\n"
   sys.stderr.write(sMsg)

# --------------------------------------------------------------------------------------------------------------

class CListValues(object):

   # constructor
   def __init__(self, listValues=None, nStartIndex=0, nCntTheSame=1, bRandom=False):
      self.listValues    = listValues
      self.nNrOfValues   = len(self.listValues)
      self.nStartIndex   = nStartIndex
      self.nCntTheSame   = nCntTheSame

      self.nCntCalls     = 0

      if ( (self.nStartIndex < 0) or (self.nStartIndex >= self.nNrOfValues) ):
         self.nCurrentIndex = 0
      else:
         self.nCurrentIndex = self.nStartIndex

      if bRandom is True:
         if type(self.listValues) == list:
            random.shuffle(self.listValues)
         else:
            raise Exception("[CListValues] : Expected 'list' type but got '" + str(type(self.listValues)) + "'!")

   # destructor
   def __del__(self):
      pass

   def Random(self):
      self.nCntCalls     = 0
      self.nCurrentIndex = 0
      if type(self.listValues) == list:
         random.shuffle(self.listValues)
      else:
         raise Exception("[CListValues] : Expected 'list' type but got '" + str(type(self.listValues)) + "'!")

   def GetValue(self, nMode=1):

      if nMode == 0:
         return len(self.listValues)

      oValue = self.listValues[self.nCurrentIndex]

      self.nCntCalls = self.nCntCalls + 1

      if self.nCntCalls >= self.nCntTheSame:
         self.nCntCalls = 0

         if nMode == 1:
            # forwards
            self.nCurrentIndex = self.nCurrentIndex + 1
            if self.nCurrentIndex >= self.nNrOfValues:
               self.nCurrentIndex = 0
         elif nMode == -1:
            # backwards
            self.nCurrentIndex = self.nCurrentIndex - 1
            if self.nCurrentIndex < 0:
               self.nCurrentIndex = self.nNrOfValues - 1
         else:
            return None

      return oValue

# eof class CListValues(object):

# --------------------------------------------------------------------------------------------------------------

sWhoAmI = CString.NormalizePath(os.path.dirname(os.path.abspath(__file__)))
print()
print(f"Script executed in folder '{sWhoAmI}'")

# --------------------------------------------------------------------------------------------------------------

# counter names for test results of suite A
listResultCounter_A = ["num_passed", "num_failed", "num_unknown"]
oResultCounter_A    = CListValues(listResultCounter_A)

# counter names for test results of suite B
listResultCounter_B = ["num_passed", "num_failed", "num_unknown"]
oResultCounter_B    = CListValues(listResultCounter_B)

# mapping between test result counter and test result
dictTestResults = {}
dictTestResults['num_passed']  = "PASSED"
dictTestResults['num_failed']  = "FAILED"
dictTestResults['num_unknown'] = "UNKNOWN"

# test names of suite A (this is separated from EXECUTION_NAME)
listTestNames_A  = ["Suite-A-Test-01","Suite-A-Test-02","Suite-A-Test-03","Suite-A-Test-04","Suite-A-Test-05","Suite-A-Test-06","Suite-A-Test-07","Suite-A-Test-08","Suite-A-Test-09","Suite-A-Test-10"]
oTestNames_A     = CListValues(listTestNames_A)

# test names of suite B (this is separated from EXECUTION_NAME)
listTestNames_B  = ["Suite-B-Test-01","Suite-B-Test-02","Suite-B-Test-03","Suite-B-Test-04","Suite-B-Test-05","Suite-B-Test-06","Suite-B-Test-07","Suite-B-Test-08","Suite-B-Test-09","Suite-B-Test-10"]
oTestNames_B     = CListValues(listTestNames_B)

# discrete values for gauge 'beats_per_minute' of suite A
listBeatsPerMinute_A = [200,180,160,140,120,100,10,20,50]
oBeatsPerMinute_A    = CListValues(listBeatsPerMinute_A)

# discrete values for gauge 'beats_per_minute' of suite B
listBeatsPerMinute_B = [55,25,15,105,125,145,165,185,205]
oBeatsPerMinute_B    = CListValues(listBeatsPerMinute_B)

# lighting for tests of suite A
listLighting_A = ["rf.prometheus_interface.set_daylight", "rf.prometheus_interface.set_nightlight"]
oLighting_A    = CListValues(listLighting_A)

# lighting for tests of suite B
listLighting_B = ["rf.prometheus_interface.set_nightlight", "rf.prometheus_interface.set_daylight"]
oLighting_B    = CListValues(listLighting_B)

# --------------------------------------------------------------------------------------------------------------

sFilePattern = """# generated at ##TIMESTAMP##

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution ##EXECUTION_NAME##
   rf.extensions.pretty_print    ==== Execution: '##EXECUTION_NAME##' / '##TEST_NAME##' : Room_1 / ##TESTBENCH##

   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=##COUNTER##    labels=Room_1;##TESTBENCH##;##TEST_NAME##;##TEST_RESULT##
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_gauge    name=beats_per_minute    value=##BEATS_PER_MINUTE##    labels=Room_1;##TESTBENCH##
   rf.extensions.pretty_print    [set_gauge] (${success}) : ${result}

   ##LIGHTING##

   sleep    ##SLEEP##
"""

# --------------------------------------------------------------------------------------------------------------
#TM***
nNrOfFiles = 900
sSleep     = "2s"
# --------------------------------------------------------------------------------------------------------------

sNrOfFiles = f"{nNrOfFiles}"
nRJust     = len(sNrOfFiles)

sTimestamp = time.strftime('%d.%m.%Y - %H:%M:%S')


# --------------------------------------------------------------------------------------------------------------
# -- suite A
# --------------------------------------------------------------------------------------------------------------

sDestFolder_A = CString.NormalizePath(f"{sWhoAmI}/../suite_2_A/tests")
oDestFolder_A = CFolder(sDestFolder_A)
print()
bSuccess, sResult = oDestFolder_A.Create(bOverwrite=True, bRecursive=True)
if bSuccess is not True:
   printfailure(sResult)
   sys.exit()
print(f"{sResult}")
print()

sLighting_A = oLighting_A.GetValue()

for nFileNumber in range(1, nNrOfFiles+1):
   sFileNumber    = f"{nFileNumber}".rjust(nRJust, '0')
   sIterationName = "I-" + f"{nFileNumber}".rjust(nRJust, '0') + "-A"
   sTestName      = oTestNames_A.GetValue()

   sResultCounter    = oResultCounter_A.GetValue()
   sTestResult       = dictTestResults[sResultCounter]
   sTestbench        = "Testbench 1" # currently fix value
   sBeatsPerMinute_A = str(oBeatsPerMinute_A.GetValue())

   sFileContent = sFilePattern.replace('##TIMESTAMP##', sTimestamp)
   sFileContent = sFileContent.replace('##EXECUTION_NAME##', sIterationName)
   sFileContent = sFileContent.replace('##TEST_NAME##', sTestName)
   sFileContent = sFileContent.replace('##TEST_RESULT##', sTestResult)
   sFileContent = sFileContent.replace('##COUNTER##', sResultCounter)
   sFileContent = sFileContent.replace('##TESTBENCH##', sTestbench)
   sFileContent = sFileContent.replace('##BEATS_PER_MINUTE##', sBeatsPerMinute_A)
   sFileContent = sFileContent.replace('##SLEEP##', sSleep)

   if nFileNumber % 3 == 0:
      sLighting_A = oLighting_A.GetValue()
   sFileContent = sFileContent.replace('##LIGHTING##', sLighting_A)

   sRobotFile = f"{sDestFolder_A}/test_file_{sFileNumber}_A.robot"
   print(f"* '{sRobotFile}'")
   oRobotFile = CFile(sRobotFile)
   oRobotFile.Write(sFileContent)
   del oRobotFile


# --------------------------------------------------------------------------------------------------------------
# -- suite B
# --------------------------------------------------------------------------------------------------------------

sDestFolder_B = CString.NormalizePath(f"{sWhoAmI}/../suite_2_B/tests")
oDestFolder_B = CFolder(sDestFolder_B)
print()
bSuccess, sResult = oDestFolder_B.Create(bOverwrite=True, bRecursive=True)
if bSuccess is not True:
   printfailure(sResult)
   sys.exit()
print(f"{sResult}")
print()

sLighting_B = oLighting_B.GetValue()

for nFileNumber in range(1, nNrOfFiles+1):
   sFileNumber    = f"{nFileNumber}".rjust(nRJust, '0')
   sIterationName = "I-" + f"{nFileNumber}".rjust(nRJust, '0') + "-B"
   sTestName      = oTestNames_B.GetValue()

   sResultCounter    = oResultCounter_B.GetValue()
   sTestResult       = dictTestResults[sResultCounter]
   sTestbench        = "Testbench 2" # currently fix value
   sBeatsPerMinute_B = str(oBeatsPerMinute_B.GetValue())

   sFileContent = sFilePattern.replace('##TIMESTAMP##', sTimestamp)
   sFileContent = sFileContent.replace('##EXECUTION_NAME##', sIterationName)
   sFileContent = sFileContent.replace('##TEST_NAME##', sTestName)
   sFileContent = sFileContent.replace('##TEST_RESULT##', sTestResult)
   sFileContent = sFileContent.replace('##COUNTER##', sResultCounter)
   sFileContent = sFileContent.replace('##TESTBENCH##', sTestbench)
   sFileContent = sFileContent.replace('##BEATS_PER_MINUTE##', sBeatsPerMinute_B)
   sFileContent = sFileContent.replace('##SLEEP##', sSleep)

   if nFileNumber % 4 == 0:
      sLighting_B = oLighting_B.GetValue()
   sFileContent = sFileContent.replace('##LIGHTING##', sLighting_B)

   sRobotFile = f"{sDestFolder_B}/test_file_{sFileNumber}_B.robot"
   print(f"* '{sRobotFile}'")
   oRobotFile = CFile(sRobotFile)
   oRobotFile.Write(sFileContent)
   del oRobotFile



