*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${auto submit sku}                  AUTO_SUBMIT

*** Test Cases ***
Valid Create New Location
    Click Element                   css:button.btn-primary
    Input Text                      id:orderingConfig-product-partSku_id                    ${auto submit sku}
    Go Down Selector                (${modal dialog}${select control})[1]                   LOCKER
    Input Text                      id:orderingConfig-currentInventoryControls-min_id       30
    Input Text                      id:orderingConfig-currentInventoryControls-max_id       60
    Input Text                      id:attributeName1_id                                    ${level 1}
    Input Text                      id:attributeValue1_id                                   ${sub 1}
    Input Text                      id:attributeName2_id                                    ${level 2}
    Input Text                      id:attributeValue2_id                                   ${sub 2}
    Input Text                      id:attributeName3_id                                    ${level 3}
    Input Text                      id:attributeValue3_id                                   ${sub 3}
    Go Down Selector                (${modal dialog}${select control})[2]                   ON
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           2 second

Checking New Location
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${level 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       ${sub 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div       ${level 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div       ${sub 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]/div       ${level 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[8]/div       ${sub 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div      ${auto submit sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[12]/div      1138
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      LOCKER
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[18]/div      ON

Select Pricing
    Click Link                      xpath://*[@href="/settings"]
    Click Element                   id:settings-tab-erp-integration
    Sleep                           1 second
    Click Element                   id:erp-integration-tab-pricing-integration
    Sleep                           2 second
    Click Element                   xpath:(${pricing integrations}${radio button})[2]
    Click Element                   xpath:${pricing integrations}${control button}
    Sleep                           2 Second

Configure Submit Settings
    Click Link                      xpath://*[@href="/customers"]
    ${my customer}                  Get Row By Text     ${table xpath}      1   Static Customer
    Click Element                   xpath:${table xpath}/tbody/tr[${my customer}]/td[1]/a
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-replenishment-rules
    Click Element                   xpath:${customer repl rule}${control button}
    Sleep                           2 second
    ${checked}                      Get Element Attribute       xpath:${customer repl rule}${checkbox type}     checked
    Run Keyword If                  "${checked}"!="true"        Click Element       xpath:${customer repl rule}${checkbox type}
    Sleep                           1 second
    Click Element                   xpath:${customer repl rule}${control button}
    Sleep                           1 second

Configure Shipto Not Ordering
    Click Link                      xpath://*[@href="/customers"]
    ${my customer}                  Get Row By Text     ${table xpath}      1   Static Customer
    Click Element                   xpath:${table xpath}/tbody/tr[${my customer}]/td[1]/a
    Click Element                   id:customer-details-tab-shiptos
    ${my shipto}                    Get Row By Text     ${table xpath}      1   2048
    Set Suite Variable              ${my shipto}
    Click Element                   xpath:${table xpath}/tbody/tr[${my shipto}]${button success}
    Clear Element Text              id:poNumber_id
    Element Should Be Visible       xpath:${modal dialog}${alert warning}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           2 second
    Click Element                   xpath:${table xpath}/tbody/tr[${my shipto}]${button default}
    Element Should Be Visible       xpath:${modal dialog}${alert warning}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           1 second

Configure Shipto As Order
    Click Element                   xpath:${table xpath}/tbody/tr[${my shipto}]${button success}
    Input Text                      id:poNumber_id          4550
    Section Is Not Present          xpath:${modal dialog}${alert warning}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           2 second
    Click Element                   xpath:${table xpath}/tbody/tr[${my shipto}]${button default}
    Section Is Not Present          xpath:${modal dialog}${alert warning}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           1 second

Delete Locations
    Click Link                      xpath://*[@href="/locations"]
    Click Element                   ${check location}
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]      ${level 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]      ${sub 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]      ${level 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]      ${sub 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]      ${level 3}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]      ${sub 3}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]     ${auto submit sku}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[11]     1138
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[12]     LOCKER
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]     30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]     60
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[17]     ON
    Click Element                   xpath:${modal dialog}${button danger}

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Click Link                      xpath://*[@href="/locations"]
    Sleep                           3 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${check location}           xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
