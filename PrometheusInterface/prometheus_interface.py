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
   """The class 'prometheus_interface' provides to communicate with the monitoring system Prometheus.
For this purpose the 'Prometheus Python client library' is used.
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
      """Returns the version of this interface library
      """
      return LIBRARY_VERSION

   @keyword
   def who_am_i(self):
      """Returns the full name of this interface library
      """
      return THISMODULE

   @keyword
   def where_am_i(self):
      """Returns path and file name of this interface library
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
      """add_info (experimental only)
      """
      oInfo = Info('prometheus_interface', ': name and version of prometheus interface')
      oInfo.info({'interface': f"{THISMODULE}", 'version': f"{LIBRARY_VERSION}"})

   @keyword
   def add_lighting(self):
      """add_lighting (experimental only)
      """
      self.__oLighting = Info('lighting', ': kind of lighting')

   @keyword
   def set_daylight(self):
      """set_daylight (experimental only)
      """
      self.__oLighting.info({'lighting' : 'daylight'})

   @keyword
   def set_nightlight(self):
      """set_nightlight (experimental only)
      """
      self.__oLighting.info({'lighting' : 'nightlight'})


   # --------------------------------------------------------------------------------------------------------------
   # -- counter
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def add_counter(self, name=None, description=None, labels=None):
      """This keyword adds a new counter. The values of existing counters can be changed with ``inc_counter``.

**Arguments:**

* ``name``

  The name of the new counter

  / *Condition*: required / *Type*: str /

* ``description``

  The description of the new counter

  / *Condition*: required / *Type*: str /

* ``labels``

  A semicolon separated list of label names assigned to the new counter

  / *Condition*: optional / *Type*: str  / *Default*: None /

**Returns:**

* ``success``

  / *Type*: bool /

  Indicates if the computation of the keyword was successful or not

* ``result``

  / *Type*: str /

  The result of the computation of the keyword
      """
      success = False
      result  = "UNKNOWN"
      if name is None:
         result = "parameter 'name' not defined"
         return success, result
      if description is None:
         result = "parameter 'description' not defined"
         return success, result
      if name in self.__dictCounter:
         result = f"a counter with name '{name}' is already defined"
         return success, result
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
      success = True
      result  = f"counter '{name}' added"
      return success, result
   # eof def add_counter(...):

   @keyword
   def inc_counter(self, name=None, value=None, labels=None):
      """This keyword increments a counter. The counter has to be added with '``add_counter``' before.

**Arguments:**

* ``name``

  The name of the counter

  / *Condition*: required / *Type*: str /

* ``value``

  The value of increment. If not given, the value of the counter is incremented by value 1.

  / *Condition*: optional / *Type*: int  / *Default*: None /

* ``labels``

  A semicolon separated list of labels assigned to the counter. The order of labels must fit to the order of label names like defined in ``add_counter``.

  / *Condition*: optional / *Type*: str  / *Default*: None /

**Returns:**

* ``success``

  / *Type*: bool /

  Indicates if the computation of the keyword was successful or not

* ``result``

  / *Type*: str /

  The result of the computation of the keyword
      """
      success = False
      result  = "UNKNOWN"
      if name is None:
         result = "parameter 'name' not defined"
         return success, result
      if name not in self.__dictCounter:
         result = f"counter '{name}' not defined"
         return success, result
      if value is not None:
         try:
            value = int(value)
         except Exception as ex:
            success = False
            result  = str(ex)
            return success, result
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
            success = False
            result  = str(ex)
            return success, result
      success = True
      listResults = []
      listResults.append(f"counter '{name}' incremented")
      if value is not None:
         listResults.append(f"by value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def inc_counter(...):


   # --------------------------------------------------------------------------------------------------------------
   # -- gauges
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def add_gauge(self, name=None, description=None, labels=None):
      """This keyword adds a new gauge. The values of existing gauges can be changed with ``set_gauge``, ``inc_gauge`` and ``dec_gauge``.

**Arguments:**

* ``name``

  The name of the new gauge

  / *Condition*: required / *Type*: str /

* ``description``

  The description of the new gauge

  / *Condition*: required / *Type*: str /

* ``labels``

  A semicolon separated list of label names assigned to the new gauge

  / *Condition*: optional / *Type*: str  / *Default*: None /

**Returns:**

* ``success``

  / *Type*: bool /

  Indicates if the computation of the keyword was successful or not

* ``result``

  / *Type*: str /

  The result of the computation of the keyword
      """
      success = False
      result  = "UNKNOWN"
      if name is None:
         result = "parameter 'name' not defined"
         return success, result
      if description is None:
         result = "parameter 'description' not defined"
         return success, result
      if name in self.__dictGauges:
         result = f"a gauge with name '{name}' is already defined"
         return success, result
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
      success = True
      result  = f"gauge '{name}' added"
      return success, result
   # eof def add_gauge(...):

   @keyword
   def set_gauge(self, name=None, value=None, labels=None):
      """This keyword sets the value for a gauge. The gauge has to be added with '``add_gauge``' before.

**Arguments:**

* ``name``

  The name of the gauge

  / *Condition*: required / *Type*: str /

* ``value``

  The new value of the gauge.

  / *Condition*: optional / *Type*: int  / *Default*: None /

* ``labels``

  A semicolon separated list of labels assigned to the gauge. The order of labels must fit to the order of label names like defined in ``add_gauge``.

  / *Condition*: optional / *Type*: str  / *Default*: None /

**Returns:**

* ``success``

  / *Type*: bool /

  Indicates if the computation of the keyword was successful or not

* ``result``

  / *Type*: str /

  The result of the computation of the keyword
      """
      success = False
      result  = "UNKNOWN"
      if name is None:
         result = "parameter 'name' not defined"
         return success, result
      if name not in self.__dictGauges:
         result = f"gauge '{name}' not defined"
         return success, result
      if value is None:
         result = "parameter 'value' not defined"
         return success, result
      else:
         try:
            value = int(value)
         except Exception as ex:
            success = False
            result  = str(ex)
            return success, result
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
            success = False
            result  = str(ex)
            return success, result
      success = True
      listResults = []
      listResults.append(f"gauge '{name}' set to value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def set_gauge(...):

   @keyword
   def inc_gauge(self, name=None, value=None, labels=None):
      """This keyword increments a gauge. The gauge has to be added with '``add_gauge``' before.

**Arguments:**

* ``name``

  The name of the gauge

  / *Condition*: required / *Type*: str /

* ``value``

  The value of increment. If not given, the value of the gauge is incremented by value 1.

  / *Condition*: optional / *Type*: int  / *Default*: None /

* ``labels``

  A semicolon separated list of labels assigned to the gauge. The order of labels must fit to the order of label names like defined in ``add_gauge``.

  / *Condition*: optional / *Type*: str  / *Default*: None /

**Returns:**

* ``success``

  / *Type*: bool /

  Indicates if the computation of the keyword was successful or not

* ``result``

  / *Type*: str /

  The result of the computation of the keyword
      """
      success = False
      result  = "UNKNOWN"
      if name is None:
         result = "parameter 'name' not defined"
         return success, result
      if name not in self.__dictGauges:
         result = f"Gause '{name}' not defined"
         return success, result
      if value is not None:
         try:
            value = int(value)
         except Exception as ex:
            success = False
            result  = str(ex)
            return success, result
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
            success = False
            result  = str(ex)
            return success, result
      success = True
      listResults = []
      listResults.append(f"gauge '{name}' incremented")
      if value is not None:
         listResults.append(f"by value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def inc_gauge(...):

   @keyword
   def dec_gauge(self, name=None, value=None, labels=None):
      """This keyword decrements a gauge. The gauge has to be added with '``add_gauge``' before.

**Arguments:**

* ``name``

  The name of the gauge

  / *Condition*: required / *Type*: str /

* ``value``

  The value of decrement. If not given, the value of the gauge is decremented by value 1.

  / *Condition*: optional / *Type*: int  / *Default*: None /

* ``labels``

  A semicolon separated list of labels assigned to the gauge. The order of labels must fit to the order of label names like defined in ``add_gauge``.

  / *Condition*: optional / *Type*: str  / *Default*: None /

**Returns:**

* ``success``

  / *Type*: bool /

  Indicates if the computation of the keyword was successful or not

* ``result``

  / *Type*: str /

  The result of the computation of the keyword
      """
      success = False
      result  = "UNKNOWN"
      if name is None:
         result = "parameter 'name' not defined"
         return success, result
      if name not in self.__dictGauges:
         result = f"Gause '{name}' not defined"
         return success, result
      if value is not None:
         try:
            value = int(value)
         except Exception as ex:
            success = False
            result  = str(ex)
            return success, result
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
            success = False
            result  = str(ex)
            return success, result
      success = True
      listResults = []
      listResults.append(f"gauge '{name}' decremented")
      if value is not None:
         listResults.append(f"by value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def dec_gauge(...):


# eof class prometheus_interface():

