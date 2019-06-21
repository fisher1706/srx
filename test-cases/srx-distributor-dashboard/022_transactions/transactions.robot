*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Sorting Transactions
    [Tags]                          Sorting
    Sorting React With Last Page    1
    Sorting React With Last Page    2
    Sorting React With Last Page    3
    Sorting React With Last Page    4
    Sorting React With Last Page    6
    Sorting React With Last Page    7
    Sorting React With Last Page    8
    Sorting React With Last Page    9
    Sorting React With Last Page    10
    Sorting React With Last Page    11
    Sleep                           7 second

Filter Transactions Part Number
    Filter Add                      2   1   92-71
    Filter Add                      3   3   USAGE HISTORY
    Filter Add                      4   4   USAGE HISTORY
    Filter Add                      5   6   218
    Filter Add                      6   7   0000
    Filter Add                      7   8   G030PM036107NGQ5
    Filter Add For Select Box       8   11  CUSTOMER

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Order Status
    Sleep                           3 second
    Click Element                   xpath:${close button}
    Sleep                           5 second
