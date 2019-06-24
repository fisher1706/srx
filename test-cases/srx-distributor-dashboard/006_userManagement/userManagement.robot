*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Valid Create New User
    Click Element                   id:item-action-create
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
    Set Suite Variable              ${warehouse}
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
    Click Element                   xpath:(${react table raw})[${number of new row}]${delete customer}
    Dialog Should Be About          ${edit first name} ${edit last name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Sorting Users
    [Tags]                          Sorting
    Sort React                      1
    Sort React                      2
    Sort React                      3
    Sort React                      5

User Filtration
    [Tags]                          Filter
    Filter Add                      1   1   az_user@example.com
    Filter Add                      2   2   First Z
    Filter Add                      3   3   Last Z

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    ${buffer}                       Generate Random Name L  10
    Set Suite Variable              ${distributor user email}   distributor.${buffer}@example.com
    Goto Sidebar Users
    Click Element                   xpath:${tab element}
    ${number of row}                Get Element Count           xpath:${react table raw}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}