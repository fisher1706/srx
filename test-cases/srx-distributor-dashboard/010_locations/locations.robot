*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Invalid Create New Location
    [Tags]                          InvalidCreateNewLocation
    Click Element                   xpath:${button primary}
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
    Click Element                   xpath:${button primary}
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
    Is Locations

Checking New Location
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${level 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       ${sub 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div       ${level 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div       ${sub 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]/div       ${level 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[8]/div       ${sub 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[9]/div       ${level 4}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[10]/div      ${sub 4}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div      ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      BUTTON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div      10

Edit Location
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]
    Input Text                      xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div/div/input             ${edit level 1}
    Press Key                       xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div/div/input             \ue007
    Sleep                           1 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]
    Input Text                      xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div/div/input             ${edit sub 1}
    Press Key                       xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div/div/input             \ue007
    Sleep                           1 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]
    Input Text                      xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div/div/input            ${edit sku}
    Press Key                       xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div/div/input            \ue007
    Sleep                           1 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]
    Input Text                      xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div/div/input            100
    Press Key                       xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div/div/input            \ue007
    Sleep                           1 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]
    Input Text                      xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div/div/input            20
    Press Key                       xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div/div/input            \ue007
    Sleep                           1 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]
    Input Text                      xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div/div/input            10
    Press Key                       xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div/div/input            \ue007
    Sleep                           1 second
    Click Element                   xpath:${button lg}
    Sleep                           5 second
    Reload Page

Checking Edit Location
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${edit level 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       ${edit sub 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div       ${level 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div       ${sub 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]/div       ${level 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[8]/div       ${sub 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[9]/div       ${level 4}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[10]/div      ${sub 4}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div      ${edit sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      BUTTON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      10
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      20
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div      100
    Sleep                           5 second

Delete Location
    [Tags]                          DeleteLocation
    Click Element                   ${check location}
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]          ${edit level 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]          ${edit sub 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]          ${level 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]          ${sub 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]          ${level 3}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]          ${sub 3}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[8]          ${level 4}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[9]          ${sub 4}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]         ${edit sku}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]         10
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]         20
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]         100
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           5 second

Sorting
    [Tags]                          Sorting
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
    Sorting Column                  13
    Sorting Column                  14
    Sorting Column                  15
    Sorting Column                  16
    Sorting Column                  17

Locations Filtration
    [Tags]                          Filter
    Filter Field                    15      17      G030PM036107NGQ5
    Filter Field                    1       2       161
    Filter Field                    2       3       loc1n
    Filter Field                    3       4       loc1v
    Filter Field                    4       5       loc2n
    Filter Field                    5       6       loc2v
    Filter Field                    6       7       loc3n
    Filter Field                    7       8       loc3v
    Filter Field                    8       9       loc4n
    Filter Field                    9       10      loc4v
    Filter Field                    10      11      STATIC SKU
    Filter Field                    11      12      test
    Filter Field                    12      14      0
    Filter Field                    13      15      20
    Filter Field                    14      16      100
    Filter Select Box               1       13      RFID

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Locations
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${check location}           xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input