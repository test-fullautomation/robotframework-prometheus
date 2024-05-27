# generated at 27.05.2024 - 13:12:08

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-20-A
   rf.extensions.pretty_print    ==== Execution: 'I-20-A' / 'Suite-A-Test-10' : Room_1 / Testbench 1

   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_failed    labels=Room_1;Testbench 1;Suite-A-Test-10;FAILED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_gauge    name=beats_per_minute    value=180    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [set_gauge] (${success}) : ${result}

   rf.prometheus_interface.set_daylight

   sleep    2s

