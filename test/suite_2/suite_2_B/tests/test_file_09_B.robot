# generated at 05.06.2024 - 17:13:37

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-09-B
   rf.extensions.pretty_print    ==== Execution: 'I-09-B' / 'Suite-B-Test-09' : Room_1 / Testbench 2

   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_unknown    labels=Room_1;Testbench 2;Suite-B-Test-09;UNKNOWN
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_unknown    value=2    labels=Room_1;Testbench 2;Suite-B-Test-09;UNKNOWN
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_gauge    name=beats_per_minute    value=205    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [set_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    value=5    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    value=2    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_info    name=overview    info=test_name:Suite-B-Test-09;test_result:UNKNOWN;file_number:F-9    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [set_info] (${success}) : ${result}

   # rf.prometheus_interface.set_nightlight

   sleep    2s

