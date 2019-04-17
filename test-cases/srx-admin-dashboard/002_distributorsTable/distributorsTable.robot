*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Invalid Add Distributor
    [Tags]                          InvalidAddDistributor
    Click Element                   xpath:${button primary}
    Click Element                   id:name_id
    Press Key                       id:name_id                      \ue004
    Element Should Be Visible       xpath:(${help block})[1]/*
    Press Key                       id:address.line1_id             \ue004
    Element Should Be Visible       xpath:(${help block})[2]/*
    Press Key                       id:address.city_id              \ue004
    Element Should Be Visible       xpath:(${help block})[4]/*
    Press Key                       id:invoiceEmail_id              \ue004
    Element Should Be Visible       xpath:(${help block})[5]/*
    Press Key                       xpath:(${modal dialog}${select control})[1]/div[1]/div[2]   \ue004
    Press Key                       xpath:(${modal dialog}${select control})[1]/div[1]/div[2]   \ue004
    Element Should Be Visible       xpath:(${help block})[6]/*
    Press Key                       id:address.zipCode_id           \ue004
    Element Should Be Visible       xpath:(${help block})[7]/*
    Click Element                   xpath:${button close}
    Sleep                           2 second

Valid Add Distributor
    [Tags]                          ValidAddDistributor
    Click Element                   xpath:${button primary}
    Input Text                      id:name_id                                      ${dynamic name}
    Input Text                      id:address.line1_id                             ${dynamic adress1}
    Input Text                      id:address.line2_id                             ${dynamic adress2}
    Input Text                      id:address.city_id                              ${dynamic city}
    Input Text                      id:invoiceEmail_id                              ${dynamic email}
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]      \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]      \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]      \ue007
    Input Text                      id:address.zipCode_id                           ${dynamic code}
    Click Element                   xpath:${button modal dialog ok}

Checking New Data
    Sleep                           5 second
    Open Full Table
    Sleep                           2 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]       ${dynamic name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]       ${dynamic full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]       ${dynamic email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]       ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]       ACTIVE

Edit Distributor
    [Tags]                          EditDistributor
    Click Element                   ${edit button}
    Input Text                      id:name_id                                      ${edit name}
    Input Text                      id:address.line1_id                             ${edit adress1}
    Input Text                      id:address.line2_id                             ${edit adress2}
    Input Text                      id:address.city_id                              ${edit city}
    Input Text                      id:invoiceEmail_id                              ${edit email}
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]      \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]      \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]      \ue007
    Input Text                      id:address.zipCode_id                           ${edit code}
    Click Element                   xpath:${button modal dialog ok}

Checking Edit Data
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]       ${edit name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]       ${edit full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]       ${edit email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]       ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]       ACTIVE

Delete Distributor
    [Tags]                          RemoveDistributor
    Click Element                   ${delete button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     ${edit name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${edit full adress}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     ${edit email}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     ON
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]     ON
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]     ACTIVE
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           4 second

Sorting Distributors
    [Tags]                          Sorting
    Sort Column                     1   ${number of row}
    Sort Column                     2   ${number of row}
    Sort Column                     4   ${number of row}
    Sort Column                     5   ${number of row}
    Sort Column                     6   ${number of row}
    Sort Column                     7   ${number of row}

Distributor Filtration
    [Tags]                          Filter
    Filter Field                    1   1   ${static name}
    Filter Field                    2   2   32
    Filter Field                    3   4   srx-group@agilevision.io

*** Keywords ***
Preparation
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/distributors"]
    Sleep                           2 second
    ${number of row}                Get Rows Count      ${table xpath}
    ${number of new row}            Evaluate            ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit button}      xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Set Suite Variable              ${delete button}    xpath:${table xpath}/tbody/tr[${number of new row}]${button danger}