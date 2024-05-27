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

# -- import Prometheus interface
from prometheus_client import start_http_server, Gauge, Counter, Info

# -- import Robotframework API
from robot.api.deco import keyword, library # required when using @keyword, @library decorators
from robot.libraries.BuiltIn import BuiltIn

# -- import some helpers
from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Utils.CUtils import *

# -- import library version
from PrometheusInterface.version import VERSION as LIBRARY_VERSION
from PrometheusInterface.version import VERSION_DATE as LIBRARY_VERSION_DATE

# --------------------------------------------------------------------------------------------------------------

THISMODULENAME = "prometheus_interface.py"
THISMODULE     = f"{THISMODULENAME} v. {LIBRARY_VERSION} / {LIBRARY_VERSION_DATE}"

# --------------------------------------------------------------------------------------------------------------
# 
@library
class prometheus_interface():
   """class prometheus_interface
   """

   ROBOT_AUTO_KEYWORDS   = False # only decorated methods are keywords
   ROBOT_LIBRARY_VERSION = LIBRARY_VERSION
   ROBOT_LIBRARY_SCOPE   = 'GLOBAL'

   DEFAULT_PORT = 8000

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def __init__(self, port_number=DEFAULT_PORT, message_level="INFO"):
      self.__sMessageLevel = message_level
      self.__dictCounter = {}
      self.__dictGauges  = {}
      start_http_server(port_number)

      self.__oLighting = None # experimental only

   def __del__(self):
      del self.__dictCounter
      del self.__dictGauges

   # --------------------------------------------------------------------------------------------------------------
   # -- library informations
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def get_version(self):
      """get_version
      """
      return LIBRARY_VERSION

   @keyword
   def who_am_i(self):
      """who_am_i
      """
      return THISMODULE

   @keyword
   def where_am_i(self):
      """who_am_i
      """
      location = CString.NormalizePath(os.path.abspath(__file__))
      return location


   # --------------------------------------------------------------------------------------------------------------
   # -- infos
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   # >>> "infos" keywords experimental, hard coded and under construction

   @keyword
   def add_info(self):
      """add_info (content currently hard coded here)
      """
      oInfo = Info('prometheus_interface', ': name and version of prometheus interface')
      oInfo.info({'interface': f"{THISMODULE}", 'version': f"{LIBRARY_VERSION}"})

   @keyword
   def add_lighting(self):
      """add_lighting
      """
      self.__oLighting = Info('lighting', ': kind of lighting')

   @keyword
   def set_daylight(self):
      """set_daylight
      """
      self.__oLighting.info({'lighting' : 'daylight'})

   @keyword
   def set_nightlight(self):
      """set_nightlight
      """
      self.__oLighting.info({'lighting' : 'nightlight'})


   # --------------------------------------------------------------------------------------------------------------
   # -- counter
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def add_counter(self, name=None, description=None, labels=None):
      """add_counter
      """
      bSuccess = False
      sResult  = "UNKNOWN"
      if name is None:
         sResult = "parameter 'name' not defined"
         return bSuccess, sResult
      if description is None:
         sResult = "parameter 'description' not defined"
         return bSuccess, sResult
      if name in self.__dictCounter:
         sResult = f"a counter with name '{name}' is already defined"
         return bSuccess, sResult
      oCounter = None
      if labels is None:
         oCounter = Counter(name, description)
      else:
         labellist = labels.split(';')
         listLabels = []
         for label in labellist:
            label = label.strip()
            listLabels.append(label)
         oCounter = Counter(name, description, listLabels)
      self.__dictCounter[name] = oCounter
      bSuccess = True
      sResult  = f"counter '{name}' added"
      return bSuccess, sResult
   # eof def add_counter(...):

   @keyword
   def inc_counter(self, name=None, value=None, labels=None):
      """inc_counter
      """
      bSuccess = False
      sResult  = "UNKNOWN"
      if name is None:
         sResult = "parameter 'name' not defined"
         return bSuccess, sResult
      if name not in self.__dictCounter:
         sResult = f"counter '{name}' not defined"
         return bSuccess, sResult
      if value is not None:
         try:
            value = int(value)
         except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult
      oCounter = self.__dictCounter[name]
      if labels is None:
         if value is None:
            oCounter.inc()
         else:
            oCounter.inc(value)
      else:
         labellist = labels.split(';')
         listLabels = []
         for label in labellist:
            label = label.strip()
            listLabels.append(label)
         # the following is not nice, but 'oCounter.labels(listLabels).inc(value)' does not work / error: 'incorrect label count' / investigation to be done
         listLabels_2 = []
         for label in listLabels:
            listLabels_2.append(f"\"{label}\"")
         sLabels = ", ".join(listLabels_2)
         if value is None:
            sCode = f"oCounter.labels({sLabels}).inc()"
         else:
            sCode = f"oCounter.labels({sLabels}).inc(value)"
         try:
            exec(sCode)
         except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult
      bSuccess = True
      listResults = []
      listResults.append(f"counter '{name}' incremented")
      if value is not None:
         listResults.append(f"by value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      sResult = " ".join(listResults)
      return bSuccess, sResult
   # eof def inc_counter(...):


   # --------------------------------------------------------------------------------------------------------------
   # -- gauges
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def add_gauge(self, name=None, description=None, labels=None):
      """add_gauge
      """
      bSuccess = False
      sResult  = "UNKNOWN"
      if name is None:
         sResult = "parameter 'name' not defined"
         return bSuccess, sResult
      if description is None:
         sResult = "parameter 'description' not defined"
         return bSuccess, sResult
      if name in self.__dictGauges:
         sResult = f"a gauge with name '{name}' is already defined"
         return bSuccess, sResult
      oGauge = None
      if labels is None:
         oGauge = Gauge(name, description)
      else:
         labellist = labels.split(';')
         listLabels = []
         for label in labellist:
            label = label.strip()
            listLabels.append(label)
         oGauge = Gauge(name, description, listLabels)
      self.__dictGauges[name] = oGauge
      bSuccess = True
      sResult  = f"gauge '{name}' added"
      return bSuccess, sResult
   # eof def add_gauge(...):

   @keyword
   def set_gauge(self, name=None, value=None, labels=None):
      """set_gauge
      """
      bSuccess = False
      sResult  = "UNKNOWN"
      if name is None:
         sResult = "parameter 'name' not defined"
         return bSuccess, sResult
      if name not in self.__dictGauges:
         sResult = f"gauge '{name}' not defined"
         return bSuccess, sResult
      if value is None:
         sResult = "parameter 'value' not defined"
         return bSuccess, sResult
      else:
         try:
            value = int(value)
         except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult
      oGauge = self.__dictGauges[name]
      if labels is None:
         oGauge.set(value)
      else:
         labellist = labels.split(';')
         listLabels = []
         for label in labellist:
            label = label.strip()
            listLabels.append(label)
         # the following is not nice, but 'oGauge.labels(listLabels).set(value)' does not work / error: 'incorrect label count' / investigation to be done
         listLabels_2 = []
         for label in listLabels:
            listLabels_2.append(f"\"{label}\"")
         sLabels = ", ".join(listLabels_2)
         sCode = f"oGauge.labels({sLabels}).set(value)"
         try:
            exec(sCode)
         except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult
      bSuccess = True
      listResults = []
      listResults.append(f"gauge '{name}' set to value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      sResult = " ".join(listResults)
      return bSuccess, sResult
   # eof def set_gauge(...):

   @keyword
   def inc_gauge(self, name=None, value=None, labels=None):
      """inc_gauge
      """
      bSuccess = False
      sResult  = "UNKNOWN"
      if name is None:
         sResult = "parameter 'name' not defined"
         return bSuccess, sResult
      if name not in self.__dictGauges:
         sResult = f"Gause '{name}' not defined"
         return bSuccess, sResult
      if value is not None:
         try:
            value = int(value)
         except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult
      oGauge = self.__dictGauges[name]
      if labels is None:
         if value is None:
            oGauge.inc()
         else:
            oGauge.inc(value)
      else:
         labellist = labels.split(';')
         listLabels = []
         for label in labellist:
            label = label.strip()
            listLabels.append(label)
         # the following is not nice, but 'oGauge.labels(listLabels).inc(value)' does not work / error: 'incorrect label count' / investigation to be done
         listLabels_2 = []
         for label in listLabels:
            listLabels_2.append(f"\"{label}\"")
         sLabels = ", ".join(listLabels_2)
         if value is None:
            sCode = f"oGauge.labels({sLabels}).inc()"
         else:
            sCode = f"oGauge.labels({sLabels}).inc(value)"
         try:
            exec(sCode)
         except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult
      bSuccess = True
      listResults = []
      listResults.append(f"gauge '{name}' incremented")
      if value is not None:
         listResults.append(f"by value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      sResult = " ".join(listResults)
      return bSuccess, sResult
   # eof def inc_gauge(...):

   @keyword
   def dec_gauge(self, name=None, value=None, labels=None):
      """dec_gauge
      """
      bSuccess = False
      sResult  = "UNKNOWN"
      if name is None:
         sResult = "parameter 'name' not defined"
         return bSuccess, sResult
      if name not in self.__dictGauges:
         sResult = f"Gause '{name}' not defined"
         return bSuccess, sResult
      if value is not None:
         try:
            value = int(value)
         except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult
      oGauge = self.__dictGauges[name]
      if labels is None:
         if value is None:
            oGauge.dec()
         else:
            oGauge.dec(value)
      else:
         labellist = labels.split(';')
         listLabels = []
         for label in labellist:
            label = label.strip()
            listLabels.append(label)
         # the following is not nice, but 'oGauge.labels(listLabels).inc(value)' does not work / error: 'incorrect label count' / investigation to be done
         listLabels_2 = []
         for label in listLabels:
            listLabels_2.append(f"\"{label}\"")
         sLabels = ", ".join(listLabels_2)
         if value is None:
            sCode = f"oGauge.labels({sLabels}).dec()"
         else:
            sCode = f"oGauge.labels({sLabels}).dec(value)"
         try:
            exec(sCode)
         except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult
      bSuccess = True
      listResults = []
      listResults.append(f"gauge '{name}' decremented")
      if value is not None:
         listResults.append(f"by value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      sResult = " ".join(listResults)
      return bSuccess, sResult
   # eof def dec_gauge(...):


# eof class prometheus_interface():

