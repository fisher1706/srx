*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Create RFID
    Click Element                   ${create button}
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Input By Name                   labelId     ${epc}
    Click Element                   xpath:${button submit}

Checking RFID
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ASSIGNED
    Element Text Should Be          xpath:(${react table column})[4]      ${email_dist}

Update RFID
    Click Element                   xpath:(${react table raw}${edit status})[1]
    Sleep                           3 second
    Click Element                   xpath:(${react modal dialog}${role button})[5]

Checking Updated RFID
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      MANIFEST
    Element Text Should Be          xpath:(${react table column})[4]      ${email_dist}

Checking Updated RFID In Activity Log
    Goto Sidebar Activity Feed
    Sleep                           2 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]     RFID
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]     RFID_TAG_UPDATE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]     USER
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]     SUCCESS

Unassign RFID
    Goto Sidebar RFID
    Sleep                           2 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           3 second
    Click Element                   xpath:(${react table raw}${unassign rfid})[1]
    Element Text Should Be          xpath:${dialog}//table/tbody/tr/td[1]     ${epc}
    Element Text Should Be          xpath:${dialog}//table/tbody/tr/td[2]     MANIFEST
    Element Text Should Be          xpath:${dialog}//table/tbody/tr/td[4]     ${email_dist}
    Click Element                   xpath:(${dialog}${button})[2]
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
