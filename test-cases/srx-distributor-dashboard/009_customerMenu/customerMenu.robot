*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Create New Shipto
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    ${number of shiptos}            Get Element Count       xpath:${react table raw}
    ${my shipto}                    Evaluate                ${number of shiptos}+1
    Set Suite Variable              ${my shipto}
    Click Element                   ${create button}
    Input By Name                   number                  ${shipto number}
    Input By Name                   name                    shipto
    Input By Name                   address.line1           ${dynamic adress1}
    Input By Name                   address.line2           ${dynamic adress2}
    Input By Name                   address.city            ${dynamic city}
    Input By Name                   address.zipCode         ${dynamic code}
    Select From Dropdown            (${dropdown menu})[1]   Alaska
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking New Shipto
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[1]      ${shipto number}
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[2]      shipto
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[3]      ${dynamic full adress}
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[4]      ${EMPTY}

Edit Shipto
    Click Element                   xpath:(${react table raw})[${my shipto}]
    Sleep                           2 second
    Input By Name                   number                  ${edit shipto number}
    Input By Name                   name                    edit-shipto
    Input By Name                   poNumber                4550
    Input By Name                   address.line1           ${edit adress1}
    Input By Name                   address.line2           ${edit adress2}
    Input By Name                   address.city            ${edit city}
    Input By Name                   address.zipCode         ${edit code}
    Select From Dropdown            (${dropdown menu})[1]   Arizona
    Input By Name                   notes                   Note
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking Shipto
    Goto Sidebar Customers
    Click Element                   xpath:(${react table raw})[${my customer}]
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[1]      ${edit shipto number}
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[2]      edit-shipto
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[3]      ${edit full adress}
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[4]      4550

Create New Customer User
    Click Element                   xpath:(${tab element})[3]
    Sleep                           2 second
    ${customer user number}         Get Element Count       xpath:${react table raw}
    ${my customer user}             Evaluate                ${customer user number}+1
    Set Suite Variable              ${my customer user}
    Click Element                   ${create button}
    Input By Name                   email                   ${customer user email}
    Select From Dropdown            (${dropdown menu})[1]   Customer User
    Input By Name                   firstName               ${user first name}
    Input By Name                   lastName                ${user last name}
    ${number of checkboxes}         Get Element Count       xpath:${checkbox type}
    Click Element                   xpath:(${checkbox type})[${number of checkboxes}]
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking New Customer User
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[1]      ${customer user email}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[2]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[3]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[4]      Customer User
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[5]      ${edit shipto number}

Edit Customer User
    Click Element                   xpath:(${react table raw})[${my customer user}]${user info}
    Sleep                           2 second
    Select From Dropdown            (${dropdown menu})[1]   Customer Super User
    Input By Name                   firstName               ${edit first name}
    Input By Name                   lastName                ${edit last name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    Goto Customer Users

Checking Edit User
    Sleep                           2 second
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[1]      ${customer user email}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[2]      ${edit first name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[3]      ${edit last name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[4]      Customer Super User

Delete Customer User
    Click Element                   xpath:(${react table raw})[${my customer user}]${delete user}
    Dialog Should Be About          ${edit first name} ${edit last name}
    Click Element                   xpath:(${dialog}${button})[3]
    Sleep                           5 second

Sorting Customer User
    [Tags]                          Sort
    Sort React                      1
    Sort React                      2
    Sort React                      3
    Sort React                      4

Filter Customer User
    [Tags]                          Filter
    Filter Add                      1       1       srx-group+dev-customer@agilevision.io
    Filter Add                      2       2       first
    Filter Add                      3       3       last

Delete Shipto
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Click Element                   xpath:(${react table raw})[${my shipto}]${delete shipto}
    Dialog Should Be About          ${edit shipto number}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Sorting ShipTo
    [Tags]                          Sort
    Sort React                      1
    Sort React                      2
    Sort React                      4

Filter ShipTo
    [Tags]                          Filter
    Filter Add                      1       1       2048
    Filter Add                      2       2       2048-name
    Filter Add                      3       4       9000

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Sidebar Customers
    Sleep                           5 second
    ${buffer}                       Generate Random Name L  10
    Set Suite Variable              ${customer user email}      customer.${buffer}@example.com
    Set Suite Variable              ${shipto number}            new-${buffer}
    Set Suite Variable              ${edit shipto number}       edit-${buffer}
    ${my customer}                  Get React Row By Text   1   ${customer_name}
    Set Suite Variable              ${my customer}
    Click Element                   xpath:(${react table raw})[${my customer}]
    Sleep                           1 second