*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             RequestsLibrary
Library                             OperatingSystem
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${locker sku}                       LOCKER_SKU
${locker user}                      LOCKER_USER
${location value}                   lv1
${location name}                    ln1

*** Test Cases ***
Valid Create New Location
    Click Element                   xpath:${button primary}
    Input Text                      id:orderingConfig-product-partSku_id                    ${locker sku}
    Go Down Selector                (${modal dialog}${select control})[1]                   LOCKER
    Input Text                      id:orderingConfig-currentInventoryControls-min_id       30
    Input Text                      id:orderingConfig-currentInventoryControls-max_id       60
    Input Text                      id:attributeName1_id                                    ${location name}
    Input Text                      id:attributeValue1_id                                   ${location value}
    Go Down Selector                (${modal dialog}${select control})[2]                   CUSTOMER
    Click Element                   xpath:${button modal dialog ok}

Checking New Location
    Sleep                           7 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       CUSTOMER
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div       ${location name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div       ${location value}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      ${locker sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      LOCKER
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[17]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[18]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[21]/div      OFF

Request Locker Available
    [Tags]                          Locker
    ${request url locker}           Get Locker URL
    Create Session                  httpbin                  ${request url locker}        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /        data={ "currentWeight": 0, "distributorSku": "${locker sku}", "kioskId": ${shipto_id}, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": 170, "quantityRequested": 10, "timestamp": "2018-10-30T11:22:48.806", "transactionStatus": "Available", "weightOfProduct": 0, "user":"${locker user}" }    headers=${headers}

Checking OHI Available
    Reload Page
    Sleep                           4 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[20]/div      170

Checking Available In Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Last AL Element Should Be       2   Locker
    Last AL Element Should Be       3   LOCKER_SUBMIT
    Last AL Element Should Be       5   HARDWARE
    Last AL Element Should Be       6   ${locker user}
    Last AL Element Should Be       8   SUCCESS
    Expand Last AL
    Sleep                           1 second
    Expanded AL Element Should Be   6   170
    Expanded AL Element Should Be   10  AVAILABLE
    Expanded AL Element Should Be   17  ${locker sku}

Request Locker Issued
    [Tags]                          Locker
    ${request url locker}           Get Locker URL
    Create Session                  httpbin                  ${request url locker}        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /        data={ "currentWeight": 0, "distributorSku": "${locker sku}", "kioskId": ${shipto_id}, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": 170, "quantityRequested": 10, "timestamp": "2018-10-30T11:22:48.806", "transactionStatus": "Issued", "weightOfProduct": 0, "user":"${locker user}" }    headers=${headers}

Checking OHI Issued
    Goto Locations
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[20]/div      0

Checking Issued In Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Last AL Element Should Be       2   Locker
    Last AL Element Should Be       3   LOCKER_SUBMIT
    Last AL Element Should Be       5   HARDWARE
    Last AL Element Should Be       6   ${locker user}
    Last AL Element Should Be       8   SUCCESS
    Expand Last AL
    Sleep                           1 second
    Expanded AL Element Should Be   6   0
    Expanded AL Element Should Be   10  ISSUED
    Expanded AL Element Should Be   17  ${locker sku}

Checking Transaction In Activity Log
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[2]             Transaction
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[4]             Locker
    Click Element                   xpath:((${react table raw})[3]${react table column})[1]
    Element Text Should Be          xpath:((${expanded react table})[2]${react table column})[2]        170
    Element Text Should Be          xpath:((${expanded react table})[2]${react table column})[3]        LOCKER
    Element Text Should Be          xpath:((${expanded react table})[2]${react table column})[7]        ACTIVE
    Element Text Should Be          xpath:((${expanded react table})[2]${react table column})[11]       LOCKER_SKU

Delete Location
    Goto Locations
    Sleep                           5 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     ${location name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     ${location value}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[12]    ${locker sku}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    LOCKER
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]    0
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[16]    30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[17]    60
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[20]    OFF
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           7 second
    ${number of new row}            Get Rows Count          ${table xpath}
    Should Be Equal As Integers     ${number of new row}    ${number of row}

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Locations
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}