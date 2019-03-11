*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Invalid Create New Warehouse
    Click Element                   xpath:${button primary}
    Sleep                           1 second
    Click Element                   xpath:${button close}
    Sleep                           2 second
    Click Element                   xpath:${button primary}
    Press Key                       id:address.line1_id     \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[1]/*
    Press Key                       id:name_id              \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[2]/*
    Press Key                       id:number_id            \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[4]/*
    Press Key                       id:address.city_id      \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[5]/*
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]   \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[7]/*
    Press Key                       id:address.zipCode_id   \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[8]/*
    Press Key                       id:contactEmail_id      \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[9]/*
    Press Key                       id:invoiceEmail_id      \ue004
    Element Should Be Visible       xpath:(${modal dialog}${help block})[10]/*
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second

Valid Create New Warehouse
    [Tags]                          ValidCreateNewWarehouse
    Click Element                   xpath:${button primary}
    Input Text                      id:name_id              ${user first name}
    Input Text                      id:address.line1_id     ${dynamic adress1}
    Input Text                      id:address.line2_id     ${dynamic adress2}
    Input Text                      id:number_id            ${warehouse number}
    Input Text                      id:address.city_id      ${dynamic city}
    Click Element                   xpath:(${modal dialog}${select control})[2]
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]        \ue007
    Input Text                      id:contactEmail_id      ${incorrect email}
    Input Text                      id:address.zipCode_id   ${dynamic code}
    Input Text                      id:invoiceEmail_id      ${incorrect email}
    Element Should Be Visible       xpath:(${modal dialog}${help block})[10]/*
    Element Should Be Visible       xpath:(${modal dialog}${help block})[9]/*
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
    Choose From Select Box          (${modal dialog}${select control})[1]                           US/Hawaii (-10:00)
    Click Element                   xpath:(${modal dialog}${select control})[2]
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]       \ue015
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]       \ue015
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]       \ue007
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

Sorting Warehouses
    [Tags]                          Sorting
    Sorting Column                  1
    Sorting Column                  2
    Sorting Column                  3
    Sorting Column                  6
    Sorting Column                  7

Warehouse Filtration
    [Tags]                          Filter
    Filter Field                    1   1   Z_Warehouse
    Filter Field                    2   3   9999
    Filter Field                    3   6   warehouseZ@example.com

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Warehouses
    Sleep                           5 second
    Reload Page
    Sleep                           5 second
    ${number of row}                Get Rows Count                  ${table xpath}
    ${number of new row}=           Evaluate                        ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${edit warehouse button}        xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Set Suite Variable              ${delete warehouse button}      xpath:${table xpath}/tbody/tr[${number of new row}]${button danger}