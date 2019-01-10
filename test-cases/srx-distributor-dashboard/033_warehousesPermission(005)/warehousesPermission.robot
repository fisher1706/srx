*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Invalid Create New Warehouse
    Click Element                   css:.btn-primary
    Is Add Warehouse
    Click Element                   css:.close
    Sleep                           2 second
    Is Warehouse Management
    Click Element                   css:.btn-primary
    Press Key                       id:name_id              \ue004
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1)
    Press Key                       id:address.line1_id     \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:number_id            \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:address.city_id      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(5) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       xpath:${select control}/div[1]/div[2]                \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(6) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:contactEmail_id      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(7) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:address.zipCode_id   \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(8) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:invoiceEmail_id      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(9) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Warehouse Management

Valid Create New Warehouse
    [Tags]                          ValidCreateNewWarehouse
    Click Element                   css:.btn-primary
    Input Text                      id:name_id              ${user first name}
    Input Text                      id:address.line1_id     ${dynamic adress1}
    Input Text                      id:address.line2_id     ${dynamic adress2}
    Input Text                      id:number_id            ${warehouse number}
    Input Text                      id:address.city_id      ${dynamic city}
    Click Element                   xpath:${select control}
    Press Key                       xpath:${select control}/div[1]/div[2]        \ue015
    Press Key                       xpath:${select control}/div[1]/div[2]        \ue015
    Press Key                       xpath:${select control}/div[1]/div[2]        \ue007
    Input Text                      id:contactEmail_id      ${incorrect email}
    Input Text                      id:address.zipCode_id   ${dynamic code}
    Input Text                      id:invoiceEmail_id      ${incorrect email}
    Element Should Be Visible       css:div.item-form-field:nth-child(7) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Element Should Be Visible       css:div.item-form-field:nth-child(9) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Input Text                      id:contactEmail_id      ${correct wrong email}
    Input Text                      id:invoiceEmail_id      ${correct wrong email}
    Click Element                   css:.modal-dialog-ok-button

Checking New Warehouse
    [Tags]                          ValidCreateNewWarehouse
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/a     ${user first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div   ${warehouse number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div   ${dynamic full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div   ${correct wrong email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div   ${correct wrong email}

Edit Warehouse
    [Tags]                          EditWarehouse
    Click Element                   ${edit warehouse button}
    Is Edit Warehouse
    Click Element                   css:.close
    Sleep                           2 second
    Is Warehouse Management
    Click Element                   ${edit warehouse button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Warehouse Management
    Click Element                   ${edit warehouse button}
    Input Text                      id:name_id              ${user last name}
    Input Text                      id:address.line1_id     ${edit adress1}
    Input Text                      id:address.line2_id     ${edit adress2}
    Input Text                      id:number_id            ${edit warehouse number}
    Input Text                      id:address.city_id      ${edit city}
    Click Element                   xpath:${select control}
    Press Key                       xpath:${select control}/div[1]/div[2]        \ue013
    Press Key                       xpath:${select control}/div[1]/div[2]        \ue007
    Input Text                      id:address.zipCode_id   ${edit code}
    Input Text                      id:contactEmail_id      ${edit email}
    Input Text                      id:invoiceEmail_id      ${edit email}
    Click Element                   css:.modal-dialog-ok-button

Checking Edit Warehouse
    [Tags]                          EditWarehouse
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/a        ${user last name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div      ${edit warehouse number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div      ${edit full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div      ${edit email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div      ${edit email}

Delete Warehouse
    [Tags]                          DeleteWarehouse
    Click Element                   ${delete warehouse button}
    Sleep                           1 second
    Click Element                   css:.close
    Sleep                           2 second
    Is Warehouse Management
    Click Element                   ${delete warehouse button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Is Warehouse Management
    Click Element                   ${delete warehouse button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]      ${user last name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]      ${edit warehouse number}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[4]      ${edit full adress}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]      ${edit email}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[6]      ${edit email}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           10 second

*** Keywords ***
Preparation
    Goto Security Groups
    ${permission test group}        Get Row By Text     (${table xpath})[2]     1       Permissions Test
    Set Suite Variable              ${edit group button}            xpath:(${table xpath})[2]/tbody/tr[${permission test group}]/td[2]/div/div[1]/button
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  15       1
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
    Click Link                      xpath://*[@href="/warehouses"]
    Sleep                           5 second
    Reload Page
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    Set Global Variable             ${number of row}
    ${number of new row}=           Evaluate                        ${number of row}+1
    Set Global Variable             ${number of new row}
    Set Global Variable             ${edit warehouse button}        xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]/div/div[1]/button
    Set Global Variable             ${delete warehouse button}      xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]/div/div[2]/button

Is Add Warehouse
    Element Text Should Be          css:.modal-title                Add warehouse

Is Edit Warehouse
    Element Text Should Be          css:.modal-title                Edit warehouse