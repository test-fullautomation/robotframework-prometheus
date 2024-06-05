# generated at 05.06.2024 - 17:13:37

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-17-A
   rf.extensions.pretty_print    ==== Execution: 'I-17-A' / 'Suite-A-Test-07' : Room_1 / Testbench 1

   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_failed    labels=Room_1;Testbench 1;Suite-A-Test-07;FAILED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_failed    value=2    labels=Room_1;Testbench 1;Suite-A-Test-07;FAILED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_gauge    name=beats_per_minute    value=20    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [set_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    value=5    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    value=2    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_info    name=overview    info=test_name:Suite-A-Test-07;test_result:FAILED;file_number:F-17    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [set_info] (${success}) : ${result}

   # rf.prometheus_interface.set_nightlight

   sleep    2s

