*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Invalid Create New Customer Type
    [Tags]                          InvalidCreateNewCustomer
    Click Link                      xpath://*[@href="/customer-types"]
    Sleep                           1 second
    Click Element                   xpath:${button info}
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   xpath:${button info}
    Press Key                       id:name_id                      \ue004
    Element Should Be Enabled       css:.fa-exclamation-circle > path:nth-child(1)
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second

Valid Create New Customer Type
    Click Element                   xpath:${button info}
    Input Text                      id:name_id                      ${test type}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    ${my customer type}             Get Rows Count                  ${table xpath}
    Set Suite Variable              ${my customer type}
    Set Suite Variable              ${edit customer type}           xpath:${table xpath}/tbody/tr[${my customer type}]${button success}
    Set Suite Variable              ${delete customer type}         xpath:${table xpath}/tbody/tr[${my customer type}]${button danger}

Checking New Customer Type In Table
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my customer type}]/td[2]/div        ${test type}

Invalid Create New Market Type
    [Tags]                          InvalidCreateNewCustomer
    Click Link                      xpath://*[@href="/market-types"]
    Sleep                           1 second
    Click Element                   xpath:${button info}
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   xpath:${button info}
    Press Key                       id:name_id                      \ue004
    Element Should Be Enabled       css:.fa-exclamation-circle > path:nth-child(1)
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second

Valid Create New Market Type
    [Tags]                          ValidCreateNewCustomer
    Click Element                   xpath:${button info}
    Input Text                      id:name_id                      ${market type}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    ${my market type}               Get Rows Count                  ${table xpath}
    Set Suite Variable              ${my market type}
    Set Suite Variable              ${edit market type button}      xpath:${table xpath}/tbody/tr[${my market type}]${button success}
    Set Suite Variable              ${delete market type button}    xpath:${table xpath}/tbody/tr[${my market type}]${button danger}

Checking New Market Type In Table
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my market type}]/td[2]/div          ${market type}

Checking New Types On Distributor Portal
    [Tags]                          CheckingOnDistributorPortal
    Goto Customer Menu Sub
    Click Element                   xpath:(${react table raw})[1]
    Select From Dropdown            (${dropdown menu})[1]       ${test type}
    Select From Dropdown            (${dropdown menu})[2]       ${market type}
    Click Element                   xpath:${button submit}
    Goto Sidebar Customers
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]     ${test type}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]     ${market type}
    Finish Suite
    Sleep                           5 second

Delete Customer Type Not Delete
    Preparation
    Click Link                      xpath://*[@href="/customer-types"]
    Sleep                           1 second
    Click Element                   ${delete customer type}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]         ${test type}
    Click Element                   xpath:${modal dialog}${button danger}
    Element Text Should Be          css:.external-page-alert > strong:nth-child(2)              Operation failed!
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second

Edit Customer Type
    Click Element                   ${edit customer type}
    Input Text                      id:name_id                      ${edit test type}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           1 second

Delete Market Type Not Delete
    Click Link                      xpath://*[@href="/market-types"]
    Sleep                           1 second
    Click Element                   ${delete market type button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]         ${market type}
    Click Element                   xpath:${modal dialog}${button danger}
    Element Text Should Be          css:.external-page-alert > strong:nth-child(2)              Operation failed!
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second

Edit Market Type
    Click Element                   ${edit market type button}
    Input Text                      id:name_id                      ${edit market type}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           1 second

Checking New Types On Distributor
    [Tags]                          CheckingOnDistributorPortal
    Goto Customer Menu Sub
    Sleep                           2 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]     ${edit test type}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]     ${edit market type}
    Click Element                   xpath:(${react table raw})[1]
    Select From Dropdown            (${dropdown menu})[1]       Not specified
    Select From Dropdown            (${dropdown menu})[2]       Not specified
    Click Element                   xpath:${button submit}
    Goto Sidebar Customers
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]     Not specified
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]     Not specified
    Finish Suite
    Sleep                           5 second

Delete Customer Type
    Preparation
    Click Link                      xpath://*[@href="/customer-types"]
    Click Element                   ${delete customer type}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ${edit test type}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           4 second
    ${current size}                 Get Rows Count                  ${table xpath}
    ${previous size}                Evaluate    ${my customer type}-1
    Should Be Equal As Integers     ${current size}     ${previous size}

Delete Market Type
    Click Link                      xpath://*[@href="/market-types"]
    Click Element                   ${delete market type button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ${edit market type}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           4 second
    ${current size}                 Get Rows Count                  ${table xpath}
    ${previous size}                Evaluate    ${my market type}-1
    Should Be Equal As Integers     ${current size}     ${previous size}

*** Keywords ***
Goto Customer Menu Sub
    Finish Suite
    Start Distributor
    Sleep                           5 second
    Goto Sidebar Customers
    Sleep                           5 second

Preparation
    Start Admin