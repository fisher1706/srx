*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             Selenium2Library
Library                             String
Library                             RequestsLibrary
Library                             String
Library                             Collections
Library                             json
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

***Variables***
${pricing sku}                      PRICING_SKU
${pricing customer}                 Static Customer
${pricing shipto}                   2048
${request url locker}               https://${API_key}:${API_key}@api-dev.storeroomlogix.com/api/webhook/events/locker
*** Test Cases ***
Import Pricing
    Goto Sidebar Pricing
    Go Down Selector                (${select control})[1]      ${pricing customer}
    Go Down Selector                (${select control})[2]      ${pricing shipto}
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importPricing.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Valid Create New Location
    Goto Sidebar Locations
    Click Element                   xpath:${button primary}
    Input Text                      id:orderingConfig-product-partSku_id                    ${pricing sku}
    Go Down Selector                (${modal dialog}${select control})[1]                   LOCKER
    Input Text                      id:orderingConfig-currentInventoryControls-min_id       20
    Input Text                      id:orderingConfig-currentInventoryControls-max_id       60
    Input Text                      id:attributeName1_id                                    bla
    Input Text                      id:attributeValue1_id                                   bla1
    Input Text                      id:attributeName2_id                                    bla2
    Input Text                      id:attributeValue2_id                                   bla3
    Click Element                   xpath:${button modal dialog ok}
    sleep                           10 second

Request Locker
    [Tags]          Locker
    Create Session                  httpbin                  ${request url locker}        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /        data={ "currentWeight": 0, "distributorSku": "${pricing sku}", "kioskId": ${shipto_id}, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": 210, "quantityRequested": 10, "timestamp": "2018-10-30T11:22:48.806", "transactionStatus": "Issued", "weightOfProduct": 0, "user":"qweqwewe" }    headers=${headers}
    Log To Console          ${resp}

Check Transactions
    sleep                           5 second
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${pricing sku}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]      ${pricing sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[9]      ACTIVE
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[4]      $10.00
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            SHIPPED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Update Pricing
    Goto Sidebar Pricing
    Go Down Selector                (${select control})[1]      ${pricing customer}
    Go Down Selector                (${select control})[2]      ${pricing shipto}
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/updatePricing.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Request Locker New
    [Tags]          Locker
    Create Session                  httpbin                  ${request url locker}        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /        data={ "currentWeight": 0, "distributorSku": "${pricing sku}", "kioskId": ${shipto_id}, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": 100, "quantityRequested": 10, "timestamp": "2019-03-04T11:22:48.806", "transactionStatus": "Issued", "weightOfProduct": 0, "user":"qweqwewe" }    headers=${headers}
    Log To Console          ${resp}

Check Transactions New
    sleep                           5 second
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${pricing sku}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]      ${pricing sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[4]      $50.00
    Sleep                           5 second

Delete Location
    [Tags]                          DeleteLocation
    Goto Sidebar Locations
    ${number of row}                Get Rows Count              ${table xpath}
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]          bla
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]          bla1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]          bla2
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]          bla3
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]         ${pricing sku}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]         20
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]         60
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           5 second


*** Keywords ***
Preparation
    Start Distributor
    Sleep                           5 second
    Goto Sidebar Settings
    Click Element                   id:settings-tab-erp-integration
    Sleep                           1 second
    Click Element                   erp-integration-tab-pricing-integration
    Select Radio Button             pricingInfoSettings             SRX
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Sleep                           5 second