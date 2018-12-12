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
    Input Text                      id:orderingConfig-currentInventoryControls-max_id                                                       40
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
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      40

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
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      40

Delete Location
    [Tags]                          DeleteLocation
    Click Element                   ${check location}
    Click Element                   css:.btn-danger
    Is Delete Location
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
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[13]         30
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[14]         40
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           5 second

Sorting
    [Tags]                          Sorting
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

Locations Filtration
    [Tags]                          Filter
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[15]/div[2]/input                    G030PM036107NGQ5
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/input                     161
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/input                     loc1n
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/input                     loc1v
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[4]/div[2]/input                     loc2n
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[5]/div[2]/input                     loc2v
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[6]/div[2]/input                     loc3n
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[7]/div[2]/input                     loc3v
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[8]/div[2]/input                     loc4n
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[9]/div[2]/input                     loc4v
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[10]/div[2]/input                    STATIC SKU
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[11]/div[2]/input                    1138
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[13]/div[2]/input                    20
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[14]/div[2]/input                    100
    Field Selector Check            xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[12]/div[2]/div/div/div/div/div[1]   RFID

*** Keywords ***
Preparation
    Goto Locations
    Number Of Rows
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Global Variable             ${number of new row}
    Set Global Variable             ${check location}           xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input

Is Add Location
    Element Text Should Be          css:.modal-title            Add location

Is Delete Location
    Element Text Should Be          css:.modal-title            Removal Confirmation

Filter Check
    [Arguments]                     ${inputField}            ${inputText}
    Click Element                   css:.button-right-margin
    Input Text                      ${inputField}            ${inputText}
    ${result} =                     Fetch From Left          ${inputField}    2]/input
    ${newString}=                   Strip String             ${result}1]/div
    ${fieldName}                    Get Text                 ${newString}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           2 seconds
    ${rowNum}                       Get Element Count        xpath:${header xpath}/thead/tr/th
    ${rowNum}=                      Evaluate                 ${rowNum}+1
     :FOR   ${var}                  IN RANGE            1    ${rowNum}
    \       ${textInfo}             Get Text                 xpath:${header xpath}/thead/tr/th[${var}]
    \       Run Keyword If          "${textInfo}" == "${fieldName}"      Field Comparing   ${var}        ${inputText}
    Click Element                   css:button.button-right-margin:nth-child(2)
    Sleep                           2 seconds

Field Comparing
    [Arguments]                     ${rowNum}               ${expectedValue}
    ${rowValue}                     Get Text                xpath:${table xpath}/tbody/tr[1]/td[${rowNum}]
    Should Be Equal As Strings      ${rowValue}             ${expectedValue}

Field Selector Check
    [Arguments]                     ${fieldAdr}             ${fieldType}
    Click Element                   css:.button-right-margin
    ${result} =                     Fetch From Left         ${fieldAdr}    2]/div/div/div/div/div[1]
    ${newString}=                   Strip String            ${result}1]/div
    ${fieldName}                    Get Text                ${newString}
    Go Down                         ${fieldAdr}             ${fieldType}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           3 seconds
    ${rowNum}                       Get Element Count       xpath:${header xpath}/thead/tr/th
    ${rowNum}=                      Evaluate                ${rowNum}+1
     :FOR    ${var}                 IN RANGE            1   ${rowNum}
    \       ${textInfo}             Get Text                xpath:${header xpath}/thead/tr/th[${var}]
    \       Run Keyword If          "${textInfo}" == "${fieldName}"      Field Comparing   ${var}        ${fieldType}
    Click Element                   css:button.button-right-margin:nth-child(2)
    Sleep                           2 seconds

Go Down
    [Arguments]                     ${fieldAdr}             ${field type}
    Click Element                   ${fieldAdr}
    ${result} =                     Fetch From Left         ${fieldAdr}    div/div[1]
    ${newString}=                   Strip String            ${result}div[1]/div[2]
    Press Key                       ${newString}            \ue015
    Press Key                       ${newString}            \ue007              
    ${text buffer sub}              Get Text                ${fieldAdr}
    Sleep                           1 second
    Run Keyword If                  "${text buffer sub}"!="${field type}"        Go Down    ${fieldAdr}    ${field type}
