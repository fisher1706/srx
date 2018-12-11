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
Invalid Create New User
    Click Element                   css:.btn-primary
    Is Add New User
    Click Element                   css:.close
    Sleep                           2 second
    Is User Management
    Click Element                   css:.btn-primary
    Press Key                       id:email_id                 \ue004
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:firstName_id             \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:lastName_id              \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]        \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)         \ue004
    Element Should Be Visible       css:.red-help-block > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is User Management

Valid Create New User
    [Tags]                          ValidCreateNewUser
    Click Element                   css:.btn-primary
    Is Add New User
    Input Text                      id:email_id                 ${incorrect email}
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Input Text                      id:email_id                 ${dynamic email}
    Input Text                      id:firstName_id             ${user first name}
    Input Text                      id:lastName_id              ${user last name}
    Click Element                   css:.modal-dialog-ok-button
    Element Should Be Enabled       css:.red-help-block > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:.Select-control
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]        \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]        \ue007
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is User Management

Checking New User
    [Tags]                          ValidCreateNewUser
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/div      ${dynamic email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div      ${user first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div      ${user last name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div      A_Warehouse
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div      User

Edit User
    [Tags]                          EditUser
    Click Element                   ${edit user button}
    Is Edit User
    Click Element                   css:.close
    Sleep                           2 second
    Is User Management
    Click Element                   ${edit user button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is User Management
    Click Element                   ${edit user button}
    Input Text                      id:firstName_id             ${edit first name}
    Input Text                      id:lastName_id              ${edit last name}
    Click Element                   css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:div.checkbox:nth-child(2) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is User Management

Checking Edit User
    [Tags]                          EditUser
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/div      ${dynamic email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div      ${edit first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div      ${edit last name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div      User

Delete User
    [Tags]                          DeleteUser
    Click Element                   ${delete user button}
    Is Delete User
    Click Element                   css:.close
    Sleep                           2 second
    Is User Management
    Click Element                   ${delete user button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Is User Management
    Click Element                   ${delete user button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]          ${dynamic email}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]          ${edit first name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]          ${edit last name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]          User
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           10 second

*** Keywords ***
Preparation
    Goto Security Groups
    Number Of Rows G
    Number Of Static Row G
    Set Suite Variable              ${edit group button}            xpath:/html/body/div/div/div[2]/div[2]/div/div[3]/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${static row g}]/td[2]/div/div[1]/button
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  2       1
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/ul/li[2]/a
    Clear All Settings Permissions
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           3 second
    Is Security Groups
    Finish Suite
    Sleep                           3 second
    Start Suite
    Input Text                      id:email        srx-group+dev-permissions@agilevision.io
    Enter Password
    Correct Submit Login
    Click Link                      xpath://*[@href="/users"]
    Number Of Rows
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Global Variable             ${number of new row}
    Set Global Variable             ${edit user button}         xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div/div[1]/button
    Set Global Variable             ${delete user button}       xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div/div[2]/button

Is Add New User
    Element Text Should Be          css:.modal-title            Add user

Is Edit User
    Element Text Should Be          css:.modal-title            Edit user

Is Delete User
    Element Text Should Be          css:.modal-title            Removal Confirmation
