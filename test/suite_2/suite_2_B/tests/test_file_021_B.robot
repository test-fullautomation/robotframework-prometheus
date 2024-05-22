*** Settings ***
Resource    ../resources.resource
Documentation    Prometheus test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Test 021
   rf.extensions.pretty_print    =========== Prometheus Set Values Test 021 / set values for Room_1/Testbench 2
   Inc Counter    name=num_unknown    labels=Room_1;Testbench 2
   Set Gauge      name=beats_per_minute    value=15    labels=Room_1;Testbench 2
   sleep    2s

