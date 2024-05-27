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

# # >>> Prometheus interface
# # repository local Prometheus interface
# # Library    ../../../PrometheusInterface/prometheus_interface.py    port_number=${8002}    WITH NAME    rf.prometheus_interface
# #
# # installed Prometheus interface
Library    %{ROBOTPYTHONSITEPACKAGESPATH}/PrometheusInterface/prometheus_interface.py    port_number=${8002}    WITH NAME    rf.prometheus_interface
# # <<< prometheus interface

