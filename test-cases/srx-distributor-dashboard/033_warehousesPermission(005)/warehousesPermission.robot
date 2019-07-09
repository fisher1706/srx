*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Valid Create New Warehouse
    Click Element                   ${create button}
    Input By Name                   name                ${user first name}
    Input By Name                   number              ${warehouse number}
    Input By Name                   address.line1       ${dynamic adress1}
    Input By Name                   address.line2       ${dynamic adress2}
    Input By Name                   address.city        ${dynamic city}
    Select From Dropdown            (${dialog}${dropdown menu})[1]      Alaska
    Input By Name                   address.zipCode     ${dynamic code}
    Input By Name                   contactEmail        ${correct wrong email}
    Input By Name                   invoiceEmail        ${correct wrong email}
    Click Element                   xpath:${button submit}
    Sleep                           2 second

Checking New Warehouse
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[3]      ${warehouse number}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[4]      America/New_York (-04:00)
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]      ${dynamic full adress}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[6]      ${correct wrong email}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[7]      ${correct wrong email}

Edit Warehouse
    Click Element                   xpath:(${react table raw})[${number of new row}]${edit warehouse}
    Input By Name                   name                ${user last name}
    Input By Name                   number              ${edit warehouse number}
    Input By Name                   address.line1       ${edit adress1}
    Input By Name                   address.line2       ${edit adress2}
    Input By Name                   address.city        ${edit city}
    Select From Dropdown            (${dialog}${dropdown menu})[1]      Arizona
    Select From Dropdown            (${dialog}${dropdown menu})[2]      US/Hawaii (-10:00)
    Input By Name                   address.zipCode     ${edit code}
    Input By Name                   contactEmail        ${edit email}
    Input By Name                   invoiceEmail        ${edit email}
    Click Element                   xpath:${button submit}
    Sleep                           2 second

Checking Edit Warehouse
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[3]      ${edit warehouse number}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[4]      US/Hawaii (-10:00)
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]      ${edit full adress}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[6]      ${edit email}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[7]      ${edit email}

Delete User
    Click Element                   xpath:(${react table raw})[${number of new row}]${delete warehouse}
    Dialog Should Be About          ${user last name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Security Groups
    Sleep                           3 second
    ${permission test group}        Get Row Number      1       Permissions Test
    Click Element                   xpath:(${react table raw})[${permission test group}]${edit security group}
    Click Element                   xpath:${general permission card}
    Clear All General Permissions
    Set General Permission          Warehouses      1
    Click Element                   xpath:${settings permission card}
    Clear All Settings Permissions
    Click Element                   xpath:${button submit}
    Sleep                           3 second
    Finish Suite
    Sleep                           3 second
    Start Permission
    Sleep                           3 second
    Goto Sidebar Warehouses
    Sleep                           3 second
    ${number of row}                Get Element Count           xpath:${react table raw}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}