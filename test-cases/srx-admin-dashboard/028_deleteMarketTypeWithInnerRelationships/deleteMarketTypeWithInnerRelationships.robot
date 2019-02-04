*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Valid Create New Market Type
    Set Suite Variable              ${right size}                   ${number of row}
    Click Element                   xpath:${button primary}
    Input Text                      id:name_id                      ${market del type}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           1 second

Checking New Market Type On Distributor Portal Not Delete
    [Tags]                          CheckingOnDistributorPortal
    Goto Customer Menu Sub
    Click Element                   ${edit customer button sub}
    Choose From Select Box          (${select control})[2]      ${market del type}
    Sleep                           1 second
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my customer}]/td[5]/div      ${market del type}
    Finish Suite

Delete Market Type Not Delete
    Sleep                           5 second
    Preparation
    Click Element                   ${delete button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]         ${market del type}
    Click Element                   xpath:${modal dialog}${button danger}
    Element Text Should Be          css:.external-page-alert > strong:nth-child(2)              Operation failed!
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           5 second

Checking New Market Type On Distributor Portal Delete
    [Tags]                          CheckingOnDistributorPortal
    Goto Customer Menu Sub
    Click Element                   ${edit customer button sub}
    Choose From Select Box          (${select control})[2]      Not specified
    Sleep                           1 second
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my customer}]/td[5]/div      Not specified
    Finish Suite

Delete Market Type Delete
    Sleep                           5 second
    Preparation
    Click Element                   ${delete button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]          ${market del type}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second
    ${current size}                 Get Element Count                   xpath:${table xpath}/tbody/tr
    Run Keyword If                  ${current size}==${right size}      Pass Execution      Pass    ELSE        Fail    Fail

*** Keywords ***
Goto Customer Menu Sub
    Finish Suite
    Start Distributor
    Sleep                           4 second
    Click Link                      xpath://*[@href="/customers"]
    Sleep                           5 second
    ${my customer}                  Get Row By Text     ${table xpath}      1   Customer Z
    Set Suite Variable              ${my customer}
    Set Suite Variable              ${edit customer button sub}     xpath:${table xpath}/tbody/tr[${my customer}]${button success}

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