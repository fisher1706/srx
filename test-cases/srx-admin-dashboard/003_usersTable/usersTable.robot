*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

***Variables***
${error_msg}                        //div[contains(@class, 'has-error')]

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
    Sleep                           1 second
    Element Should Be Visible       xpath:(${error_msg}${help block})[1]/*
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   xpath:${distributors admin pane}${button primary}
    Press Key                       id:email_id             \ue004
    Element Should Be Visible       xpath:(${error_msg}${help block})[1]/*
    Press Key                       id:firstName_id         \ue004
    Element Should Be Visible       xpath:(${error_msg}${help block})[2]/*
    Press Key                       id:lastName_id          \ue004
    Element Should Be Visible       xpath:(${error_msg}${help block})[3]/*
    Click Element                   xpath:${button modal dialog cancel}
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
    Click Element                   ${delete user button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     ${user email}	
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ${edit first name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${edit last name}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

Sorting Users
    [Tags]                          Sorting
    Sort Column                     1   ${number of row}
    Sort Column                     2   ${number of row}
    Sort Column                     3   ${number of row}

User Filtration
    [Tags]                          Filter
    Filter Field                    1   1   ${filter email}
    Filter Field                    2   2   ${filter first}
    Filter Field                    3   3   ${filter last}

*** Keywords ***
Preparation
    Goto Admin Users
    Number Of Rows
    ${number of new row}=           Evaluate                ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit user button}     xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Set Suite Variable              ${delete user button}   xpath:${table xpath}/tbody/tr[${number of new row}]${button danger}