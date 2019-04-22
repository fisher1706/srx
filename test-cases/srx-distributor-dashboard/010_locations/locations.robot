*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

***Variables***
${for edit}                         xpath://td[contains(@class, 'FOR-EDIT')]

*** Test Cases ***
Invalid Create New Location
    [Tags]                          InvalidCreateNewLocation
    Click Element                   xpath:${button info}
    Press Key                       id:orderingConfig-product-partSku_id                                                                    \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   xpath:${modal dialog}${select control}
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue004
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:orderingConfig-currentInventoryControls-min_id                                                       \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:orderingConfig-currentInventoryControls-max_id                                                       \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:attributeName1_id                                                                                    \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(5) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:attributeValue1_id                                                                                   \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(5) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           2 second

Valid Create New Location
    [Tags]                          ValidCreateNewLocation
    Click Element                   xpath:${button info}
    Input Text                      id:orderingConfig-product-partSku_id                                                                    ${dynamic sku}
    Click Element                   xpath:${modal dialog}${select control}
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue007
    Input Text                      id:orderingConfig-currentInventoryControls-min_id                                                       43
    Input Text                      id:orderingConfig-currentInventoryControls-max_id                                                       59
    Input Text                      id:attributeName1_id                                                                                    ${level 1}
    Input Text                      id:attributeValue1_id                                                                                   ${sub 1}
    Input Text                      id:attributeName2_id                                                                                    ${level 2}
    Input Text                      id:attributeValue2_id                                                                                   ${sub 2}
    Input Text                      id:attributeName3_id                                                                                    ${level 3}
    Input Text                      id:attributeValue3_id                                                                                   ${sub 3}
    Input Text                      id:attributeName4_id                                                                                    ${level 4}
    Input Text                      id:attributeValue4_id                                                                                   ${sub 4}
    Click Element                   xpath:(${modal dialog}${select control})[2]
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]            \ue015
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]            \ue007
    Click Element                   xpath:${button modal dialog ok}
    Element Text Should Be          css:.external-page-alert > strong:nth-child(2)                                                          Operation failed!
    Input Text                      id:orderingConfig-currentInventoryControls-min_id                                                       30
    Input Text                      id:orderingConfig-currentInventoryControls-max_id                                                       20
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Input Text                      id:orderingConfig-currentInventoryControls-max_id                                                       30
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Input Text                      id:orderingConfig-currentInventoryControls-min_id                                                       0
    Input Text                      id:orderingConfig-currentInventoryControls-max_id                                                       10
    Input Text                      id:orderingConfig-product-partSku_id                                                                    ${dynamic name}
    Sleep                           5 second
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Input Text                      id:orderingConfig-product-partSku_id                                                                    ${dynamic sku}
    Sleep                           5 second
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Checking New Location
    Sleep                           5 second
    Simple Table Comparing          Owned by            DISTRIBUTOR         ${number of new row}
    Simple Table Comparing          Location 1 Name     ${level 1}          ${number of new row}
    Simple Table Comparing          Location 1 Value    ${sub 1}            ${number of new row}
    Simple Table Comparing          Location 2 Name     ${level 2}          ${number of new row}
    Simple Table Comparing          Location 2 Value    ${sub 2}            ${number of new row}
    Simple Table Comparing          Location 3 Name     ${level 3}          ${number of new row}
    Simple Table Comparing          Location 3 Value    ${sub 3}            ${number of new row}
    Simple Table Comparing          Location 4 Name     ${level 4}          ${number of new row}
    Simple Table Comparing          Location 4 Value    ${sub 4}            ${number of new row}
    Simple Table Comparing          SKU                 ${dynamic sku}      ${number of new row}
    Simple Table Comparing          Type                BUTTON              ${number of new row}
    Simple Table Comparing          Critical Min        0                   ${number of new row}
    Simple Table Comparing          Min                 0                   ${number of new row}
    Simple Table Comparing          Max                 10                  ${number of new row}
    Simple Table Comparing          Surplus             OFF                 ${number of new row}

Checking New Location Activity Log
    [Tags]                          CheckingNewLocationActivityLog
    Goto Sidebar Activity Feed
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]             Location
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]             LOCATION_CREATE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]             USER
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[6]             ${email_dist}
    Element TExt Should Be          xpath:((${react table raw})[1]${react table column})[8]             SUCCESS

