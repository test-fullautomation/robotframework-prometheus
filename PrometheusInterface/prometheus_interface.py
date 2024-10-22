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
from prometheus_client import start_http_server, Gauge, Counter, Info, Summary, Histogram

# -- import Robotframework API
from robot.api.deco import keyword, library # required when using @keyword, @library decorators
from robot.libraries.BuiltIn import BuiltIn

# -- import some helpers
from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Utils.CUtils import *

# --------------------------------------------------------------------------------------------------------------
# this interface library
#
LIBRARY_VERSION      = "0.8.0"
LIBRARY_VERSION_DATE = "21.10.2024"
#
THISMODULENAME = "prometheus_interface.py"
THISMODULE     = f"{THISMODULENAME} v. {LIBRARY_VERSION} / {LIBRARY_VERSION_DATE}"
#
DEFAULT_PORT = 8000
#
DEFAULT_MESSAGE_LEVEL = "INFO"
#
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

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def __init__(self, port_number=DEFAULT_PORT, message_level=DEFAULT_MESSAGE_LEVEL):
      self.__sMessageLevel = message_level
      self.__port_number   = port_number

      # prometheus metric types
      self.__dictCounter    = {}
      self.__dictGauges     = {}
      self.__dictInfos      = {}
      self.__dictSummaries  = {}
      self.__dictHistograms = {}

      start_http_server(self.__port_number)

      # default info metric about this interface library
      oInfo = Info("Prometheus_interface", "Prometheus interface info")
      dictInfo = {}
      dictInfo['file_name'] = THISMODULENAME
      dictInfo['version']   = LIBRARY_VERSION
      dictInfo['date']      = LIBRARY_VERSION_DATE
      dictInfo['location']  = self.where_am_i()
      oInfo.info(dictInfo)


   def __del__(self):
      del self.__dictCounter
      del self.__dictGauges
      del self.__dictInfos
      del self.__dictSummaries

   # --------------------------------------------------------------------------------------------------------------

   def convert_to_int_or_float(self, value):
      """Little helper to convert a string value to an integer or a float
      """
      try:
         converted_value = int(value)
         return converted_value # is int
      except ValueError:
         pass
      try:
         converted_value = float(value)
         return converted_value # is float
      except ValueError:
         pass
      return None # not int and not float

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
      """Returns path to this interface library
      """
      location = CString.NormalizePath(os.path.dirname(os.path.abspath(__file__)))
      return location

   @keyword
   def get_port_number(self):
      """Returns the port number assigned to this instance of the library
      """
      return self.__port_number


   # --------------------------------------------------------------------------------------------------------------
   # -- prometheus metric type 'Info'
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def add_info(self, name=None, description=None, labels=None):
      """This keyword adds a new info. The content of an existing info can be defined with ``set_info``.

**Arguments:**

* ``name``

  The name of the new info

  / *Condition*: required / *Type*: str /

* ``description``

  The description of the new info

  / *Condition*: required / *Type*: str /

* ``labels``

  A semicolon separated list of label names assigned to the new info

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
         result = "Parameter 'name' not defined"
         return success, result
      if description is None:
         result = "Parameter 'description' not defined"
         return success, result
      if name in self.__dictInfos:
         result = f"An info with name '{name}' is already defined"
         return success, result
      oInfo = None
      if labels is None:
         oInfo = Info(name, description)
      else:
         labellist = labels.split(';')
         listLabelNames = []
         for label in labellist:
            label = label.strip()
            listLabelNames.append(label)
         oInfo = Info(name, description, listLabelNames)
      self.__dictInfos[name] = oInfo
      success = True
      listResults = []
      listResults.append(f"Info '{name}' added")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result

   @keyword
   def set_info(self, name=None, info=None, labels=None):
      """This keyword defines the content of an info. The info has to be added with '``add_info``' before.

**Arguments:**

* ``name``

  The name of the info

  / *Condition*: required / *Type*: str /

* ``info``

  The info itself (every info is a key-value information).

  / *Condition*: required / *Type*: dict /

