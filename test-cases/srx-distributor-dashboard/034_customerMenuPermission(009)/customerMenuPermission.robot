*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Create New Shipto
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    ${shipto number}                Get Element Count       xpath:${react table raw}
    ${my shipto}                    Evaluate                ${shipto number}+1
    Set Suite Variable              ${my shipto}
    Click Element                   id:item-action-create
    Input By Name                   name                    ${dynamic name}
    Input By Name                   address.line1           ${dynamic adress1}
    Input By Name                   address.line2           ${dynamic adress2}
    Input By Name                   address.city            ${dynamic city}
    Input By Name                   address.zipCode         ${dynamic code}
    Select From Dropdown            (${dropdown menu})[1]   Alaska
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking New Shipto
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[1]      ${dynamic name}
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[2]      ${dynamic full adress}
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[3]      ${EMPTY}

Edit Shipto
    Click Element                   xpath:(${react table raw})[${my shipto}]
    Sleep                           2 second
    Input By Name                   name                    ${edit name}
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
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[1]      ${edit name}
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[2]      ${edit full adress}
    Element Text Should Be          xpath:((${react table raw})[${my shipto}]${react table column})[3]      4550

Create New Customer User
    Click Element                   xpath:(${tab element})[3]
    Sleep                           2 second
    ${customer user number}         Get Element Count       xpath:${react table raw}
    ${my customer user}             Evaluate                ${customer user number}+1
    Set Suite Variable              ${my customer user}
    Click Element                   id:item-action-create
    Input By Name                   email                   ${dynamic email}
    Select From Dropdown            (${dropdown menu})[1]   Customer User
    Input By Name                   firstName               ${user first name}
    Input By Name                   lastName                ${user last name}
    ${number of checkboxes}         Get Element Count       xpath:${checkbox type}
    Click Element                   xpath:(${checkbox type})[${number of checkboxes}]
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking New Customer User
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[1]      ${dynamic email}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[2]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[3]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[4]      Customer User
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[5]      ${edit name}

Edit Customer User
    Click Element                   xpath:(${react table raw})[${my customer user}]${edit user}
    Sleep                           2 second
    Select From Dropdown            (${dropdown menu})[1]   Customer Super User
    Input By Name                   firstName               ${edit first name}
    Input By Name                   lastName                ${edit last name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking Edit User
    Goto Sidebar Customers
    Click Element                   xpath:(${react table raw})[${my customer}]
    Click Element                   xpath:(${tab element})[3]
    Sleep                           2 second
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[1]      ${dynamic email}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[2]      ${edit first name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[3]      ${edit last name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[4]      Customer Super User

Delete Customer User
    Click Element                   xpath:(${react table raw})[${my customer user}]${delete user}
    Dialog Should Be About          ${edit first name} ${edit last name}
    Click Element                   xpath:(${dialog}${button})[3]
    Sleep                           5 second

Delete Shipto
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Click Element                   xpath:(${react table raw})[${my shipto}]${delete shipto}
    Dialog Should Be About          ${edit name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Security Groups
    Sleep                           5 second
    ${permission test group}        Get Row By Text     (${table xpath})[2]     1       Permissions Test
    Set Suite Variable              ${edit group button}            xpath:(${table xpath})[2]/tbody/tr[${permission test group}]${button success}
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  8       1
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/ul/li[2]/a
    Clear All Settings Permissions
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           3 second
    Finish Suite
    Sleep                           3 second
    Start Permission
    Sleep                           3 second
    Goto Sidebar Customers
    Sleep                           3 second
    ${my customer}                  Get React Row By Text   1   ${customer_name}
    Set Suite Variable              ${my customer}
    Click Element                   xpath:(${react table raw})[${my customer}]
    Sleep                           1 second
