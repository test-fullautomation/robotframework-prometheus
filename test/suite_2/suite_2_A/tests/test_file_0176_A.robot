# generated at 23.05.2024 - 13:02:05

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-0176-A
   rf.extensions.pretty_print    === Execution: 'I-0176-A' / 'Suite-A-Test-06' : Room_1 / Testbench 1
   rf.extensions.pretty_print    >>> inc 'num_failed' / beats_per_minute = 120 / testresult = FAILED

   Inc Counter    name=num_failed    labels=Room_1;Testbench 1;Suite-A-Test-06;FAILED
   Set Gauge    name=beats_per_minute    value=120    labels=Room_1;Testbench 1

   sleep    4s