* ``labels``

  A semicolon separated list of labels assigned to the info. The order of labels must fit to the order of label names like defined in ``add_info``.

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
         result = "Parameter 'name' not defined"
         return success, result
      if info is None:
         result = "Parameter 'info' not defined"
         return success, result
      if name not in self.__dictInfos:
         result = f"Info '{name}' not defined"
         return success, result
      dictInfo = {}
      list_splitparts = info.split(';')
      for splitpart in list_splitparts:
         splitpart = splitpart.strip()
         list_splitparts2 = splitpart.split(':')
         if len(list_splitparts2) != 2:
            success = False
            result  = "Syntax error in parameter 'info' of '{name}': missing delimiter"
            return success, result
         param_name = list_splitparts2[0].strip()
         if param_name == "":
            success = False
            result  = "Syntax error in parameter 'info' of '{name}': parameter name is empty"
            return success, result
         param_value = list_splitparts2[1].strip()
         if param_value == "":
            success = False
            result  = "Syntax error in parameter 'info' of '{name}': parameter value is empty"
            return success, result
         dictInfo[param_name] = str(param_value)
      oInfo = self.__dictInfos[name]
      if labels is None:
         oInfo.info(dictInfo)
      else:
         labellist = labels.split(';')
         listLabelValues = []
         for label in labellist:
            label = label.strip()
            listLabelValues.append(label)
         oInfo.labels(*listLabelValues).info(dictInfo)
      success = True
      listResults = []
      listResults.append(f"Info '{name}' set to'{info}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result


   # --------------------------------------------------------------------------------------------------------------
   # -- prometheus metric type 'Counter'
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
         result = "Parameter 'name' not defined"
         return success, result
      if description is None:
         result = "Parameter 'description' not defined"
         return success, result
      if name in self.__dictCounter:
         result = f"A counter with name '{name}' is already defined"
         return success, result
      oCounter = None
      if labels is None:
         oCounter = Counter(name, description)
      else:
         labellist = labels.split(';')
         listLabelNames = []
         for label in labellist:
            label = label.strip()
            listLabelNames.append(label)
         oCounter = Counter(name, description, listLabelNames)
      self.__dictCounter[name] = oCounter
      success = True
      listResults = []
      listResults.append(f"Counter '{name}' added")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
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
         result = "Parameter 'name' not defined"
         return success, result
      if name not in self.__dictCounter:
         result = f"Counter '{name}' not defined"
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
         listLabelValues = []
         for label in labellist:
            label = label.strip()
            listLabelValues.append(label)
         if value is None:
            oCounter.labels(*listLabelValues).inc()
         else:
            oCounter.labels(*listLabelValues).inc(value)
      success = True
      listResults = []
      listResults.append(f"Counter '{name}' incremented")
      if value is not None:
         listResults.append(f"by value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def inc_counter(...):


   # --------------------------------------------------------------------------------------------------------------
   # -- prometheus metric type 'Gauge'
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
         result = "Parameter 'name' not defined"
         return success, result
      if description is None:
         result = "Parameter 'description' not defined"
         return success, result
      if name in self.__dictGauges:
         result = f"A gauge with name '{name}' is already defined"
         return success, result
      oGauge = None
      if labels is None:
         oGauge = Gauge(name, description)
      else:
         labellist = labels.split(';')
         listLabelNames = []
         for label in labellist:
            label = label.strip()
            listLabelNames.append(label)
         oGauge = Gauge(name, description, listLabelNames)
      self.__dictGauges[name] = oGauge
      success = True
      listResults = []
      listResults.append(f"Gauge '{name}' added")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
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
         result = "Parameter 'name' not defined"
         return success, result
      if name not in self.__dictGauges:
         result = f"Gauge '{name}' not defined"
         return success, result
      if value is None:
         result = "Parameter 'value' not defined"
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
         listLabelValues = []
         for label in labellist:
            label = label.strip()
            listLabelValues.append(label)
         oGauge.labels(*listLabelValues).set(value)
      success = True
      listResults = []
      listResults.append(f"Gauge '{name}' set to value '{value}'")
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
         result = "Parameter 'name' not defined"
         return success, result
      if name not in self.__dictGauges:
         result = f"Gauge '{name}' not defined"
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
         listLabelValues = []
         for label in labellist:
            label = label.strip()
            listLabelValues.append(label)
         if value is None:
            oGauge.labels(*listLabelValues).inc()
         else:
            oGauge.labels(*listLabelValues).inc(value)
      success = True
      listResults = []
      listResults.append(f"Gauge '{name}' incremented")
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
         result = "Parameter 'name' not defined"
         return success, result
      if name not in self.__dictGauges:
         result = f"Gauge '{name}' not defined"
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
         listLabelValues = []
         for label in labellist:
            label = label.strip()
            listLabelValues.append(label)
         if value is None:
            oGauge.labels(*listLabelValues).dec()
         else:
            oGauge.labels(*listLabelValues).dec(value)
      success = True
      listResults = []
      listResults.append(f"Gauge '{name}' decremented")
      if value is not None:
         listResults.append(f"by value '{value}'")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def dec_gauge(...):


   # --------------------------------------------------------------------------------------------------------------
   # -- prometheus metric type 'Summary'
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def add_summary(self, name=None, description=None, labels=None):
      """This keyword adds a new summary. The values of existing summaries can be set with ``observe_summary```.

**Arguments:**

* ``name``

  The name of the new summary

  / *Condition*: required / *Type*: str /

* ``description``

  The description of the new summary

  / *Condition*: required / *Type*: str /

* ``labels``

  A semicolon separated list of label names assigned to the new summary

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
         result = "Parameter 'name' not defined"
         return success, result
      if description is None:
         result = "Parameter 'description' not defined"
         return success, result
      if name in self.__dictSummaries:
         result = f"A summary with name '{name}' is already defined"
         return success, result
      oSummary = None
      if labels is None:
         oSummary = Summary(name, description)
      else:
         labellist = labels.split(';')
         listLabelNames = []
         for label in labellist:
            label = label.strip()
            listLabelNames.append(label)
         oSummary = Summary(name, description, listLabelNames)
      self.__dictSummaries[name] = oSummary
      success = True
      listResults = []
      listResults.append(f"Summary '{name}' added")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def add_summary(...):

   @keyword
   def observe_summary(self, name=None, value=None, labels=None):
      """This keyword observes a summary. The summary has to be added with '``add_summary``' before.

**Arguments:**

* ``name``

  The name of the summary

  / *Condition*: required / *Type*: str /

* ``value``

  The value assigned to the summary.

  / *Condition*: required / *Type*: int or float /

* ``labels``

  A semicolon separated list of labels assigned to the summary. The order of labels must fit to the order of label names like defined in ``add_summary``.

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
         result = "Parameter 'name' not defined"
         return success, result
      if value is None:
         result = "Parameter 'value' not defined"
         return success, result
      value_type = type(value)
      value = self.convert_to_int_or_float(value)
      if value is None:
         success = False
         result  = f"invalid type '{value_type}' of input parameter 'value'; expected int or float"
         return success, result
      if name not in self.__dictSummaries:
         result = f"Summary '{name}' not defined"
         return success, result
      oSummary = self.__dictSummaries[name]
      if labels is None:
         oSummary.observe(value)
      else:
         labellist = labels.split(';')
         listLabelValues = []
         for label in labellist:
            label = label.strip()
            listLabelValues.append(label)
         oSummary.labels(*listLabelValues).observe(value)
      success = True
      listResults = []
      listResults.append(f"Summary '{name}' observed value {value}")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def observe_summary(...):


   # --------------------------------------------------------------------------------------------------------------
   # -- prometheus metric type 'Histogram'
   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def add_histogram(self, name=None, description=None, labels=None):
      """This keyword adds a new histogram. The values of existing histograms can be set with ``observe_histogram```.

**Arguments:**

* ``name``

  The name of the new histogram

  / *Condition*: required / *Type*: str /

* ``description``

  The description of the new histogram

  / *Condition*: required / *Type*: str /

* ``labels``

  A semicolon separated list of label names assigned to the new histogram

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
         result = "Parameter 'name' not defined"
         return success, result
      if description is None:
         result = "Parameter 'description' not defined"
         return success, result
      if name in self.__dictHistograms:
         result = f"A histogram with name '{name}' is already defined"
         return success, result
      oHistogram = None
      if labels is None:
         oHistogram = Histogram(name, description)
      else:
         labellist = labels.split(';')
         listLabelNames = []
         for label in labellist:
            label = label.strip()
            listLabelNames.append(label)
         oHistogram = Histogram(name, description, listLabelNames)
      self.__dictHistograms[name] = oHistogram
      success = True
      listResults = []
      listResults.append(f"Summary '{name}' added")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def add_histogram(...):

   @keyword
   def observe_histogram(self, name=None, value=None, labels=None):
      """This keyword observes a histogram. The histogram has to be added with '``add_histogram``' before.

**Arguments:**

* ``name``

  The name of the histogram

  / *Condition*: required / *Type*: str /

* ``value``

  The value assigned to the histogram.

  / *Condition*: required / *Type*: int or float /

* ``labels``

  A semicolon separated list of labels assigned to the histogram. The order of labels must fit to the order of label names like defined in ``add_histogram``.

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
         result = "Parameter 'name' not defined"
         return success, result
      if value is None:
         result = "Parameter 'value' not defined"
         return success, result
      value_type = type(value)
      value = self.convert_to_int_or_float(value)
      if value is None:
         success = False
         result  = f"invalid type '{value_type}' of input parameter 'value'; expected int or float"
         return success, result
      if name not in self.__dictHistograms:
         result = f"Histogram '{name}' not defined"
         return success, result
      oHistogram = self.__dictHistograms[name]
      if labels is None:
         oHistogram.observe(value)
      else:
         labellist = labels.split(';')
         listLabelValues = []
         for label in labellist:
            label = label.strip()
            listLabelValues.append(label)
         oHistogram.labels(*listLabelValues).observe(value)
      success = True
      listResults = []
      listResults.append(f"Histogram '{name}' observed value {value}")
      if labels is not None:
         listResults.append(f"with labels: '{labels}'")
      result = " ".join(listResults)
      return success, result
   # eof def observe_histogram(...):

# eof class prometheus_interface():

