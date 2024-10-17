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
Documentation    Setup and teardown of suite, including the setup of Prometheus interface

Resource    ./resources.resource

Library    RobotFramework_TestsuitesManagement    WITH NAME    tm

Suite Setup       Prometheus Suite Setup
Suite Teardown    Prometheus Suite Teardown

*** Keywords ***

Prometheus Suite Setup
    [Documentation]    Prometheus Suite Setup

    rf.extensions.pretty_print    =========== executing Prometheus Suite Setup

    # setup of TestsuitesManagement
    tm.testsuite_setup    ./config/variants_config.json

    # prometheus interface information
    ${me}   rf.prometheus_interface.who_am_i
    rf.extensions.pretty_print    [INTERFACE INFO] I am: ${me}

    ${location}   rf.prometheus_interface.where_am_i
    rf.extensions.pretty_print    [INTERFACE INFO] Located in: ${location}

    ${port_number}   rf.prometheus_interface.get_port_number
    rf.extensions.pretty_print    [INTERFACE INFO] Working with port: ${port_number}

    # setup of Prometheus counter and gauges
    ${success}    ${result}    rf.prometheus_interface.add_counter    name=num_passed     description=: number of passed tests     labels=room;testbench;testname;testresult
    rf.extensions.pretty_print    [add_counter] (${success}) : ${result}
    ${success}    ${result}    rf.prometheus_interface.add_counter    name=num_failed     description=: number of failed tests     labels=room;testbench;testname;testresult
    rf.extensions.pretty_print    [add_counter] (${success}) : ${result}
    ${success}    ${result}    rf.prometheus_interface.add_counter    name=num_unknown    description=: number of unknown tests    labels=room;testbench;testname;testresult
    rf.extensions.pretty_print    [add_counter] (${success}) : ${result}

    ${success}    ${result}    rf.prometheus_interface.add_gauge    name=beats_per_minute    description=: current beats per minute     labels=room;testbench
    rf.extensions.pretty_print    [add_gauge] (${success}) : ${result}

    ${success}    ${result}    rf.prometheus_interface.add_info    name=overview    description=: The overview about the test sytem     labels=room;testbench
    rf.extensions.pretty_print    [add_info] (${success}) : ${result}

    ${success}    ${result}    rf.prometheus_interface.add_info    name=lighting    description=: The kind of lighting     labels=room;testbench
    rf.extensions.pretty_print    [add_info] (${success}) : ${result}

    ${success}    ${result}    rf.prometheus_interface.add_summary    name=summary_delay    description=: summary test delays     labels=room;testbench
    rf.extensions.pretty_print    [add_summary] (${success}) : ${result}

    ${success}    ${result}    rf.prometheus_interface.add_histogram    name=histogram_delay    description=: histogram test delays     labels=room;testbench
    rf.extensions.pretty_print    [add_histogram] (${success}) : ${result}


Prometheus Suite Teardown
    [Documentation]    Prometheus Suite Teardown

    rf.extensions.pretty_print    =========== executing Prometheus Suite Teardown
