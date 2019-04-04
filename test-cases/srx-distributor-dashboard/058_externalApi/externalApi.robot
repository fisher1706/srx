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
Create Location
    [Tags]                          CreateLocation
    Goto Locations
    Sleep                           2 second
    Click Element                   xpath:${button primary}
    Input Text                      id:orderingConfig-product-partSku_id                            ${dynamic sku}
    Click Element                   xpath:${modal dialog}${select control}
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue007
    Input Text                      id:orderingConfig-currentInventoryControls-min_id               10
    Input Text                      id:orderingConfig-currentInventoryControls-max_id               1000
    Input Text                      id:attributeName1_id                                            ${level 1}
    Input Text                      id:attributeValue1_id                                           ${sub 1}
    Input Text                      id:attributeName2_id                                            ${level 2}
    Input Text                      id:attributeValue2_id                                           ${sub 2}
    Input Text                      id:attributeName3_id                                            ${level 3}
    Input Text                      id:attributeValue3_id                                           ${sub 3}
    Input Text                      id:attributeName4_id                                            ${level 4}
    Input Text                      id:attributeValue4_id                                           ${sub 4}
    Go Down Selector                (${modal dialog}${select control})[2]                           CUSTOMER
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           2 second

Checking Location
    [Tags]                          CheckingLocation
    Sleep                           2 second
    ${number of row}                Get Rows Count              ${table xpath}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div       CUSTOMER
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[4]/div       ${level 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[5]/div       ${sub 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[6]/div       ${level 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[7]/div       ${sub 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[8]/div       ${level 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[9]/div       ${sub 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[10]/div       ${level 4}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[11]/div      ${sub 4}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[12]/div      ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[14]/div      LOCKER
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[16]/div      10
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[17]/div      1000

Request Locker
    [Tags]                          Locker
    ${request url locker}           Get Locker URL
    Create Session                  httpbin                 ${request url locker}        verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin    /        data={ "currentWeight": 0, "distributorSku": "${dynamic sku}", "kioskId": ${shipto_id}, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": 30, "quantityRequested": 10, "timestamp": "2018-10-30T11:22:48.806", "transactionStatus": "Issued", "weightOfProduct": 0, "user":"example@example.com" }    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Original Transaction Order Status
    [Tags]                          CheckingOriginalTransaction
    Sleep                           2 second
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${dynamic sku}
    ${transaction_id}               Get Text            xpath:${table xpath}/tbody/tr[${my transaction}]/td[1]
    Set Suite Variable              ${transaction_id}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]     ACTIVE
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[6]      30

Checking Original Transaction Activity Log
    [Tags]                          CheckingOriginalTransactionActivityLog
    Goto Sidebar Activity Feed
    Sleep                           2 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]                      Locker
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]                      LOCKER_SUBMIT
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]                      Locker
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]                      HARDWARE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[6]                      example@example.com
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]                      SUCCESS
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]                      Transaction
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]                      CREATE
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[4]                      Locker
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[5]                      HARDWARE
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[6]                      example@example.com
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[8]                      SUCCESS

ExternalApi Update
    [Tags]                          ExternalApiUpdate
    ${request url update}           Get Update Request URL
    Create Session                  httpbin                 ${request url update}        verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json                       ApiKey=${API_key}
    ${resp}=                        Post Request            httpbin    /        data=[{"id": ${transaction_id}, "quantity": 70, "status": "ORDERED","productPartSku": "${dynamic sku}"}]     headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Update Transaction Order Status
    [Tags]                          CheckingUpdateTransaction
    Goto Sidebar Order Status
    Sleep                           5 second
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]     ORDERED
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[6]      70

Checking Update Transaction Activity Log
    [Tags]                          CheckingOriginalTransactionActivityLog
    Sleep                           2 second
    Goto Sidebar Activity Feed
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]                      Transaction
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]                      UPDATE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]                      USER
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[6]                      ${API_key}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]                      SUCCESS

ExternalApi Split
    [Tags]                          ExternalApiSplit
    ${request url split}            Get Split Request URL
    Create Session                  httpbin                 ${request url split}        verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json                         ApiKey=${API_key}
    ${resp}=                        Post Request                    httpbin    /       headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Split Transaction Order Status
    [Tags]                          CheckingUpdateTransactionOrderStatus
    Goto Sidebar Order Status
    Sleep                           5 second
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${dynamic sku}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]     ORDERED
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[6]      10
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}+1]/td[3]    ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}+1]/td[6]    60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}+1]/td[10]    ORDERED

Checking Split Transaction Activity Log
    [Tags]                          CheckingOriginalTransactionActivityLog
    Sleep                           2 second
    Goto Sidebar Activity Feed
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]                      Transaction
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]                      CREATE_BY_SPLIT
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]                      USER
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[6]                      ${API_key}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]                      SUCCESS
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]                      Transaction
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]                      SPLIT
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[5]                      USER
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[6]                      ${API_key}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[8]                      SUCCESS

Delete Location
    Goto Locations
    ${number of row}                Get Rows Count              ${table xpath}
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]          CUSTOMER
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]          ${level 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]          ${sub 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]          ${level 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]          ${sub 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]          ${level 3}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[8]          ${sub 3}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[9]          ${level 4}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]         ${sub 4}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[11]         ${dynamic sku}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]         10
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[16]         1000
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           3 second

Close Transaction
    [Tags]                          CloseTransaction
    Goto Sidebar Order Status
    Sleep                           2 second
    ${number of row}                Get Rows Count              ${table xpath}
    :FOR    ${var}                  IN RANGE                                1   ${number of row}
    \       ${my transaction}       Get Row By Text     ${table xpath}      2   ${dynamic sku}
    \       ${buffer}               Get Text            xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]
    \       Run Keyword If          "${buffer}" == "${dynamic sku}"           Make Delivered          ${my transaction}
    \       ${number of row}        Get Rows Count                          ${table xpath}
    \       Sleep                   2 seconds

***Keywords***
Preparation
    Start Distributor
    Sleep                           2 second
    ${number of row}                Get Rows Count              ${table xpath}
    Set Suite Variable              ${number of row}

Get Split Request URL
    Return From Keyword If          "${environment}"=="dev"                 https://api-dev.storeroomlogix.com/api/distributor/items/${transaction_id}/split/10
    Return From Keyword If          "${environment}"=="staging"             https://api-staging.storeroomlogix.com/api/distributor/items/${transaction_id}/split/10

Get Update Request URL
    Return From Keyword If          "${environment}"=="dev"                 https://api-dev.storeroomlogix.com/api/distributor/items/update
    Return From Keyword If          "${environment}"=="staging"             https://api-staging.storeroomlogix.com/api/distributor/items/update

Make Delivered
    [Arguments]                     ${row}
    Click Element                   xpath:${table xpath}/tbody/tr[${row}]/td[12]
    ${buf}                          Get Text                     xpath:${modal dialog}${select control}
    Run Keyword If                  "${buf}" == "ORDERED"        Ordered To Delivered        ELSE IF         "${buf}" == "ACTIVE"       Active To Delivered      ELSE        Log To Console      Unexpected Status
    Sleep                           1 second
    Click Element                   ${button modal dialog ok}

Ordered To Delivered
    Click Element                   xpath:${modal dialog}${select control}
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue007

Active To Delivered
    Click Element                   xpath:${modal dialog}${select control}
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue007
