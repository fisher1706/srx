*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
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