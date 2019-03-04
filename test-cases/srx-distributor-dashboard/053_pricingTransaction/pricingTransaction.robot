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
    Input Text                      id:orderingConfig-currentInventoryControls-min_id       10
    Input Text                      id:orderingConfig-currentInventoryControls-max_id       60
    Input Text                      id:attributeName1_id                                    ${level 1}
    Input Text                      id:attributeValue1_id                                   ${sub 1}
    Input Text                      id:attributeName2_id                                    ${level 2}
    Input Text                      id:attributeValue2_id                                   ${sub 2}
    Click Element                   xpath:${button modal dialog ok}

Request Locker
    [Tags]          Locker
    Create Session                  httpbin                  ${request url locker}        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /        data={ "currentWeight": 0, "distributorSku": "${pricing sku}", "kioskId": ${shipto_id}, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": 210, "quantityRequested": 10, "timestamp": "2018-10-30T11:22:48.806", "transactionStatus": "Issued", "weightOfProduct": 0, "user":"qweqwewe" }    headers=${headers}
    Log To Console          ${resp}

Check Transactions
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${pricing sku}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]      ${pricing sku}
    #Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[4]      
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[9]      ACTIVE
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
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${pricing sku}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]      ${pricing sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[9]      ACTIVE

    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            SHIPPED
    Click Element                   xpath:${button modal dialog ok}
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