*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Create New Customer
    Click Element                   ${create button}
    Input By Name                   name            ${user first name}
    ${customer type}                Select First    (${dropdown menu})[1]
    Set Suite Variable              ${customer type}
    ${market type}                  Select First    (${dropdown menu})[2]
    Set Suite Variable              ${market type}
    ${warehouse}                    Select First    (${dropdown menu})[3]
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking New Customer
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[2]      ${EMPTY}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[4]      ${customer type}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]      ${market type}

Edit Customer
    Click Element                   xpath:(${react table raw})[${number of new row}]
    Input By Name                   name            ${user last name}
    Input By Name                   number          ${warehouse number}
    ${edit customer type}           Select First    (${dropdown menu})[1]
    Set Suite Variable              ${edit customer type}
    ${edit market type}             Select First    (${dropdown menu})[2]
    Set Suite Variable              ${edit market type}
    Input By Name                   notes           Note
    Click Element                   xpath:${button submit}
    Sleep                           3 second

Checking Customer
    Goto Sidebar Customers
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[2]      ${warehouse number}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[4]      ${edit customer type}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]      ${edit market type}

Delete Customer
    Click Element                   xpath:(${react table raw})[${number of new row}]${delete customer}
    Dialog Should Be About          ${user last name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Security Groups
    Sleep                           3 second
    ${permission test group}        Get Row By Text     (${table xpath})[2]     1       Permissions Test
    Set Suite Variable              ${edit group button}            xpath:(${table xpath})[2]/tbody/tr[${permission test group}]${button success}
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  8       1
    Click Element                   xpath:(${dialog tab})[2]
    Clear All Settings Permissions
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           3 second
    Finish Suite
    Sleep                           3 second
    Start Permission
    Sleep                           3 second
    Goto Sidebar Customers
    ${number of row}                Get Element Count           xpath:${react table raw}
    Set Suite Variable              ${number of row}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of new row}