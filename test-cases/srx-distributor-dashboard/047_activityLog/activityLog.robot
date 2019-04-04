*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Sorting Activity Log
    [Tags]                          Sorting
    Sorting React With Last Page    2
    Sorting React With Last Page    3
    Sorting React With Last Page    4
    Sorting React With Last Page    5
    Sorting React With Last Page    6
    Sorting React With Last Page    7
    Sorting React With Last Page    8

Filter Activity Log
    [Tags]                          Filter
    Filter Add For Select Box       1   2   Transaction
    Filter Add For Select Box       2   3   SPLIT
    Filter Add For Select Box       3   8   FAIL
    Filter Add For Select Box       4   5   HARDWARE

*** Keywords ***
Preparation
    Start Distributor
    Goto Sidebar Activity Feed
    Sleep                           5 second