*** Settings ***
Resource    ../resources.resource
Documentation    Prometheus test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Test 034
   rf.extensions.pretty_print    =========== Prometheus Set Values Test 034 / set values for Room_1/Testbench 1
   Inc Counter    name=num_passed    labels=Room_1;Testbench 1
   Set Gauge      name=beats_per_minute    value=10    labels=Room_1;Testbench 1
   sleep    2s

