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
    Sort Column With Last Page      5
    Sort Column With Last Page      6
    Sort Column With Last Page      7
    Sort Column With Last Page      8
    Sort Column With Last Page      9
    Sort Column With Last Page      10
    Sleep                           7 second

Filter Transactions Part Number
    [Tags]                          Filter
    Filter Field                    1   2   CHANGE SKU 2
    Sleep                           2 second

Filter Transactions Description
    [Tags]                          Filter
    Filter Field                    2   3   CHANGE SKU 2
    Sleep                           2 second

Filter Transactions Quantity
    [Tags]                          Filter
    Filter Field                    3   5   225
    Sleep                           2 second

Filter Transactions PO Number
    [Tags]                          Filter
    Filter Field                    4   6   0000
    Sleep                           2 second

Filter Transactions DSN
    [Tags]                          Filter
    Filter Field                    5   7   G030PM036107NGQ5
    Sleep                           2 second

Filter Transactions Submitted By
    [Tags]                          Filter      FilterSubmittedBy
    Filter Select Box               1   10  CUSTOMER

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Click Link                      xpath://*[@href="/order-status"]
    Sleep                           5 second
    Click Element                   xpath:${checkbox type}
    Sleep                           3 second
