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
    Click Element                   xpath:${users pane users}${button primary}
    Is Add New User
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   xpath:${users pane users}${button primary}
    Press Key                       id:email_id                 \ue004
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:firstName_id             \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:lastName_id              \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]        \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)         \ue004
    Element Should Be Visible       css:.red-help-block > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second

Valid Create New User
    [Tags]                          ValidCreateNewUser
    Click Element                   xpath:${users pane users}${button primary}
    Is Add New User
    Input Text                      id:email_id                 ${incorrect email}
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Input Text                      id:email_id                 ${dynamic email}
    Input Text                      id:firstName_id             ${user first name}
    Input Text                      id:lastName_id              ${user last name}
    Click Element                   css:.modal-dialog-ok-button
    Element Should Be Enabled       css:.red-help-block > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Go Down Selector                ${modal dialog}${select control}    User
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    

Checking New User
    [Tags]                          ValidCreateNewUser
    Sleep                           5 second
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[1]/div      ${dynamic email}
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[2]/div      ${user first name}
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[3]/div      ${user last name}
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[4]/div      A_Warehouse
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[5]/div      User

Edit User
    [Tags]                          EditUser
    Click Element                   ${edit user button}
    Is Edit User
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   ${edit user button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Click Element                   ${edit user button}
    Input Text                      id:firstName_id             ${edit first name}
    Input Text                      id:lastName_id              ${edit last name}
    Go Down Selector                ${modal dialog}${select control}    Static Group
    Click Element                   css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:div.checkbox:nth-child(2) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    

Checking Edit User
    [Tags]                          EditUser
    Sleep                           5 second
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[1]/div      ${dynamic email}
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[2]/div      ${edit first name}
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[3]/div      ${edit last name}
    Element Text Should Be          xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[5]/div      Static Group

Delete User
    [Tags]                          DeleteUser
    Click Element                   ${delete user button}
    Sleep                           1 second
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   ${delete user button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Click Element                   ${delete user button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]          ${dynamic email}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]          ${edit first name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]          ${edit last name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]          Static Group
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           10 second

Sorting Users By Email
    [Tags]                          Sorting                     UserSorting
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[1]
    ${text buffer1}                 Get Text                    xpath:${table xpath}/tbody/tr[1]/td[1]/div
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[1]
    ${text buffer2}                 Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/div
    Should Be Equal                 ${text buffer1}             ${text buffer2}
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[1]

Sorting Users By First Name
    [Tags]                          Sorting                     UserSorting
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[2]
    ${text buffer1}                 Get Text                    xpath:${table xpath}/tbody/tr[1]/td[2]/div
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[2]
    ${text buffer2}                 Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div
    Should Be Equal                 ${text buffer1}             ${text buffer2}
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[2]

Sorting Users By Last Name
    [Tags]                          Sorting                     UserSorting
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[3]
    ${text buffer1}                 Get Text                    xpath:${table xpath}/tbody/tr[1]/td[3]/div
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[3]
    ${text buffer2}                 Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div
    Should Be Equal                 ${text buffer1}             ${text buffer2}
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[3]
    
Sorting By Role
    [Tags]                          Sorting                     UserSorting
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[5]
    ${text buffer1}                 Get Text                    xpath:${table xpath}/tbody/tr[1]/td[5]/div
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[5]
    ${text buffer2}                 Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[5]/div
    Should Be Equal                 ${text buffer1}             ${text buffer2}
    Click Element                   xpath:${users pane users}${header xpath}/thead/tr/th[5]

User filtration
    [Tags]                          Filter
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/input    z_user@example.com
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/input    First Z
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/input    Last Z

*** Keywords ***
Preparation
    Goto User Managemant
    Click Element                   id:users-tab-users
    ${number of row}                Get Rows Count              ${users pane users}${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit user button}         xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[6]/div/div[1]/button
    Set Suite Variable              ${delete user button}       xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]/td[6]/div/div[2]/button

Is Add New User
    Element Text Should Be          css:.modal-title            Add user

Is Edit User
    Element Text Should Be          css:.modal-title            Edit user