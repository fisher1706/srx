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
    Sort Column With Last Page      1
    Sort Column With Last Page      2
    Sort Column With Last Page      3
    Sort Column With Last Page      4
    Sort Column With Last Page      6
    Sort Column With Last Page      7
    Sort Column With Last Page      8
    Sort Column With Last Page      9
    Sort Column With Last Page      10
    Sort Column With Last Page      11
    Sleep                           7 second

Filter Transactions Part Number
    [Tags]                          Filter
    Filter Field                    2   3   CHANGE SKU 2
    Sleep                           2 second

Filter Transactions Description
    [Tags]                          Filter
    Filter Field                    3   4   CHANGE SKU 2
    Sleep                           2 second

Filter Transactions Quantity
    [Tags]                          Filter
    Filter Field                    4   6   225
    Sleep                           2 second

Filter Transactions PO Number
    [Tags]                          Filter
    Filter Field                    5   7   0000
    Sleep                           2 second

Filter Transactions DSN
    [Tags]                          Filter
    Filter Field                    6   8   G030PM036107NGQ5
    Sleep                           2 second

Filter Transactions Submitted By
    [Tags]                          Filter      FilterSubmittedBy
    Filter Select Box               1   11  CUSTOMER

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Order Status
    Sleep                           3 second
    Open Minimum Table
    Sleep                           3 second
    Click Element                   xpath:${checkbox type}
    Sleep                           3 second
