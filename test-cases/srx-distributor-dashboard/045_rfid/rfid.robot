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
    Click Element                   xpath:(${react table raw}${button danger})[1]
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     ${epc}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ASSIGNED
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     ${email_dist}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second
    Reload Page
    Sleep                           7 second
    Select Location At Rfid Menu    Static Customer - 2048      STATIC SKU
    Sleep                           5 second
    ${previous epc}                 Get Text    xpath:(${react table column})[1]
    Should Not Be Equal As Strings  ${epc}      ${previous epc}

Sorting RFIDs
    [Tags]                          Sorting
    Sorting React With Last Page    1
    Sorting React With Last Page    2
    Sorting React With Last Page    3
    Sorting React With Last Page    4
    Sorting React With Last Page    5

Filter RFID
    [Tags]                          Filter
    Filter React Field              1   1   X1
    Filter React Field              2   4   SYSTEM
    Filter React Field              3   5   rfid1
    Filter React Select Box         1   2   ISSUED

Filter RFID Date
    [Tags]                          Filter      FilterDate
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[4]       2/4/2019, 2:21 P
    Input Text                      xpath:(${modal dialog}${form control})[5]       2/4/2019, 2:23 P
    Sleep                           2 second
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    Element Text Should Be          xpath:(${react table column})[3]      2/4/2019, 2:22 PM
    Click Element                   xpath:${button default}
    Sleep                           2 second

*** Keywords ***
Preparation
    Start Distributor
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    Static Customer - 2048      STATIC SKU
    Sleep                           5 second
