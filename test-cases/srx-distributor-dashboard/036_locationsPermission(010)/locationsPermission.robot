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
    Click Element                   css:button.btn-primary
    Is Add Location
    Click Element                   css:.close
    Sleep                           2 second
    Is Locations
    Click Element                   css:button.btn-primary
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
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Locations

Valid Create New Location
    Click Element                   css:button.btn-primary
    Is Add Location
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
    Click Element                   css:.modal-dialog-ok-button
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
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           3 second
    Input Text                      id:orderingConfig-product-partSku_id                                                                    ${dynamic sku}
    Sleep                           2 second
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
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
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[12]/div      1138
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      BUTTON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      10

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
    Click Element                   css:.btn-lg
    Sleep                           5 second
    Reload Page
    Sleep                           3 second
    Go Down Selector                ${select control}           Static Customer - 2048

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
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[12]/div      1138
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      BUTTON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      10

Delete Location
    [Tags]                          DeleteLocation
    Click Element                   ${check location}
    Click Element                   css:.btn-danger
    Sleep                           1 second
    Click Element                   css:.close
    Is Locations
    Sleep                           2 second
    Click Element                   ${check location}
    Click Element                   css:.btn-danger
    Click Element                   css:.modal-footer > button:nth-child(1)
    Is Locations
    Sleep                           2 second
    Click Element                   ${check location}
    Click Element                   css:.btn-danger
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]          ${edit level 1}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]          ${edit sub 1}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[4]          ${level 2}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]          ${sub 2}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[6]          ${level 3}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[7]          ${sub 3}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[8]          ${level 4}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[9]          ${sub 4}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[10]         ${edit sku}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[11]         1138
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[14]         10
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           5 second

*** Keywords ***
Preparation
    Goto Security Groups
    ${permission test group}        Get Row By Text     (${table xpath})[2]     1       Permissions Test
    Set Suite Variable              ${edit group button}            xpath:(${table xpath})[2]/tbody/tr[${permission test group}]/td[2]/div/div[1]/button
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  7       1
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/ul/li[2]/a
    Clear All Settings Permissions
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           3 second
    Is Security Groups
    Finish Suite
    Sleep                           3 second
    Start Suite
    ${permissions email}            Return Permissions Email
    Input Text                      id:email        ${permissions email}
    Enter Password
    Correct Submit Login
    Click Link                      xpath://*[@href="/locations"]
    Goto Locations
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${check location}           xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input

Is Add Location
    Element Text Should Be          css:.modal-title            Add location