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
    Press Key                       id:name_id                                      \ue004
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second

Valid Create New Customer
    [Tags]                          ValidCreateNewCustomer
    Click Element                   xpath:${button primary}
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
    Click Element                   xpath:${button modal dialog ok}
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
    Input Text                      id:name_id                  ${edit first name}
    Clear Element Text              id:number_id
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue013
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue007
    Click Element                   xpath:(${select control})[2]
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue013
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue007
    Click Element                   xpath:${button modal dialog ok}
    
Checking Edit Customer
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/a        ${edit first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div      Not specified
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div      Not specified

Delete Customer
    Click Element                   ${delete customer button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]          ${edit first name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]          Not specified
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]          Not specified
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           10 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Click Link                      xpath://*[@href="/security-groups"]
    Sleep                           5 second
    ${permission test group}        Get Row By Text     (${table xpath})[2]     1       Permissions Test
    Set Suite Variable              ${edit group button}            xpath:(${table xpath})[2]/tbody/tr[${permission test group}]${button success}
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  7       1
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/ul/li[2]/a
    Clear All Settings Permissions
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           3 second
    Finish Suite
    Sleep                           3 second
    Start Permission
    Sleep                           3 second
    Goto Sidebar Customers
    ${number of row}                Get Rows Count              ${table xpath}
    Set Suite Variable              ${number of row}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit customer button}     xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Set Suite Variable              ${delete customer button}   xpath:${table xpath}/tbody/tr[${number of new row}]${button danger}