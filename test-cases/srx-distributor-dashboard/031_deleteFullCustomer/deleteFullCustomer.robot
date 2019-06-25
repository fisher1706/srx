*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${delete customer name}             Delete Customer

*** Test Cases ***
Create Customer
    Click Element                   ${create button}
    Input By Name                   name            ${delete customer name}
    ${customer type}                Select First    (${dropdown menu})[1]
    Set Suite Variable              ${customer type}
    ${market type}                  Select First    (${dropdown menu})[2]
    Set Suite Variable              ${market type}
    ${warehouse}                    Select First    (${dropdown menu})[3]
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    ${my customer}                  Get React Row By Text   1   ${delete customer name}
    Set Suite Variable              ${my customer}

Checking Customer
    Element Text Should Be          xpath:((${react table raw})[${my customer}]${react table column})[1]      ${delete customer name}
    Element Text Should Be          xpath:((${react table raw})[${my customer}]${react table column})[2]      ${EMPTY}
    Element Text Should Be          xpath:((${react table raw})[${my customer}]${react table column})[4]      ${customer type}
    Element Text Should Be          xpath:((${react table raw})[${my customer}]${react table column})[5]      ${market type}

Create Shipto 1
    Click Element                   xpath:(${react table raw})[${my customer}]
    Sleep                           1 second
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Click Element                   ${create button}
    Input By Name                   name                    ${dynamic name}
    Input By Name                   address.line1           ${dynamic adress1}
    Input By Name                   address.line2           ${dynamic adress2}
    Input By Name                   address.city            ${dynamic city}
    Input By Name                   address.zipCode         ${dynamic code}
    Select From Dropdown            (${dropdown menu})[1]   Alaska
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking Shipto 1
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]      ${dynamic name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]      ${dynamic full adress}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]      ${EMPTY}

Create Customer User 1
    ${buffer}                       Generate Random Name L
    Set Suite Variable              ${delete customer user1}    ${buffer}@example.com
    Click Element                   xpath:(${tab element})[3]
    Sleep                           2 second
    Click Element                   ${create button}
    Input By Name                   email                   ${delete customer user1}
    Select From Dropdown            (${dropdown menu})[1]   Customer User
    Input By Name                   firstName               ${user first name}
    Input By Name                   lastName                ${user last name}
    ${number of checkboxes}         Get Element Count       xpath:${checkbox type}
    Click Element                   xpath:(${checkbox type})[${number of checkboxes}]
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking Customer User 1
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]      ${delete customer user1}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]      Customer User
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]      ${dynamic name}

Delete Shipto 1
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Click Element                   xpath:(${react table raw})[1]${delete shipto}
    Dialog Should Be About          ${dynamic name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Create Shipto 2
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Click Element                   ${create button}
    Input By Name                   name                    ${dynamic name}
    Input By Name                   address.line1           ${dynamic adress1}
    Input By Name                   address.line2           ${dynamic adress2}
    Input By Name                   address.city            ${dynamic city}
    Input By Name                   address.zipCode         ${dynamic code}
    Select From Dropdown            (${dropdown menu})[1]   Alaska
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    ${number of shiptos}            Get Element Count       xpath:${react table raw}
    Should Be Equal As Integers     ${number of shiptos}    1

Checking Shipto 2
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]      ${dynamic name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]      ${dynamic full adress}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]      ${EMPTY}

Create Customer User 2
    ${buffer}                       Generate Random Name L
    Set Suite Variable              ${delete customer user2}    ${buffer}@example.com
    Click Element                   xpath:(${tab element})[3]
    Sleep                           2 second
    Click Element                   ${create button}
    Input By Name                   email                   ${delete customer user1}
    Select From Dropdown            (${dropdown menu})[1]   Customer User
    Input By Name                   firstName               ${user first name}
    Input By Name                   lastName                ${user last name}
    ${number of checkboxes}         Get Element Count       xpath:${checkbox type}
    Click Element                   xpath:(${checkbox type})[${number of checkboxes}]
    Click Element                   xpath:${button submit}
    Sleep                           2 second
    Input By Name                   email                   ${delete customer user2}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking Customer User 2
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]      ${delete customer user2}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]      Customer User
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]      ${dynamic name}

Delete Customer
    Goto Sidebar Customers
    Sleep                           3 second
    Click Element                   xpath:(${react table raw})[${my customer}]${delete customer}
    Dialog Should Be About          ${delete customer name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    ${number of customers}          Get Element Count       xpath:${react table raw}
    ${start number of customers}    Evaluate    ${my customer}-1
    Should Be Equal As Integers     ${number of customers}      ${start number of customers}

Checking On Transactions
    [Tags]                          Check
    Goto Sidebar Order Status
    ${start shipto}                 Get Text                    xpath:${select control}/div/div
    Set Suite Variable              ${start shipto}
    Go Down Check

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Customers

Go Down Check
    Click Element                   xpath:${select control}
    ${count}                        Get Element Count       xpath:${select control}/../div[2]/div/div
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   ${text buffer sub}          Get Text                                xpath:${select control}/../div[2]/div/div[${index}]
    \   Run Keyword If              "${text buffer sub}"=="${delete customer name} - ${dynamic name}"   Fail    Customer was not deleted