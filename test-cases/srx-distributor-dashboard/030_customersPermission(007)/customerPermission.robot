*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***
${number of new row}
${number of row}

*** Test Cases ***
Invalid Create New Customer
    [Tags]                          InvalidCreateNewCustomer
    Click Element                   xpath:${button primary}
    Is Add Customer
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   xpath:${button primary}
    Press Key                       id:name_id                                      \ue004
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second

Valid Create New Customer
    [Tags]                          ValidCreateNewCustomer
    Click Element                   xpath:${button primary}
    Is Add Customer
    Input Text                      id:name_id                  ${user first name}
    Input Text                      id:number_id                ${warehouse number}
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue007
    Click Element                   xpath:(${select control})[2]
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue007
    ${selecting type}               Get Text                    xpath:(${select control})[2]/div[1]/div[1]/span
    Set Suite Variable              ${selecting type}
    Click Element                   xpath:(${select control})[3]
    Press Key                       xpath:(${select control})[3]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[3]/div[1]/div[2]        \ue007
    ${selecting market}             Get Text                    xpath:(${select control})[3]/div[1]/div[1]/span
    Click Element                   css:.modal-dialog-ok-button
    Set Suite Variable              ${selecting market}

Checking New Customer
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/a        ${user first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div      ${warehouse number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div      ${selecting type}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div      ${selecting market}

Edit Customer
    [Tags]                          EditCustomer
    Click Element                   ${edit customer button}
    Is Edit Customer
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   ${edit customer button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Click Element                   ${edit customer button}
    Input Text                      id:name_id                  ${edit first name}
    Clear Element Text              id:number_id
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue013
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue007
    Click Element                   xpath:(${select control})[2]
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue013
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue007
    Click Element                   css:.modal-dialog-ok-button
    
Checking Edit Customer
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/a        ${edit first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div      Not specified
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div      Not specified

Delete Customer
    Click Element                   ${delete customer button}
    Is Delete Customer
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   ${delete customer button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Click Element                   ${delete customer button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]          ${edit first name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[4]          Not specified
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]          Not specified
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           10 second

*** Keywords ***
Preparation
    Goto Security Groups
    ${permission test group}        Get Row By Text     (${table xpath})[2]     1       Permissions Test
    Set Suite Variable              ${edit group button}            xpath:(${table xpath})[2]/tbody/tr[${permission test group}]/td[2]/div/div[1]/button
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  5       1
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/ul/li[2]/a
    Clear All Settings Permissions
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           3 second
    Is Security Groups
    Finish Suite
    Sleep                           3 second
    Start Suite
    ${permissions email}            Return Permissions Email
    Input Text                      id:email        ${permissions email}
    Enter Password
    Correct Submit Login
    Click Link                      xpath://*[@href="/customers"]
    ${number of row}                Get Rows Count              ${table xpath}
    Set Global Variable             ${number of row}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Global Variable             ${number of new row}
    Set Global Variable             ${edit customer button}     xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div/div[1]/button
    Set Global Variable             ${delete customer button}   xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div/div[2]/button

Is Add Customer
    Element Text Should Be          css:.modal-title            Add customer

Is Edit Customer
    Element Text Should Be          css:.modal-title            Edit customer

Is Delete Customer
    Element Text Should Be          css:.modal-title            Removal Confirmation