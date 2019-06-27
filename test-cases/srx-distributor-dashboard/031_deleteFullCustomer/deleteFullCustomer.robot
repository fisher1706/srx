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
    ${shipto number 1}              Generate Random Name L
    Click Element                   xpath:(${react table raw})[${my customer}]
    Sleep                           1 second
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Click Element                   ${create button}
    Input By Name                   number                  ${shipto number 1}
    Input By Name                   address.line1           ${dynamic adress1}
    Input By Name                   address.line2           ${dynamic adress2}
    Input By Name                   address.city            ${dynamic city}
    Input By Name                   address.zipCode         ${dynamic code}
    Select From Dropdown            (${dropdown menu})[1]   Alaska
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking Shipto 1
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]      ${shipto number 1}
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
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]      ${shipto number 1}

Delete Shipto 1
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Click Element                   xpath:(${react table raw})[1]${delete shipto}
    Dialog Should Be About          ${shipto number 1}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Create Shipto 2
    ${shipto number 2}              Generate Random Name L
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Click Element                   ${create button}
    Input By Name                   number                  ${shipto number 2}
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
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]      ${shipto number 2}
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
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]      ${shipto number 2}

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

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Customers