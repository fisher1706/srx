*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Invalid Create New Market Type
    [Tags]                          InvalidCreateNewCustomer
    Click Element                   xpath:${button primary}
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Is Market Types
    Click Element                   xpath:${button primary}
    Press Key                       id:name_id                      \ue004
    Element Should Be Enabled       css:.fa-exclamation-circle > path:nth-child(1)
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second
    Is Market Types

Valid Create New Market Type
    [Tags]                          ValidCreateNewCustomer
    Click Element                   xpath:${button primary}
    Input Text                      id:name_id                      ${market type}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           1 second
    Is Market Types

Checking New Market Type In Table
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div          ${market type}

Checking New Market Type On Distributor Portal
    [Tags]                          CheckingOnDistributorPortal
    Goto Customer Menu Sub
    ${current type}                 Get Text    xpath:((${react table raw})[1]${react table column})[5]
    Click Element                   xpath:(${react table raw})[1]
    Select From Dropdown            (${dropdown menu})[2]       ${market type}
    Click Element                   xpath:${button submit}
    Goto Sidebar Customers
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]     ${market type}
    Click Element                   xpath:(${react table raw})[1]
    Select From Dropdown            (${dropdown menu})[2]       ${current type}
    Click Element                   xpath:${button submit}
    Goto Sidebar Customers
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]     ${current type}
    Finish Suite

Edit Market Type
    Sleep                           5 second
    Preparation
    Click Element                   ${edit button}
    Sleep                           2 second
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Is Market Types
    Click Element                   ${edit button}
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second
    Is Market Types
    Click Element                   ${edit button}
    Input Text                      id:name_id                      ${edit market type}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           1 second
    Is Market Types

Delete Market Type
    Click Element                   ${delete button}
    Sleep                           1 second
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Is Market Types
    Click Element                   ${delete button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Is Market Types
    Click Element                   ${delete button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]          ${edit market type}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           7 second

Sorting Market Types By Id
    [Tags]                          Sorting
    Click Element                   css:th.sort-column:nth-child(1)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[1]/div
    Click Element                   css:th.sort-column:nth-child(1)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}-1]/td[1]/div
    Should Be Equal                 ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(1)

Sorting Market Types By Type
    [Tags]                          Sorting
    Click Element                   css:th.sort-column:nth-child(2)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[2]/div
    Click Element                   css:th.sort-column:nth-child(2)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}-1]/td[2]/div
    Should Be Equal                 ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(2)

*** Keywords ***
Goto Customer Menu Sub
    Finish Suite
    Start Distributor
    Sleep                           4 second
    Goto Sidebar Customers
    Sleep                           5 second

Preparation
    Start Admin
    Sleep                           3 second
    Click Link                      xpath://*[@href="/market-types"]
    Sleep                           1 second
    ${number of row}                Get Rows Count                  ${table xpath}
    ${number of new row}=           Evaluate                        ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${edit button}                  xpath:${table xpath}/tbody/tr[${number of row}]${button success}
    Set Suite Variable              ${delete button}                xpath:${table xpath}/tbody/tr[${number of row}]${button danger}