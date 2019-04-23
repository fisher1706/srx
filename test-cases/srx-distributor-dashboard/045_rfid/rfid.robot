*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Create RFID
    Click Element                   xpath:${add rfid button}
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Input Text                      id:labelId_id               ${epc}
    Click Element                   xpath:${modal dialog}${button primary}

Checking RFID
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ASSIGNED
    Element Text Should Be          xpath:(${react table column})[4]      ${email_dist}

Unassign RFID
    Click Element                   xpath:(${react table raw}${unassign rfid})[1]
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     ${epc}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ASSIGNED
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     ${email_dist}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second
    Reload Page
    Sleep                           7 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    ${previous epc}                 Get Text    xpath:(${react table column})[1]
    Should Not Be Equal As Strings  ${epc}      ${previous epc}

Sorting RFIDs
    [Tags]                          Sort
    Sorting React With Last Page    1
    Sorting React With Last Page    2
    Sorting React With Last Page    3
    Sorting React With Last Page    4
    Sorting React With Last Page    5

Filter RFID
    [Tags]                          Filter
    Filter Add                      1       1       WKYSPCTYJIXSTVPSXC
    Filter Add                      3       4       SYSTEM
    Filter Add                      4       5       TestDATA
    Filter Add For Select Box       2       2       ASSIGNED

*** Keywords ***
Preparation
    Start Distributor
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
