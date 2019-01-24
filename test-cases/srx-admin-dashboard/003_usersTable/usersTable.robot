*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***
${number of new row}
${number of row}
${filter button}                    css:.filtering-options > button:nth-child(1)
${apply filter}                     css:button.btn:nth-child(2)
${text buffer1}
${text buffer2}

*** Test Cases ***
Admin Users Menu Checking
    [Tags]                          AdminUsersMenuChecking
    Element Text Should Be          css:.table-responsive > table:nth-child(1) > thead:nth-child(1) > tr:nth-child(1) > td:nth-child(2)     ${static adress1}
    Element Text Should Be          css:.table-responsive > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)     ${static adress2}
    Element Text Should Be          css:.table-responsive > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)     ${static city}
    Element Text Should Be          css:.table-responsive > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)     ${static state}
    Element Text Should Be          css:.table-responsive > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)     ${static code}
    Element Text Should Be          css:.table-responsive > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)     Singular Billing
    Element Text Should Be          css:.table-responsive > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(2)     ${static email}

Invalid Add Admin User
    [Tags]                          InvalidAddAdminUser
    Click Element                   css:#distributor-details-tab-2
    Sleep                           2 second
    Click Element                   xpath:${distributors admin pane}${button primary}
    Input Text                      id:email_id             ${incorrect email}
    Element Should Be Visible       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1)
    Click Element                   css:.close
    Sleep                           2 second
    Click Element                   xpath:${distributors admin pane}${button primary}
    Press Key                       id:email_id             \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1)
    Press Key                       id:firstName_id         \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1)
    Press Key                       id:lastName_id          \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second

Valid Add Admin User
    [Tags]                          ValidAddAdminUser
    Click Element                   css:#distributor-details-tab-2
    Click Element                   xpath:${distributors admin pane}${button primary}
    Input Text                      id:email_id             dprovorov+srx@agilevision.io
    Input Text                      id:firstName_id         ${user first name}
    Input Text                      id:lastName_id          ${user last name}
    Click Element                   xpath:${button modal dialog ok}
    Element Should Be Visible       css:.external-page-alert > button:nth-child(1)
    Sleep                           1 second
    Input Text                      id:email_id             ${user email}
    Click Element                   xpath:${button modal dialog ok}

Checking New User
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/div       ${user email}	
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div       ${user first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${user last name}

Edit User
    [Tags]                          EditUser
    Click Element                   css:#distributor-details-tab-2
    Click Element                   ${edit user button}
    Input Text                      id:firstName_id         ${edit first name}
    Input Text                      id:lastName_id          ${edit last name}
    Click Element                   xpath:${button modal dialog ok}

Checking Edit Data
    [Tags]                          EditUser
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/div       ${user email}	
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div       ${edit first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${edit last name}

Delete User
    [Tags]                          DeleteUser
    Click Element                   css:#distributor-details-tab-2
    Click Element                   ${delete user button}
    Click Element                   css:.close
    Sleep                           2 second
    Click Element                   ${delete user button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Click Element                   ${delete user button}
    Table Cell Should Contain       css:table.table:nth-child(2)        2       1       ${user email}	
    Table Cell Should Contain       css:table.table:nth-child(2)        2       2       ${edit first name}
    Table Cell Should Contain       css:table.table:nth-child(2)        2       3       ${edit last name}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           5 second

Sorting Users By Email
    [Tags]                          Sorting             UsersSorting
    Click Element                   css:#distributor-details-tab-2
    Click Element                   css:th.sort-column:nth-child(1)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[1]/div
    Click Element                   css:th.sort-column:nth-child(1)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/div
    Should Be Equal                 ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(1)

Sorting Users By First Name
    [Tags]                          Sorting             UsersSorting
    Click Element                   css:#distributor-details-tab-2
    Click Element                   css:th.sort-column:nth-child(2)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[2]/div
    Click Element                   css:th.sort-column:nth-child(2)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div
    Click Element                   css:th.sort-column:nth-child(2)

Sorting Users By Last Name
    [Tags]                          Sorting             UsersSorting
    Click Element                   css:#distributor-details-tab-2
    Click Element                   css:th.sort-column:nth-child(3)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[3]/div
    Click Element                   css:th.sort-column:nth-child(3)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div
    Should Be Equal                 ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(3)
    
Email Filter
    [Tags]                          Filter
    Click Element                   css:#distributor-details-tab-2
    Click Element                   ${filter button}
    Click Element                   css:.close
    Sleep                           2 second
    Click Element                   ${filter button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Click Element                   ${filter button}
    Input Text                      css:.filtering-options-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)    ${filter email}
    Apply Filter

First Name Filter
    [Tags]                          Filter
    Click Element                   ${filter button}
    Input Text                      css:div.row-spaced:nth-child(2) > div:nth-child(2) > input:nth-child(1)                         ${filter first}
    Apply Filter

Second Name Filter
    [Tags]                          Filter
    Click Element                   ${filter button}
    Input Text                      css:div.row-spaced:nth-child(3) > div:nth-child(2) > input:nth-child(1)                         ${filter last}
    Apply Filter

Email And First Name Filter
    [Tags]                          Filter
    Click Element                   ${filter button}
    Input Text                      css:.filtering-options-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)    ${filter email}
    Input Text                      css:div.row-spaced:nth-child(2) > div:nth-child(2) > input:nth-child(1)	                        ${filter first}
    Apply Filter

First Name And Second Name Filter
    [Tags]                          Filter
    Click Element                   ${filter button}
    Input Text                      css:div.row-spaced:nth-child(3) > div:nth-child(2) > input:nth-child(1)                         ${filter last}
    Input Text                      css:div.row-spaced:nth-child(2) > div:nth-child(2) > input:nth-child(1)                         ${filter first}
    Apply Filter

Email And Second Name Filter
    [Tags]                          Filter
    Click Element                   ${filter button}
    Input Text                      css:.filtering-options-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)    ${filter email}
    Input Text                      css:div.row-spaced:nth-child(3) > div:nth-child(2) > input:nth-child(1)                         ${filter last}
    Apply Filter

Email And First Name And Second Name Filter
    [Tags]                          Filter
    Click Element                   ${filter button}
    Input Text                      css:.filtering-options-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)    ${filter email}
    Input Text                      css:div.row-spaced:nth-child(2) > div:nth-child(2) > input:nth-child(1)                         ${filter first}
    Input Text                      css:div.row-spaced:nth-child(3) > div:nth-child(2) > input:nth-child(1)	                        ${filter last}
    Apply Filter

*** Keywords ***
Preparation
    Goto Admin Users
    Number Of Rows
    ${number of new row}=           Evaluate                ${number of row}+1
    Set Global Variable             ${number of new row}
    Set Global Variable             ${edit user button}     xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div/div[1]/button
    Set Global Variable             ${delete user button}   xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div/div[2]/button

Apply Filter
    Click Element                   ${apply filter}
    Sleep                           3 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr/td[1]/div     ${filter email}
    Click Element                   css:button.button-right-margin:nth-child(2)