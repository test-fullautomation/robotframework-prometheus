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

# XC-HWP/ESW3-Queckenstedt

# -- import standard Python modules
import pickle, os, time, random
import dotdict

from prometheus_client import start_http_server, Gauge, Counter

# -- import Robotframework API
from robot.api.deco import keyword, library # required when using @keyword, @library decorators
from robot.libraries.BuiltIn import BuiltIn

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Utils.CUtils import *

# --------------------------------------------------------------------------------------------------------------

sThisModuleName    = "prometheus_interface.py"
sThisModuleVersion = "0.1.1"                         # TODO: import from version.py
sThisModuleDate    = "16.05.2024"                    # TODO: import from version.py
sThisModule        = f"{sThisModuleName} v. {sThisModuleVersion} / {sThisModuleDate}"

# --------------------------------------------------------------------------------------------------------------
# 
@library
class prometheus_interface():
    """ generic system methods
    """

    ROBOT_AUTO_KEYWORDS   = False # only decorated methods are keywords
    ROBOT_LIBRARY_VERSION = sThisModuleVersion
    ROBOT_LIBRARY_SCOPE   = 'GLOBAL'

    # --------------------------------------------------------------------------------------------------------------
    #TM***

    def __init__(self, sThisModule=sThisModule, port_number=8000, message_level="INFO"):

        self.__sThisModule   = sThisModule
        self.__sMessageLevel = message_level

        self.__dictCounter = {}
        self.__dictGauges  = {}

        start_http_server(port_number)

    def __del__(self):
        del self.__dictGauges

    # --------------------------------------------------------------------------------------------------------------
    #TM***

    @keyword
    def add_counter(self, name=None, description=None, labels=None):
        """add_counter
        """
        if name not in self.__dictCounter:
            labellist = labels.split(';')
            listLabels = []
            for label in labellist:
                label = label.strip()
                listLabels.append(label)
            oCounter = Counter(name, description, listLabels)
            self.__dictCounter[name] = oCounter
    # eof def add_counter(...):

    @keyword
    def inc_counter(self, name=None, value=None, labels=None):
        """inc_counter
        """
        labellist = labels.split(';')
        listLabels = []
        for label in labellist:
            label = label.strip()
            listLabels.append(label)
        oCounter = self.__dictCounter[name]     # TODO: error handling
        # the following is not nice, but 'oCounter.labels(listLabels).inc(value)' does not work / error: 'incorrect label count' / investigation to be done
        listLabels_2 = []
        for label in listLabels:
           listLabels_2.append(f"\"{label}\"")
        sLabels = ", ".join(listLabels_2)
        if value is None:
            value = 1
        sCode = f"oCounter.labels({sLabels}).inc(value)"
        bSuccess = True
        sResult = f"counter '{name}' incremented by value '{value}' with labels: '{labels}'"
        try:
           exec(sCode)
        except Exception as ex:
           bSuccess = False
           sResult  = str(ex)
        return bSuccess, sResult

    # eof def inc_counter(...):

    # --------------------------------------------------------------------------------------------------------------

    @keyword
    def add_gauge(self, name=None, description=None, labels=None):
        """add_gauge
        """
        if name not in self.__dictGauges:
            labellist = labels.split(';')
            listLabels = []
            for label in labellist:
                label = label.strip()
                listLabels.append(label)
            oGauge = Gauge(name, description, listLabels)
            self.__dictGauges[name] = oGauge
    # eof def add_gauge(...):

    @keyword
    def set_gauge(self, name=None, value=None, labels=None):
        """set_gauge
        """
        labellist = labels.split(';')
        listLabels = []
        for label in labellist:
            label = label.strip()
            listLabels.append(label)
        oGauge = self.__dictGauges[name]              # TODO: error handling
        # the following is not nice, but 'oGauge.labels(listLabels).set(value)' does not work / error: 'incorrect label count' / investigation to be done
        listLabels_2 = []
        for label in listLabels:
           listLabels_2.append(f"\"{label}\"")
        sLabels = ", ".join(listLabels_2)
        sCode = f"oGauge.labels({sLabels}).set(value)"
        bSuccess = True
        sResult = f"gauge '{name}' set to value '{value}' with labels: '{labels}'"
        try:
           exec(sCode)
        except Exception as ex:
           bSuccess = False
           sResult  = str(ex)
        return bSuccess, sResult

    # eof def set_gauge(...):

    # --------------------------------------------------------------------------------------------------------------

# eof class prometheus_interface():

