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
Valid Create New User
    Click Element                   ${create button}
    Input By Name                   email       ${incorrect email}
    Page Should Contain             Email must be a valid email
    Input By Name                   email       ${distributor user email}
    Input By Name                   firstName   ${user first name}
    Input By Name                   lastName    ${user last name}
    Click Element                   xpath:${button submit}
    Page Should Contain             Role is a required field
    Page Should Contain             Warehouses is a required field
    Select From Dropdown            (${dialog}${dropdown menu})[1]   User
    Click Element                   (${dialog}${checkbox type})[1]
    Click Element                   xpath:${button submit}
    Sleep                           2 second

Checking New User
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]      ${distributor user email}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[2]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[3]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]      User

Edit User
    Click Element                   xpath:(${react table raw})[${number of new row}]${edit user}
    Input By Name                   firstName   ${edit first name}
    Input By Name                   lastName    ${edit last name}
    Select From Dropdown            (${dialog}${dropdown menu})[1]   Static Group
    Click Element                   (${dialog}${checkbox type})[1]
    Click Element                   (${dialog}${checkbox type})[2]
    Click Element                   xpath:${button submit}
    Sleep                           2 second

Checking Edit User
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]      ${distributor user email}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[2]      ${edit first name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[3]      ${edit last name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]      Static Group

Delete User
    Click Element                   xpath:(${react table raw})[${number of new row}]${delete user}
    Dialog Should Be About          ${edit first name} ${edit last name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Security Groups
    Sleep                           3 second
    ${permission test group}        Get Row By Text     (${table xpath})[2]     1       Permissions Test
    Set Suite Variable              ${edit group button}            xpath:(${table xpath})[2]/tbody/tr[${permission test group}]${button success}
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  2       1
    Click Element                   xpath:(${dialog tab})[2]
    Clear All Settings Permissions
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           3 second
    Finish Suite
    Sleep                           3 second
    Start Permission
    ${buffer}                       Generate Random Name L  10
    Set Suite Variable              ${distributor user email}   distributor.${buffer}@example.com
    Goto Sidebar Users
    Click Element                   id:users-tab-users
    ${number of row}                Get Rows Count              ${users pane users}${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit user button}         xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]${button success}
    Set Suite Variable              ${delete user button}       xpath:${users pane users}${table xpath}/tbody/tr[${number of new row}]${button danger}