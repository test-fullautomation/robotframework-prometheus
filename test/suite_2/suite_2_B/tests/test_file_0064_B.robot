# generated at 23.05.2024 - 13:02:05

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-0064-B
   rf.extensions.pretty_print    === Execution: 'I-0064-B' / 'Suite-B-Test-04' : Room_1 / Testbench 2
   rf.extensions.pretty_print    >>> inc 'num_passed' / beats_per_minute = 55 / testresult = PASSED

   Inc Counter    name=num_passed    labels=Room_1;Testbench 2;Suite-B-Test-04;PASSED
   Set Gauge    name=beats_per_minute    value=55    labels=Room_1;Testbench 2

   sleep    4s

