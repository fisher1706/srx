*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${delete customer name}             Delete Customer
${delete customer number}           777

*** Test Cases ***
Valid Create New Customer
    [Tags]                          ValidCreateNewCustomer
    Click Element                   css:.btn-primary
    Is Add Customer
    Input Text                      id:name_id                  ${delete customer name}
    Input Text                      id:number_id                ${delete customer number}
    Click Element                   css:div.item-form-field:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[3]/div/div/div/div[1]/div[2]        \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[3]/div/div/div/div[1]/div[2]        \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[3]/div/div/div/div[1]/div[2]        \ue007
    Click Element                   css:div.item-form-field:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]        \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]        \ue007
    ${selecting type}               Get Text                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[1]/span
    Set Global Variable             ${selecting type}
    Click Element                   css:div.item-form-field:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[2]        \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[2]        \ue007
    ${selecting market}             Get Text                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[1]/span
    Click Element                   css:.modal-dialog-ok-button
    Set Global Variable             ${selecting market}

Checking New Customer
    Sleep                           5 second
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of new row}]/td[1]/a        ${delete customer name}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of new row}]/td[2]/div      ${delete customer number}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of new row}]/td[3]/div      Z_Warehouse(9999)
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of new row}]/td[4]/div      ${selecting type}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of new row}]/td[5]/div      ${selecting market}

Create Shiptos 1
    Click Element                   xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of new row}]/td[1]/a
    Goto Customer Shipto
    Click Element                   css:#customer-details-pane-shiptos > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
    Input Text                      css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                    ${dynamic name}
    Input Text                      id:address.line1_id     ${dynamic adress1}
    Input Text                      id:address.line2_id     ${dynamic adress2}
    Input Text                      id:address.city_id      ${dynamic city}
    Click Element                   css:.Select-control
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[2]            \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[2]            \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[2]            \ue007
    Input Text                      id:address.zipCode_id   ${dynamic code}
    Input Text                      id:poNumber_id          ${test number}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is Customer Shipto
    Number Of Rows Shiptos
    Set Global Variable             ${delete shipto button}         xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row s}]/td[4]/div/div[2]/button

Checking New Shipto 1
    Sleep                           5 second
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row s}]/td[1]/div      ${dynamic name}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row s}]/td[2]/div      ${dynamic full adress}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row s}]/td[3]/div      ${test number}

Valid Create New User 1
    Goto Customer Users
    ${buffer}=                      Generate Random String      18      [LETTERS]
    ${buffer2}                      Convert To Lowercase        ${buffer}
    Set Global Variable             ${delete customer user1}    ${buffer2}@example.com
    Click Element                   css:#customer-details-pane-users > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
    Input Text                      css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                ${delete customer user1}
    Input Text                      id:firstName_id             ${user first name}
    Input Text                      id:lastName_id              ${user last name}
    Click Element                   css:.Select-control
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]    \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]    \ue004
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div[${number of row s}]/label/input
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is Customer Users
    Number Of Rows Users

Checking New User 1
    Sleep                           5 second
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[2]/div     ${delete customer user1}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[3]/div     ${user first name}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[4]/div     ${user last name}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[5]/div     Customer User
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[6]/div     ${dynamic name}

Delete Shipto 1
    Goto Customer Shipto
    Click Element                   ${delete shipto button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]      ${dynamic name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]      ${dynamic full adress}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           3 second

Create Shiptos 2
    Goto Customer Shipto
    Click Element                   css:#customer-details-pane-shiptos > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
    Input Text                      css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                    ${dynamic name}
    Input Text                      id:address.line1_id     ${dynamic adress1}
    Input Text                      id:address.line2_id     ${dynamic adress2}
    Input Text                      id:address.city_id      ${dynamic city}
    Click Element                   css:.Select-control
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[2]        \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[2]        \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div/div/div[1]/div[2]        \ue007
    Input Text                      id:address.zipCode_id   ${dynamic code}
    Input Text                      id:poNumber_id          ${test number}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is Customer Shipto
    Number Of Rows Shiptos

Checking New Shipto 2
    Sleep                           5 second
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row s}]/td[1]/div      ${dynamic name}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row s}]/td[2]/div      ${dynamic full adress}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row s}]/td[3]/div      ${test number}

Valid Create New User 2
    Goto Customer Users
    ${buffer}=                      Generate Random String      18      [LETTERS]
    ${buffer2}                      Convert To Lowercase        ${buffer}
    Set Global Variable             ${delete customer user2}    ${buffer2}@example.com
    Click Element                   css:#customer-details-pane-users > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
    Input Text                      id:email_id                 ${delete customer user1}
    Input Text                      id:firstName_id             ${user first name}
    Input Text                      id:lastName_id              ${user last name}
    Click Element                   css:.Select-control
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]    \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]    \ue004
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div[${number of row s}]/label/input
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           1 second
    Page Should Contain             The user ${delete customer user1} already present.
    Input Text                      id:email_id                 ${delete customer user2}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is Customer Users
    Number Of Rows Users

Checking New User 2
    Sleep                           5 second
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[2]/div     ${delete customer user2}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[3]/div     ${user first name}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[4]/div     ${user last name}
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[5]/div     Customer User
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of row u}]/td[6]/div     ${dynamic name}

Delete Customer
    [Tags]                          DeleteCustomer
    Click Link                      xpath://*[@href="/customers"]
    Click Element                   ${delete customer button}
    Is Delete Customer
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Management
    Click Element                   ${delete customer button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Is Customer Management
    Click Element                   ${delete customer button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]          ${delete customer name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]          ${delete customer number}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]          Z_Warehouse(9999)
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[4]          ${selecting type}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]          ${selecting market}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           10 second

Checking On Transactions
    [Tags]                          Check
    Click Link                      xpath://*[@href="/transactions"]
    ${start shipto}                 Get Text                    xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[1]/span
    Set Global Variable             ${start shipto}
    Go Down Check

*** Keywords ***
Preparation
    Goto Customer Management
    Number Of Rows
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Global Variable             ${number of new row}
    Set Global Variable             ${delete customer button}   xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${number of new row}]/td[6]/div/div[2]/button

Is Add Customer
    Element Text Should Be          css:.modal-title            Add customer

Is Delete Customer
    Element Text Should Be          css:.modal-title            Removal Confirmation

Number Of Rows
    ${number of row}                Get Element Count           xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr
    Set Global Variable             ${number of row}

Number Of Rows Shiptos
    ${number of row s}              Get Element Count           xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr
    Set Global Variable             ${number of row s}

Number Of Rows Users
    ${number of row u}              Get Element Count           xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr
    Set Global Variable             ${number of row u}

Go Down Check
    Click Element                   css:.Select-control
    Press Key                       xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[2]      \ue015
    Press Key                       xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[2]      \ue007
    ${current shipto}               Get Text                    xpath:/html/body/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[1]/span
    Run Keyword If                  "${current shipto}"=="${delete customer name} - ${dynamic name}"        Fail    Fail
    Run Keyword If                  "${current shipto}"!="${start shipto}"      Go Down Check