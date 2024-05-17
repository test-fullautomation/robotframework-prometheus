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

from prometheus_client import start_http_server, Gauge

# -- import Robotframework API
from robot.api.deco import keyword, library # required when using @keyword, @library decorators
from robot.libraries.BuiltIn import BuiltIn

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Utils.CUtils import *

# --------------------------------------------------------------------------------------------------------------

sThisModuleName    = "prometheus_interface.py"
sThisModuleVersion = "0.1.0"                         # TODO: import from version.py
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

    def __init__(self, sThisModule=sThisModule, sMessageLevel="INFO"):

        self.__sThisModule = sThisModule
        self.sMessageLevel = sMessageLevel

        # Starte den HTTP-Server auf Port 8000
        start_http_server(8000)

        self.__dictGauges = {}


    def __del__(self):
        del self.__dictGauges

    # --------------------------------------------------------------------------------------------------------------
    #TM***

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
        oGauge = self.__dictGauges[name]
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

