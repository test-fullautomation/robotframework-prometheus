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

*** Settings ***

# Robot Framework Built-In libraries
Library    Collections
Library    BuiltIn

# specific libraries
Library    RobotframeworkExtensions.Collection    WITH NAME    rf.extensions

# >>> Prometheus interface
# repository local Prometheus interface
Library    ../../PrometheusInterface/prometheus_interface.py    WITH NAME    rf.prometheus_interface
#
# installed Prometheus interface
# Library    %{ROBOTPYTHONSITEPACKAGESPATH}/PrometheusInterface/prometheus_interface.py    WITH NAME    rf.prometheus_interface
# <<< prometheus interface

Documentation    Simple test suite to set test values

*** Test Cases ***

Prometheus Set Values Test

   rf.prometheus_interface.add_counter    name=num_passed     description=: number of passed tests     labels=room;testbench
   rf.prometheus_interface.add_counter    name=num_failed     description=: number of failed tests     labels=room;testbench
   rf.prometheus_interface.add_counter    name=num_unknown    description=: number of unknown tests    labels=room;testbench

   rf.prometheus_interface.add_counter    name=num_counterparts    description=: number of counterparts    labels=room;testbench

   rf.prometheus_interface.add_gauge    name=temperature    description=: header temperature     labels=location;style
   rf.prometheus_interface.add_gauge    name=speed          description=: beats per minute       labels=location;style
   rf.prometheus_interface.add_gauge    name=collapses      description=: number of collapses    labels=location;style


   # --------------------------------------------------------------------------------------------------------------
   # >>>>> thread test
   # THREAD    ROOM_1     False
      # FOR    ${num_test_executions}    IN RANGE    1    600
         # rf.extensions.pretty_print    =========== num_test_executions: ${num_test_executions}
         # # with default increment (1):
         # rf.prometheus_interface.inc_counter    name=num_passed     labels=Room_1;Testbench_1
         # rf.prometheus_interface.inc_counter    name=num_failed     labels=Room_1;Testbench_1
         # rf.prometheus_interface.inc_counter    name=num_unknown    labels=Room_1;Testbench_1
         # # with increment set explicitly:
         # rf.prometheus_interface.inc_counter    name=num_counterparts    value=${1}    labels=Room_1;Testbench_1
         # rf.prometheus_interface.inc_counter    name=num_counterparts    value=${2}    labels=Room_2;Testbench_2
         # rf.prometheus_interface.inc_counter    name=num_counterparts    value=${3}    labels=Room_3;Testbench_3
         # sleep    1s
      # END
   # END

   # FOR    ${num_turntables}    IN RANGE    1    900
      # rf.extensions.pretty_print    =========== num_turntables: ${num_turntables}
      # rf.prometheus_interface.set_gauge    name=temperature    value=${num_turntables}    labels=Room_1;HipHop
      # rf.prometheus_interface.set_gauge    name=speed          value=${num_turntables}    labels=Room_1;Teckkno
      # rf.prometheus_interface.set_gauge    name=collapses      value=${num_turntables}    labels=Room_1;Trance
      # sleep    1s
   # END
   # <<<<< thread test
   # --------------------------------------------------------------------------------------------------------------

   # --------------------------------------------------------------------------------------------------------------
   # >>>>> version test

   ${me}   rf.prometheus_interface.who_am_i
   rf.extensions.pretty_print    =========== I am: ${me}

   ${location}   rf.prometheus_interface.where_am_i
   rf.extensions.pretty_print    =========== Located in: ${location}

   ${interfaceversion}   rf.prometheus_interface.get_version
   rf.extensions.pretty_print    =========== Version: ${interfaceversion}

   # <<<<< version test
   # --------------------------------------------------------------------------------------------------------------

