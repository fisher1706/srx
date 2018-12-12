*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Case ***
Invalid Create New Product
    [Tags]                          Catalog
    Click Element                   css:.btn-primary
    Is Add Product
    Click Element                   css:.close
    Sleep                           2 second
    Is Catalog
    Click Element                   css:.btn-primary
    Press Key                       id:partSku_id               \ue004
    Element Should Be Enabled       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:shortDescription_id      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:roundBuy_id              \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:unitOfMeasure_id         \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:roundBuy_id              \ue007
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:weight_id                \ue004
    Element Should Be Visible       css:.fa-exclamation-circle > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Catalog

Valid Create New Product
    [Tags]                          Catalog
    Click Element                   css:.btn-primary
    Is Add Product
    Input Text                      id:partSku_id                   ${random string}
    Input Text                      id:shortDescription_id          ${user last name}
    Input Text                      id:weight_id                    10
    Input Text                      id:roundBuy_id                  ${round by}
    Input Text                      id:unitOfMeasure_id             ${warehouse number}
    Input Text                      id:manufacturerPartNumber_id    ${dynamic code}
    Input Text                      id:longDescription_id           ${dynamic adress1}
    Input Text                      id:manufacturer_id              ${dynamic adress2}
    Input Text                      id:productLvl1_id               ${level 1}
    Input Text                      id:productLvl2_id               ${level 2}
    Input Text                      id:productLvl3_id               ${level 3}
    Input Text                      id:attribute1_id                ${sub 1}
    Input Text                      id:attribute2_id                ${sub 2}
    Input Text                      id:attribute3_id                ${sub 3}
    Input Text                      id:gtin_id                      ${dynamic city}
    Input Text                      id:upc_id                       ${test string}
    Input Text                      id:alternative_id               ${test number}
    Input Text                      id:keyword_id                   ${keyword}
    Input Text                      id:image_id                     ${keyword}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           3 second
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)

Checking New Product
    [Tags]                          Catalog
    Sleep                           3 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/div           ${random string}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div           ${user last name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div           ${round by}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[17]/div          10
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[20]/button
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]         ${random string}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]         ${dynamic code}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[3]/div[2]         ${user last name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[4]/div[2]         ${dynamic adress1}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[5]/div[2]         ${dynamic adress2}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[6]/div[2]         ${round by}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[7]/div[2]         ${level 1}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[8]/div[2]         ${level 2}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[9]/div[2]         ${level 3}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[10]/div[2]        ${sub 1}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[11]/div[2]        ${sub 2}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[12]/div[2]        ${sub 3}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[13]/div[2]        ${dynamic city}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[14]/div[2]        ${test string}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[15]/div[2]        ${test number}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[16]/div[2]        ${keyword}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[17]/div[2]        10
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[19]/div[2]        ${keyword}
    Click Element                   css:.close
    Sleep                           3 second

Edit Product
    [Tags]                          Catalog
    Click Element                   ${edit product button}
    Is Edit Product
    Click Element                   css:.close
    Sleep                           2 second
    Is Catalog
    Click Element                   ${edit product button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Catalog
    Click Element                   ${edit product button}
    Input Text                      id:partSku_id                       ${edit random string}
    Input Text                      id:shortDescription_id              ${edit last name}
    Input Text                      id:weight_id                        20
    Input Text                      id:roundBuy_id                      ${edit round by}
    Input Text                      id:unitOfMeasure_id                 ${edit warehouse number}
    Input Text                      id:manufacturerPartNumber_id        ${edit code}
    Input Text                      id:longDescription_id               ${edit adress1}
    Input Text                      id:manufacturer_id                  ${edit adress2}
    Input Text                      id:productLvl1_id                   ${edit level 1}
    Input Text                      id:productLvl2_id                   ${edit level 2}
    Input Text                      id:productLvl3_id                   ${edit level 3}
    Input Text                      id:attribute1_id                    ${edit sub 1}
    Input Text                      id:attribute2_id                    ${edit sub 2}
    Input Text                      id:attribute3_id                    ${edit sub 3}
    Input Text                      id:gtin_id                          ${edit city}
    Input Text                      id:upc_id                           ${edit string}
    Input Text                      id:alternative_id                   ${edit test number}
    Input Text                      id:keyword_id                       ${edit keyword}
    Input Text                      id:image_id                         ${edit keyword}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           3 second
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)

Checking Edit Product
    [Tags]                          Catalog
    Sleep                           3 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/div      ${edit random string}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div      ${edit last name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div      ${edit round by}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[17]/div     20
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[20]/button
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]         ${edit random string}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]         ${edit code}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[3]/div[2]         ${edit last name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[4]/div[2]         ${edit adress1}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[5]/div[2]         ${edit adress2}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[6]/div[2]         ${edit round by}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[7]/div[2]         ${edit level 1}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[8]/div[2]         ${edit level 2}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[9]/div[2]         ${edit level 3}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[10]/div[2]        ${edit sub 1}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[11]/div[2]        ${edit sub 2}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[12]/div[2]        ${edit sub 3}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[13]/div[2]        ${edit city}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[14]/div[2]        ${edit string}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[15]/div[2]        ${edit test number}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[16]/div[2]        ${edit keyword}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[17]/div[2]        20
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div[19]/div[2]        ${edit keyword}
    Set Global Variable             ${number of row}        ${number of new row}
    Click Element                   css:.close
    Sleep                           3 second

*** Keywords ***
Preparation
    Goto Security Groups
    Sleep                           5 second
    Number Of Rows G
    Number Of Static Row G
    Set Suite Variable              ${edit group button}            xpath:(${table xpath})[2]/tbody/tr[${static row g}]/td[2]/div/div[1]/button
    Click Element                   ${edit group button}
    Clear All Permissions
    Set Permission                  4       1
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/ul/li[2]/a
    Clear All Settings Permissions
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           3 second
    Is Security Groups
    Finish Suite
    Sleep                           3 second
    Start Suite
    Input Text                      id:email        srx-group+dev-permissions@agilevision.io
    Enter Password
    Correct Submit Login
    Click Link                      xpath://*[@href="/catalog"]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    Sleep                           3 second
    Number Of Rows
    ${number of new row}=           Evaluate                    ${number of row}+1
    Run Keyword If                  ${number of new row}==11    Set Global Variable     ${number of new row}    1
    ${buffer}=                      Generate Random String      18      [LETTERS]
    ${random string}=               Convert To Uppercase        ${buffer}
    ${buffer}=                      Generate Random String      18      [LETTERS]
    ${edit random string}=          Convert To Uppercase        ${buffer}
    Set Global Variable             ${random string}
    Set Global Variable             ${edit random string}
    Set Global Variable             ${number of new row}
    Set Global Variable             ${edit product button}      xpath:${table xpath}/tbody/tr[${number of new row}]/td[21]/div/div/button

Is Add Product
    Element Text Should Be          css:.modal-title            Add product

Is Edit Product
    Element Text Should Be          css:.modal-title            Edit product