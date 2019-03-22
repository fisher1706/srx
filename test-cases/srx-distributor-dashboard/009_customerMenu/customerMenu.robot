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

Delete Shipto
    Click Element                   xpath:(${react table raw})[${my shipto}]${delete shipto}
    Dialog Should Be About          ${edit name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Sidebar Customers
    Sleep                           5 second
    ${my customer}                  Get React Row By Text   1   ${customer_name}
    Set Suite Variable              ${my customer}
    Click Element                   xpath:(${react table raw})[${my customer}]
    Sleep                           1 second