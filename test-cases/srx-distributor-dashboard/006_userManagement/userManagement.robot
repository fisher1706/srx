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
    Sleep                           1 second
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   xpath:${users pane users}${button primary}
    Press Key                       id:email_id                 \ue004
    Element Should Be Enabled       xpath:(${modal dialog}${help block})[1]/*
    Press Key                       id:firstName_id             \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[2]/*
    Press Key                       id:lastName_id              \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[3]/*
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]        \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[4]/*
    Press Key                       css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)         \ue004
    Element Should Be Visible       css:.red-help-block > svg:nth-child(1) > path:nth-child(1)
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second

Valid Create New User
    [Tags]                          ValidCreateNewUser
    Click Element                   xpath:${users pane users}${button primary}
    Input Text                      id:email_id                 ${incorrect email}
    Element Should Be Enabled       xpath:(${modal dialog}${help block})[1]/*
    Input Text                      id:email_id                 ${dynamic email}
    Input Text                      id:firstName_id             ${user first name}
    Input Text                      id:lastName_id              ${user last name}
    Click Element                   xpath:${button modal dialog ok}
    Element Should Be Enabled       css:.red-help-block > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Go Down Selector                ${modal dialog}${select control}    User
    Click Element                   xpath:${button modal dialog ok}
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
    Sleep                           1 second
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   ${edit user button}
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second
    Click Element                   ${edit user button}
    Input Text                      id:firstName_id             ${edit first name}
    Input Text                      id:lastName_id              ${edit last name}
    Go Down Selector                ${modal dialog}${select control}    Static Group
    Click Element                   css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:div.checkbox:nth-child(2) > label:nth-child(1) > input:nth-child(1)
    Click Element                   xpath:${button modal dialog ok}
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
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]          ${dynamic email}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]          ${edit first name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]          ${edit last name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]          Static Group
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           10 second

Sorting Users
    [Tags]                          Sorting
    Sort Column                     1   ${number of row}
    Sort Column                     2   ${number of row}
    Sort Column                     3   ${number of row}
    Sort Column                     5   ${number of row}

User Filtration
    [Tags]                          Filter
    Filter Field                    1   1   az_user@example.com
    Filter Field                    2   2   First Z
    Filter Field                    3   3   Last Z

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Sidebar Users
    Click Element                   id:users-tab-users
    ${number of row}                Get Rows Count              ${users pane users}${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit user button}         xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]${button success}
    Set Suite Variable              ${delete user button}       xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]${button danger}