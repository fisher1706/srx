*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***
${filter clear}                     css:button.button-right-margin:nth-child(2)
${filter apply}                     css:button.btn:nth-child(2)
${filter button}                    css:.filtering-options > button:nth-child(1)

*** Test Cases ***
Invalid Add Distributor
    [Tags]                          InvalidAddDistributor
    Click Element                   xpath:${button primary}
    Press Key                       id:name_id                      \ue004
    Element Should Be Visible       xpath:(${help block})[1]/*
    Press Key                       id:address.line1_id             \ue004
    Element Should Be Visible       xpath:(${help block})[2]/*
    Press Key                       id:address.city_id              \ue004
    Element Should Be Visible       xpath:(${help block})[4]/*
    Press Key                       xpath:(${modal dialog}${select control})[1]/div[1]/div[2]   \ue004
    Element Should Be Visible       xpath:(${help block})[5]/*
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]   \ue004
    Element Should Be Visible       xpath:(${help block})[6]/*
    Press Key                       id:invoiceEmail_id              \ue004
    Element Should Be Visible       xpath:(${help block})[7]/*
    Press Key                       id:address.zipCode_id           \ue004
    Element Should Be Visible       xpath:(${help block})[8]/*
    Click Element                   xpath:${button close}
    Sleep                           2 second

Valid Add Distributor
    [Tags]                          ValidAddDistributor
    Click Element                   xpath:${button primary}
    Input Text                      id:name_id                                                                                          ${dynamic name}
    Input Text                      id:address.line1_id                                                                                 ${dynamic adress1}
    Input Text                      id:address.line2_id                                                                                 ${dynamic adress2}
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue007
    Input Text                      id:address.city_id                                                                                  ${dynamic city}
    Input Text                      id:invoiceEmail_id                                                                                  ${dynamic email}
    Click Element                   xpath:(${select control})[2]
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue007
    Input Text                      id:address.zipCode_id                                                                               ${dynamic code}
    Click Element                   xpath:${button modal dialog ok}

Checking New Data
    Sleep                           5 second
    Open Full Table
    Sleep                           2 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]       ${dynamic name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]       ${dynamic full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]       Singular Billing
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]       ${dynamic email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]       ACTIVE

Edit Distributor
    [Tags]                          EditDistributor
    Click Element                   ${edit button}
    Input Text                      id:name_id                                                                                          ${edit name}
    Input Text                      id:address.line1_id                                                                                 ${edit adress1}
    Input Text                      id:address.line2_id                                                                                 ${edit adress2}
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]        \ue007
    Input Text                      id:address.city_id                                                                                  ${edit city}
    Input Text                      id:invoiceEmail_id                                                                                  ${edit email}
    Click Element                   xpath:(${select control})[2]
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue013
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]        \ue007
    Input Text                      id:address.zipCode_id                                                                               ${edit code}
    Click Element                   xpath:${button modal dialog ok}

Checking Edit Data
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]       ${edit name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]       ${edit full adress}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]       Bill By Warehouse
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]       ${edit email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       ON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]       ACTIVE

Delete Distributor
    [Tags]                          RemoveDistributor
    Click Element                   ${delete button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     ${edit name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${edit full adress}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     Bill By Warehouse
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     ${edit email}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]     ON
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]     ACTIVE
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           4 second

Sorting Distributors By Name
    [Tags]                          Sorting
    Click Element                   css:th.sort-column:nth-child(1)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[1]/a
    Click Element                   css:th.sort-column:nth-child(1)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/a
    Should Be Equal	                ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(1)

Sorting Distributors By Number
    [Tags]                          Sorting
    Click Element                   css:th.sort-column:nth-child(2)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[2]/div
    Click Element                   css:th.sort-column:nth-child(2)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div
    Should Be Equal                 ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(2)

Sorting Distributors By Email
    [Tags]                          Sorting
    Click Element                   css:th.sort-column:nth-child(5)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[5]/div
    Click Element	                css:th.sort-column:nth-child(5)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}]/td[5]/div
    Should Be Equal                 ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(5)
    
Name Filter
    [Tags]                          NameFilter          Filter
    Click Element                   ${filter button}
    Click Element                   css:.close
    Sleep                           2 second
    Click Element                   ${filter button}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           2 second
    Click Element                   ${filter button}
    Input Text                      css:div.row-spaced:nth-child(1) > div:nth-child(2) > input:nth-child(1)     ${static name}
    Apply Filter

Number Filter
    [Tags]                          NumberFilter                    Filter
    Click Element                   ${filter button}
    Input Text                      css:div.row-spaced:nth-child(2) > div:nth-child(2) > input:nth-child(1)     ${static number}
    Apply Filter

Email Filter
    [Tags]                          EmailFilter                     Filter
    Click Element                   ${filter button}
    Input Text                      css:div.row-spaced:nth-child(3) > div:nth-child(2) > input:nth-child(1)     ${static email}
    Apply Filter

*** Keywords ***
Preparation
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/distributors"]
    Open Full Table
    Sleep                           2 second
    ${number of row}                Get Rows Count      ${table xpath}
    ${number of new row}            Evaluate            ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit button}      xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Set Suite Variable              ${delete button}    xpath:${table xpath}/tbody/tr[${number of new row}]${button danger}

Apply Filter
    Sleep                           1 second
    Click Element                   ${filter apply}
    Sleep                           3 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[1]/a       ${static name}
    Click Element                   ${filter clear}