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
    Sleep                           3 second
    Open Full Table
    Sleep                           4 second

Filter Transactions Part Number
    [Tags]                          Filter
    Filter Field                    1   2   CHANGE SKU 2

Filter Transactions Description
    [Tags]                          Filter
    Filter Field                    2   3   CHANGE SKU 2

Filter Transactions Quantity
    [Tags]                          Filter
    Filter Field                    3   5   225

Filter Transactions PO Number
    [Tags]                          Filter
    Filter Field                    4   6   0000

Filter Transactions DSN
    [Tags]                          Filter
    Filter Field                    5   7   G030PM036107NGQ5

Filter Transactions Submitted By
    [Tags]                          Filter      FilterSubmittedBy
    Sleep                           4 second
    Filter Select Box               1   10  CUSTOMER

*** Keywords ***
Preparation
    Goto Transactions
    Click Element                   xpath:${checkbox type}
    Sleep                           3 second
