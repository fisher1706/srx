*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Valid Add Distributor
    [Tags]                          ValidAddDistributor
    Click Element                   xpath:${button primary}
    Input Text                      id:name_id                      ${dynamic name}
    Input Text                      id:address.line1_id             ${dynamic adress1}
    Input Text                      id:address.line2_id             ${dynamic adress2}
    Input Text                      id:address.city_id              ${dynamic city}
    Choose From Select Box          (${select control})[1]          Alaska
    Go Down Selector                (${select control})[2]          Singular Billing
    Input Text                      id:invoiceEmail_id              ${dynamic email}
    Input Text                      id:address.zipCode_id           ${dynamic code}
    Click Element                   xpath:${button modal dialog ok}

Checking New Data
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${dynamic name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]   ${dynamic full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   Singular Billing
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]   ${dynamic email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]   ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]   ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[8]   ACTIVE

Edit Distributor
    [Tags]                          EditDistributor
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]${button info}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     ${dynamic name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[8]     ACTIVE
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Input Text                      id:name_id                                              ${edit name}
    Input Text                      id:address.line1_id                                     ${edit adress1}
    Input Text                      id:address.line2_id                                     ${edit adress2}
    Go Down Selector                (${select control})[2]                                  Bill By Warehouse
    Input Text                      id:address.city_id                                      ${edit city}
    Input Text                      id:invoiceEmail_id                                      ${edit email}
    Choose From Select Box          (${select control})[1]                                  Arizona
    Input Text                      id:address.zipCode_id                                   ${edit code}
    Click Element                   xpath:${button modal dialog ok}

Checking Edit Data
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${edit name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]   ${edit full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   Bill By Warehouse
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]   ${edit email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]   ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]   ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[8]   INACTIVE

Remove Distributor
    [Tags]                          RemoveDistributor
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     ${edit name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${edit full adress}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     Bill By Warehouse
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     ${edit email}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]     ON
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]     ON
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[8]     INACTIVE
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           3 second
    ${number of new row}            Get Rows Count          ${table xpath}
    Should Be Equal As Integers     ${number of new row}    ${number of row}

*** Keywords ***
Preparation
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/distributors"]
    Sleep                           5 second
    Open Full Table
    Sleep                           2 second
    ${number of row}                Get Rows Count      ${table xpath}
    ${number of new row}            Evaluate            ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}

