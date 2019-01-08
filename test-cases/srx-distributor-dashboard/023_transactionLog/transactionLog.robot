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
    Sort Column With Last Page      5
    Sort Column With Last Page      6
    Sort Column With Last Page      7
    Sort Column With Last Page      8
    Sort Column With Last Page      9
    Sleep                           3 second
    Open Full Table

Filter Transaction Log Part Number
    [Tags]                          Filter
    Filter Field                    1   2   CHANGE SKU 2

Filter Transaction Log DSN
    [Tags]                          Filter
    Filter Field                    2   4   G030PM036107NGQ5

Filter Transactions Action
    [Tags]                          Filter
    Filter Select Box               1   5   SPLIT

Filter Transactions Status
    [Tags]                          Filter
    Filter Select Box               2   6   DO_NOT_REORDER

Filter Transactions Submitted By
    [Tags]                          Filter
    Filter Select Box               3   7   CUSTOMER

Filter RFID Date
    [Tags]                          Filter      FilterDate
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[3]       11/1/2018, 9:03 A
    Input Text                      xpath:(${modal dialog}${form control})[4]       11/1/2018, 9:05 A
    Sleep                           5 second
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[9]/div      11/1/2018, 9:04 AM
    Click Element                   xpath:${button default}
    Sleep                           2 second

*** Keywords ***
Preparation
    Goto Transaction Log