*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Valid Create New Security Group
    Click Element                   ${create button}
    ${security group}               Generate Random Name L
    Set Suite Variable              ${security group}
    Input By Name                   name    ${security group}
    Click Element                   xpath:${button submit}

Checking New Security Group
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]      ${security group}

Create User With New Security Group
    ${buffer}                       Generate Random Name L  10
    Set Suite Variable              ${distributor user email}   distributor.${buffer}@example.com
    Goto Sidebar Users
    Click Element                   ${create button}
    Input By Name                   email       ${distributor user email}
    Input By Name                   firstName   ${user first name}
    Input By Name                   lastName    ${user last name}
    Select From Dropdown            (${dialog}${dropdown menu})[1]   ${security group}
    Click Element                   (${dialog}${checkbox type})[1]
    Click Element                   xpath:${button submit}
    Sleep                           4 second
    ${number of row u}              Get Element Count           xpath:${react table raw}
    Set Suite Variable              ${number of row u}

Checking New User
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[1]      ${distributor user email}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[2]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[3]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[5]      ${security group}

Try To Delete Security Group
    Goto Sidebar Security Groups
    Click Element                   xpath:(${react table raw})[${number of new row}]${delete security group}
    Dialog Should Be About          ${security group}
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    Page Should Contain             UserGroup with key 
    Page Should Contain             has unresolved constraint: Users are present.
    Goto Sidebar Users

Delete User
    [Tags]                          Test
    Click Element                   xpath:(${react table raw})[${number of row u}]${delete user}
    Dialog Should Be About          ${user first name} ${user last name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    Goto Sidebar Security Groups

Edit Security Group
    Click Element                   xpath:(${react table raw})[${number of new row}]${edit security group}
    Input By Name                   name    ${security group}
    Click Element                   xpath:${general permission card}
    Set General Permission          Users           1
    Set General Permission          Super Users     2
    Click Element                   xpath:${settings permission card}
    Set Settings Permission         Settings - Distributor Contact Information      1
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Delete Security Group
    Click Element                   xpath:(${react table raw})[${number of new row}]${delete security group}
    Dialog Should Be About          ${security group}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Security Groups
    Sleep                           2 second
    ${number of row}                Get Element Count           xpath:${react table raw}
    ${number of new row}=           Evaluate    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
