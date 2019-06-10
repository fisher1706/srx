*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             Selenium2Library
Library                             String
Library                             RequestsLibrary
Library                             String
Library                             Collections
Library                             json
Library                             OperatingSystem
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
    Click Element                   xpath:${button info}
    Input Text                      id:orderingConfig-product-partSku_id                            ${dynamic sku}
    Choose From Select Box          (${modal dialog}${select control})[1]                   RFID
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
    Choose From Select Box          (${modal dialog}${select control})[2]                           CUSTOMER
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           2 second

Checking Location
    [Tags]                          CheckingLocation
    Sleep                           2 second
    ${number of row}                Get Rows Count              ${table xpath}
    Simple Table Comparing          Owned by            CUSTOMER                ${number of row}
    Simple Table Comparing          Location 1 Name     ${level 1}              ${number of row}
    Simple Table Comparing          Location 1 Value    ${sub 1}                ${number of row}
    Simple Table Comparing          Location 2 Name     ${level 2}              ${number of row}
    Simple Table Comparing          Location 2 Value    ${sub 2}                ${number of row}
    Simple Table Comparing          Location 3 Name     ${level 3}              ${number of row}
    Simple Table Comparing          Location 3 Value    ${sub 3}                ${number of row}
    Simple Table Comparing          Location 4 Name     ${level 4}              ${number of row}
    Simple Table Comparing          Location 4 Value    ${sub 4}                ${number of row}
    Simple Table Comparing          SKU                 ${dynamic sku}          ${number of row}
    Simple Table Comparing          Type                RFID                    ${number of row}
    Simple Table Comparing          Min                 10                      ${number of row}
    Simple Table Comparing          Max                 1000                    ${number of row}

Create RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      ${dynamic sku}
    Sleep                           5 second
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Create File                     ${CURDIR}/../../../resources/importRfid.csv     RFID ID,SKU,${\n}${epc},${dynamic sku},
    Sleep                           5 second
    Choose File                     id:upload-rfid-available        ${CURDIR}/../../../resources/importRfid.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}            Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}          ${dynamic sku}
    Sleep                           10 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      AVAILABLE
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM

Request RFID
    [Tags]                          RFID
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Original Transaction Order Status
    [Tags]                          CheckingOriginalTransaction
    Sleep                           2 second
    Goto Sidebar Order Status
    Sleep                           2 second
    Choose From Select Box          (${select control})[1]       ${customer_name} - ${shipto_name}
    Sleep                           2 second
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           1 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      3   ${dynamic sku}
    ${transaction_id}               Get Text            xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]
    Set Suite Variable              ${transaction_id}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]     ACTIVE

Checking Original Transaction Activity Log
    [Tags]                          CheckingOriginalTransactionActivityLog
    Goto Sidebar Activity Feed
    Sleep                           2 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]                      RFID
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]                      RFID_TAG_READ
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]                      RFID Reader
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]                      HARDWARE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[6]                      ${RFID_SN}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]                      SUCCESS
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]                      Transaction
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]                      CREATE
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[4]                      RFID Reader
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[5]                      HARDWARE
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[6]                      ${RFID_SN}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[8]                      SUCCESS

ExternalApi Update
    [Tags]                          ExternalApiUpdate
    ${request url update}           Get Update Request URL
    Create Session                  httpbin                 ${request url update}        verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json                       ApiKey=${API_key}
    ${resp}=                        Post Request            httpbin    /        data=[{"createdAt": "", "id": ${transaction_id}, "productPartSku": "${dynamic sku}", "quantity": 70, "status": "ORDERED", "updatedAt": "", "updatedBy": ""}]     headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Update Transaction Order Status
    [Tags]                          CheckingUpdateTransaction
    Goto Sidebar Order Status
    Sleep                           2 second
    Choose From Select Box          (${select control})[1]       ${customer_name} - ${shipto_name}
    Sleep                           2 second
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           1 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      3   ${dynamic sku}
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
    Sleep                           2 second
    Choose From Select Box          (${select control})[1]       ${customer_name} - ${shipto_name}
    Sleep                           2 second
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           1 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      3   ${dynamic sku}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${dynamic sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]     ORDERED
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[6]      10

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
    Simple Table Comparing          Owned by            CUSTOMER                    1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Name     ${level 1}                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Value    ${sub 1}                    1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 2 Name     ${level 2}                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 2 Value    ${sub 2}                    1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 3 Name     ${level 3}                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 3 Value    ${sub 3}                    1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 4 Name     ${level 4}                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 4 Value    ${sub 4}                    1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          SKU                 ${dynamic sku}              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Min                 10                          1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Max                 1000                        1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           3 second

Close Transaction
    [Tags]                          CloseTransaction
    Goto Sidebar Order Status
    Sleep                           2 second
    Choose From Select Box          (${select control})[1]       ${customer_name} - ${shipto_name}
    Sleep                           2 second
    ${number of row}                Get Rows Count              ${table xpath}
    :FOR    ${var}                  IN RANGE    1   ${number of row}+1
    \   Click Element               xpath:${table xpath}/tbody/tr[1]${button success}
    \   Choose From Select Box      ${modal dialog}${select control}            DELIVERED
    \   Click Element               xpath:${button modal dialog ok}
    \   Sleep                       5 second

***Keywords***
Preparation
    Start Distributor
    Set Order Status Settings

Get Split Request URL
    Return From Keyword             https://api-${environment}.storeroomlogix.com/api/distributor/items/${transaction_id}/split/10

Get Update Request URL
    Return From Keyword             https://api-${environment}.storeroomlogix.com/api/distributor/items/update

Goto Transaction Status Updates Logic
    Click Element                   id:settings-tab-erp-integration
    Sleep                           1 second
    Click Element                   id:erp-integration-tab-transaction-status
    Sleep                           3 second