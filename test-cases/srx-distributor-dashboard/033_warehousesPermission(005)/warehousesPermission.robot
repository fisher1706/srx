*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Valid Create New Warehouse
    [Tags]                          ValidCreateNewWarehouse
    Click Element                   xpath:${button info}
    Input Text                      id:name_id              ${user first name}
    Input Text                      id:address.line1_id     ${dynamic adress1}
    Input Text                      id:address.line2_id     ${dynamic adress2}
    Input Text                      id:number_id            ${warehouse number}
    Input Text                      id:address.city_id      ${dynamic city}
    Choose From Select Box          (${modal dialog}${select control})[2]       Alaska
    Input Text                      id:contactEmail_id      ${incorrect email}
    Input Text                      id:address.zipCode_id   ${dynamic code}
    Input Text                      id:invoiceEmail_id      ${incorrect email}
    Element Should Be Visible       xpath:(${modal dialog}${help block})[7]/*
    Element Should Be Visible       xpath:(${modal dialog}${help block})[8]/*
    Input Text                      id:contactEmail_id      ${correct wrong email}
    Input Text                      id:invoiceEmail_id      ${correct wrong email}
    Click Element                   xpath:${button modal dialog ok}

Checking New Warehouse
    [Tags]                          ValidCreateNewWarehouse
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${user first name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]   ${warehouse number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   America/New_York (-04:00)
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]   ${dynamic full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]   ${correct wrong email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]   ${correct wrong email}

Edit Warehouse
    [Tags]                          EditWarehouse
    Click Element                   ${edit warehouse button}
    Sleep                           1 second
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   ${edit warehouse button}
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second
    Click Element                   ${edit warehouse button}
    Input Text                      id:name_id              ${user last name}
    Input Text                      id:address.line1_id     ${edit adress1}
    Input Text                      id:address.line2_id     ${edit adress2}
    Input Text                      id:number_id            ${edit warehouse number}
    Input Text                      id:address.city_id      ${edit city}
    Choose From Select Box          (${modal dialog}${select control})[1]       US/Hawaii (-10:00)
    Choose From Select Box          (${modal dialog}${select control})[2]       Arizona
    Input Text                      id:address.zipCode_id   ${edit code}
    Input Text                      id:contactEmail_id      ${edit email}
    Input Text                      id:invoiceEmail_id      ${edit email}
    Click Element                   xpath:${button modal dialog ok}

Checking Edit Warehouse
    [Tags]                          EditWarehouse
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${user last name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]   ${edit warehouse number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   US/Hawaii (-10:00)
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]   ${edit full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]   ${edit email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]   ${edit email}

Delete Warehouse
    [Tags]                          DeleteWarehouse
    Click Element                   ${delete warehouse button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]      ${user last name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]      ${edit warehouse number}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]      US/Hawaii (-10:00)
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]      ${edit full adress}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]      ${edit email}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]      ${edit email}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           10 second

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
    Set Permission                  17      1
    Click Element                   xpath:(${dialog tab})[2]
    Clear All Settings Permissions
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           3 second
    Finish Suite
    Sleep                           3 second
    Start Permission
    Sleep                           3 second
    Goto Sidebar Warehouses
    Sleep                           3 second
    ${number of row}                Get Rows Count              ${table xpath}
    Set Suite Variable              ${number of row}
    ${number of new row}=           Evaluate                        ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit warehouse button}        xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Set Suite Variable              ${delete warehouse button}      xpath:${table xpath}/tbody/tr[${number of new row}]${button danger}