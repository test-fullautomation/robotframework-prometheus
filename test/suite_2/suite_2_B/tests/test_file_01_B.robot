# generated at 17.10.2024 - 16:43:46

*** Settings ***
Resource    ../resources.resource
Documentation    Test file to set values for Prometheus

*** Test Cases ***

Prometheus Set Values Execution I-01-B
   rf.extensions.pretty_print    ==== Execution: 'I-01-B' / 'Suite-B-Test-01' : Room_1 / Testbench 2

   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_passed    labels=Room_1;Testbench 2;Suite-B-Test-01;PASSED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_counter    name=num_passed    value=2    labels=Room_1;Testbench 2;Suite-B-Test-01;PASSED
   rf.extensions.pretty_print    [inc_counter] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_gauge    name=beats_per_minute    value=55    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [set_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.inc_gauge    name=beats_per_minute    value=5    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [inc_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}
   ${success}    ${result}    rf.prometheus_interface.dec_gauge    name=beats_per_minute    value=2    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [dec_gauge] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_info    name=overview    info=test_name:Suite-B-Test-01;test_result:PASSED;file_number:F-1    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [set_info (overview)] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.set_info    name=lighting    info=lighting:nightlight    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [set_info (lighting)] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.observe_summary    name=summary_delay    value=1.1    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [observe_summary] (${success}) : ${result}

   ${success}    ${result}    rf.prometheus_interface.observe_histogram    name=histogram_delay    value=3.3    labels=Room_1;Testbench 2
   rf.extensions.pretty_print    [observe_histogram] (${success}) : ${result}

   sleep    2s

