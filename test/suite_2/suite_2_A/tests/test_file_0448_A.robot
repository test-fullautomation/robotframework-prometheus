# generated at 23.05.2024 - 13:02:05

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-0448-A
   rf.extensions.pretty_print    === Execution: 'I-0448-A' / 'Suite-A-Test-08' : Room_1 / Testbench 1
   rf.extensions.pretty_print    >>> inc 'num_passed' / beats_per_minute = 10 / testresult = PASSED

   Inc Counter    name=num_passed    labels=Room_1;Testbench 1;Suite-A-Test-08;PASSED
   Set Gauge    name=beats_per_minute    value=10    labels=Room_1;Testbench 1

   sleep    4s

