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
    Click Element                   css:.btn-primary
    Is Add Customer
    Click Element                   css:.close
    Sleep                           2 second
    Click Element                   css:.btn-primary
    Press Key                       id:name_id                  \ue004
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:number_id                \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       css:.Select-input           \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second

Valid Create New Customer
    [Tags]                          ValidCreateNewCustomer
    Click Element                   css:.btn-primary
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
    Set Global Variable             ${selecting type}
    Click Element                   xpath:(${select control})[3]
    Press Key                       xpath:(${select control})[3]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[3]/div[1]/div[2]        \ue007
    ${selecting market}             Get Text                    xpath:(${select control})[3]/div[1]/div[1]/span
    Click Element                   css:.modal-dialog-ok-button
    Set Global Variable             ${selecting market}

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
    Click Element                   css:.close
    Sleep                           2 second
    Click Element                   ${edit customer button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Click Element                   ${edit customer button}
    Input Text                      id:name_id                  ${edit first name}
    Input Text                      id:number_id                ${edit warehouse number}
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
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div      ${edit warehouse number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div      Not specified
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div      Not specified

Delete Customer
    Click Element                   ${delete customer button}
    Is Delete Customer
    Click Element                   css:.close
    Sleep                           2 second
    Click Element                   ${delete customer button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Click Element                   ${delete customer button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]          ${edit first name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]          ${edit warehouse number}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[4]          Not specified
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]          Not specified
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           10 second

Sorting Customers
    [Tags]                          Sorting
    Sorting Column                  1
    Sorting Column                  2
    Sorting Column                  3
    Sorting Column                  4
    Sorting Column                  5

Customer Filtration
    [Tags]                          Filter
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/input                       Customer A
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/input                       1138
    Field Selector Check            xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div/div/div/div/div[1]      Not specified
    Field Selector Check            xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[4]/div[2]/div/div/div/div/div[1]      Not specified

*** Keywords ***
Preparation
    Goto Customer Management
    Number Of Rows
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

Field Selector Check
    [Arguments]                     ${fieldAdr}                 ${fieldType}
    Click Element                   css:.button-right-margin
    ${result} =                     Fetch From Left             ${fieldAdr}    2]/div/div/div/div/div[1]
    ${newString}=                   Strip String                ${result}1]/div
    ${fieldName}                    Get Text                    ${newString}
    Go Down Selector                ${fieldAdr}                 ${fieldType}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           3 seconds
    ${rowNum}                       Get Element Count           xpath:${header xpath}/thead/tr/th
    ${rowNum}=                      Evaluate                    ${rowNum}+1
     :FOR   ${var}                  IN RANGE                    1   ${rowNum}
    \       ${textInfo}             Get Text                    xpath:${header xpath}/thead/tr/th[${var}]
    \       Run Keyword If          "${textInfo}" == "${fieldName}"   Field Comparing First Fields   ${var}        ${fieldType}
    Click Element                   css:button.button-right-margin:nth-child(2)
    Sleep                           2 seconds

Go Down Selector
    [Arguments]                     ${fieldAdr}                 ${field type}
    Click Element                   ${fieldAdr}
    ${result} =                     Fetch From Left             ${fieldAdr}    div/div[1]
    ${newString}=                   Strip String                ${result}div[1]/div[2]
    Press Key                       ${newString}                \ue015
    Press Key                       ${newString}                \ue007              
    ${text buffer sub}              Get Text                    ${fieldAdr}
    Sleep                           1 second
    Run Keyword If                  "${text buffer sub}"!="${field type}"        Go Down Selector    ${fieldAdr}    ${field type}