Edit Location
    [Tags]                          EditLocation
    Goto Locations
    Simple Table Editing            Location 1 Name     ${edit level 1}     ${number of new row}
    Sleep                           1 second
    Simple Table Editing            Location 1 Value    ${edit sub 1}       ${number of new row}
    Sleep                           1 second
    Simple Table Editing            SKU                 ${edit sku}         ${number of new row}
    Sleep                           1 second
    Simple Table Editing            Max                 100                 ${number of new row}
    Sleep                           1 second
    Simple Table Editing            Min                 20                  ${number of new row}
    Sleep                           1 second
    Simple Table Editing            Critical Min        10                  ${number of new row}
    Sleep                           1 second
    Click Element                   xpath:${button info}
    Sleep                           5 second
    Reload Page

Checking Edit Location
    [Tags]                          CheckingEdit
    Sleep                           5 second
    Simple Table Comparing          Owned by            DISTRIBUTOR             ${number of new row}
    Simple Table Comparing          Location 1 Name     ${edit level 1}         ${number of new row}
    Simple Table Comparing          Location 1 Value    ${edit sub 1}           ${number of new row}
    Simple Table Comparing          Location 2 Name     ${level 2}              ${number of new row}
    Simple Table Comparing          Location 2 Value    ${sub 2}                ${number of new row}
    Simple Table Comparing          Location 3 Name     ${level 3}              ${number of new row}
    Simple Table Comparing          Location 3 Value    ${sub 3}                ${number of new row}
    Simple Table Comparing          Location 4 Name     ${level 4}              ${number of new row}
    Simple Table Comparing          Location 4 Value    ${sub 4}                ${number of new row}
    Simple Table Comparing          SKU                 ${edit sku}             ${number of new row}
    Simple Table Comparing          Type                BUTTON                  ${number of new row}
    Simple Table Comparing          Critical Min        10                      ${number of new row}
    Simple Table Comparing          Min                 20                      ${number of new row}
    Simple Table Comparing          Max                 100                     ${number of new row}
    Simple Table Comparing          Surplus             OFF                     ${number of new row}
    Sleep                           5 second

Checking Edit Location Activity
    [Tags]                          CheckingEditLocationActivityLog
    Goto Sidebar Activity Feed
    Sleep                           3 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]             Location
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]             LOCATION_UPDATE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]             USER
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[6]             ${email_dist}
    Element TExt Should Be          xpath:((${react table raw})[1]${react table column})[8]             SUCCESS

Delete Location
    [Tags]                          DeleteLocation
    Goto Locations
    Click Element                   ${check location}
    Click Element                   xpath:${button danger}
    Simple Table Comparing          Owned by            DISTRIBUTOR             1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Name     ${edit level 1}         1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Value    ${edit sub 1}           1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 2 Name     ${level 2}              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 2 Value    ${sub 2}                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 3 Name     ${level 3}              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 3 Value    ${sub 3}                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 4 Name     ${level 4}              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 4 Value    ${sub 4}                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          SKU                 ${edit sku}             1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Type                BUTTON                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Critical Min        10                      1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Min                 20                      1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Max                 100                     1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           5 second

Checking Delete Location Activity Log
    [Tags]                          CheckingDeleteLocationsActivityLog
    Goto Sidebar Activity Feed
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]             Location
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]             LOCATION_DELETE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]             USER
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[6]             ${email_dist}
    Element TExt Should Be          xpath:((${react table raw})[1]${react table column})[8]             SUCCESS

Sorting
    [Tags]                          Sorting
    Goto Locations
    Sleep                           5 second
    Sorting Column                  2
    Sorting Column                  3
    Sorting Column                  4
    Sorting Column                  5
    Sorting Column                  6
    Sorting Column                  7
    Sorting Column                  8
    Sorting Column                  9
    Sorting Column                  10
    Sorting Column                  11
    Sorting Column                  12
    Sorting Column                  13
    Sorting Column                  15
    Sorting Column                  16
    Sorting Column                  17
    Sorting Column                  18

Locations Filtration
    [Tags]                          Filter
    Filter Field                    1       5       loc1n
    Filter Field                    2       6       loc1v
    Filter Field                    3       7       loc2n
    Filter Field                    4       8       loc2v
    Filter Field                    5       9       loc3n
    Filter Field                    6       10      loc3v
    Filter Field                    7       11      loc4n
    Filter Field                    8       12      loc4v
    Filter Field                    9       13      STATIC SKU
    Filter Field                    11      16      0
    Filter Field                    12      17      20
    Filter Field                    13      18      100
    Filter Select Box               1       3       MOVING
    Filter Select Box               3       15      RFID
    Filter Select Box               2       4       CUSTOMER

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Locations
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${check location}           xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input