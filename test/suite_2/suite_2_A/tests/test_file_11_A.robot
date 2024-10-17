# generated at 17.10.2024 - 16:43:46

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-11-A
   rf.extensions.pretty_print    ==== Execution: 'I-11-A' / 'Suite-A-Test-01' : Room_1 / Testbench 1

   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_failed    labels=Room_1;Testbench 1;Suite-A-Test-01;FAILED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_failed    value=2    labels=Room_1;Testbench 1;Suite-A-Test-01;FAILED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_gauge    name=beats_per_minute    value=180    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [set_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    value=5    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    value=2    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_info    name=overview    info=test_name:Suite-A-Test-01;test_result:FAILED;file_number:F-11    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [set_info (overview)] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_info    name=lighting    info=lighting:party    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [set_info (lighting)] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.observe_summary    name=summary_delay    value=2    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [observe_summary] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.observe_histogram    name=histogram_delay    value=4    labels=Room_1;Testbench 1
   rf.extensions.pretty_print    [observe_histogram] (${success}) : ${result}

   sleep    2s

