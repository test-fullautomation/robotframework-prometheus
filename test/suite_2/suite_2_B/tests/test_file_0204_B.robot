# generated at 23.05.2024 - 13:02:05

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-0204-B
   rf.extensions.pretty_print    === Execution: 'I-0204-B' / 'Suite-B-Test-04' : Room_1 / Testbench 2
   rf.extensions.pretty_print    >>> inc 'num_unknown' / beats_per_minute = 145 / testresult = UNKNOWN

   Inc Counter    name=num_unknown    labels=Room_1;Testbench 2;Suite-B-Test-04;UNKNOWN
   Set Gauge    name=beats_per_minute    value=145    labels=Room_1;Testbench 2

   sleep    4s

