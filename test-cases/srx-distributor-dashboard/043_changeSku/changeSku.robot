*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             OperatingSystem
Library                             RequestsLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${change sku 1}                     CHANGE SKU 1
${change sku 2}                     CHANGE SKU 2

*** Test Cases ***
Valid Create New Location
    Click Element                   xpath:${button info}
    Input Text                      id:orderingConfig-product-partSku_id                    ${change sku 1}
    Choose From Select Box          (${modal dialog}${select control})[1]                   RFID
    Input Text                      id:orderingConfig-currentInventoryControls-min_id       30
    Input Text                      id:orderingConfig-currentInventoryControls-max_id       60
    Input Text                      id:attributeName1_id                                    ${level 1}
    Input Text                      id:attributeValue1_id                                   ${sub 1}
    Input Text                      id:attributeName2_id                                    ${level 2}
    Input Text                      id:attributeValue2_id                                   ${sub 2}
    Choose From Select Box          (${modal dialog}${select control})[2]                   CUSTOMER
    Click Element                   xpath:${button modal dialog ok}

Checking New Location
    Sleep                           7 second
    Simple Table Comparing          Owned by            CUSTOMER            ${number of new row}
    Simple Table Comparing          Location 1 Name     ${level 1}          ${number of new row}
    Simple Table Comparing          Location 1 Value    ${sub 1}            ${number of new row}
    Simple Table Comparing          Location 2 Name     ${level 2}          ${number of new row}
    Simple Table Comparing          Location 2 Value    ${sub 2}            ${number of new row}
    Simple Table Comparing          SKU                 ${change sku 1}     ${number of new row}
    Simple Table Comparing          Type                RFID                ${number of new row}
    Simple Table Comparing          Critical Min        0                   ${number of new row}
    Simple Table Comparing          Min                 30                  ${number of new row}
    Simple Table Comparing          Max                 60                  ${number of new row}
    Simple Table Comparing          Surplus             OFF                 ${number of new row}

Create RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      ${change sku 1}
    Sleep                           5 second
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Create File                     ${CURDIR}/../../../resources/importRfid.csv     RFID ID,SKU,${\n}${epc},${change sku 1},
    Sleep                           5 second
    Choose File                     id:upload-rfid-available        ${CURDIR}/../../../resources/importRfid.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}            Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}          ${change sku 1}
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

Checking RFID Status
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      ${change sku 1}
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ISSUED
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM

Check Transactions
    Goto Sidebar Order Status
    Sleep                           2 second
    Choose From Select Box          (${select control})[1]       ${customer_name} - ${shipto_name}
    Sleep                           2 second
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           1 second
    ${my transaction}               Get Row By Text     ${table xpath}      3   ${change sku 1}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]     ACTIVE
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            SHIPPED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Change Location SKU
    [Tags]                          Change
    Goto Locations
    Sleep                           5 second
    Simple Table Editing            SKU                 ${change sku 2}     ${number of new row}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           3 second
    Click Element                   xpath:${button primary}
    Sleep                           4 second
    Reload Page

Checking Edit Location
    Sleep                           5 second
    Simple Table Comparing          Owned by            CUSTOMER            ${number of new row}
    Simple Table Comparing          Location 1 Name     ${level 1}          ${number of new row}
    Simple Table Comparing          Location 1 Value    ${sub 1}            ${number of new row}
    Simple Table Comparing          Location 2 Name     ${level 2}          ${number of new row}
    Simple Table Comparing          Location 2 Value    ${sub 2}            ${number of new row}
    Simple Table Comparing          SKU                 ${change sku 2}     ${number of new row}
    Simple Table Comparing          Type                RFID                ${number of new row}
    Simple Table Comparing          Critical Min        0                   ${number of new row}
    Simple Table Comparing          Min                 30                  ${number of new row}
    Simple Table Comparing          Max                 60                  ${number of new row}
    Simple Table Comparing          Surplus             OFF                 ${number of new row}

Check Transactions After Change SKU
    Goto Sidebar Order Status
    Sleep                           2 second
    Choose From Select Box          (${select control})[1]       ${customer_name} - ${shipto_name}
    Sleep                           2 second
    ${my transaction}               Get Row By Text     ${table xpath}      3   ${change sku 1}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]      SHIPPED

Deliver Transaction
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}       DELIVERED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Delete Location
    Goto Locations
    Sleep                           5 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Simple Table Comparing          Owned by            CUSTOMER                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Name     ${level 1}              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Value    ${sub 1}                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 2 Name     ${level 2}              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 2 Value    ${sub 2}                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          SKU                 ${change sku 2}         1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Type                RFID                    1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Critical Min        0                       1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Min                 30                      1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Max                 60                      1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Set Order Status Settings
    Goto Locations
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
