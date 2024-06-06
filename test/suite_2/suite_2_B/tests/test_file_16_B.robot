# generated at 05.06.2024 - 17:13:37

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-16-B
   rf.extensions.pretty_print    ==== Execution: 'I-16-B' / 'Suite-B-Test-06' : Room_1 / Testbench 2

   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_passed    labels=Room_1;Testbench 2;Suite-B-Test-06;PASSED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_passed    value=2    labels=Room_1;Testbench 2;Suite-B-Test-06;PASSED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_gauge    name=beats_per_minute    value=165    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [set_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    value=5    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    value=2    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_info    name=overview    info=test_name:Suite-B-Test-06;test_result:PASSED;file_number:F-16    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [set_info] (${success}) : ${result}

   # rf.prometheus_interface.set_nightlight

   sleep    2s

