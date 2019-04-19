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
${usage history sku}                USAGE HISTORY

*** Test Cases ***
Valid Create New Location
    Click Element                   xpath:${button primary}
    Input Text                      id:orderingConfig-product-partSku_id                    ${usage history sku}
    Go Down Selector                (${modal dialog}${select control})[1]                   RFID
    Input Text                      id:orderingConfig-currentInventoryControls-min_id       30
    Input Text                      id:orderingConfig-currentInventoryControls-max_id       60
    Input Text                      id:attributeName1_id                                    ${level 1}
    Input Text                      id:attributeValue1_id                                   ${sub 1}
    Input Text                      id:attributeName2_id                                    ${level 3}
    Input Text                      id:attributeValue2_id                                   ${sub 3}
    Go Down Selector                (${modal dialog}${select control})[2]                   CUSTOMER
    Click Element                   xpath:${button modal dialog ok}

Checking New Location
    Sleep                           7 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       CUSTOMER
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       ${level 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div       ${sub 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div       ${level 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[7]/div       ${sub 3}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[12]/div      ${usage history sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[17]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[18]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[20]/div      OFF

Create RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      ${usage history sku}
    Sleep                           5 second
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Create File                     ${CURDIR}/../../../resources/importRfid.csv     RFID ID,SKU,${\n}${epc},${usage history sku},
    Sleep                           5 second
    Click Element                   xpath:${import rfid button}
    Sleep                           2 second
    Execute Javascript              document.getElementById("upload-rfid-available").style.display='block'
    Sleep                           1 second
    Choose File                     id:upload-rfid-available        ${CURDIR}/../../../resources/importRfid.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}            Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}          ${usage history sku}
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
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      ${usage history sku}
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ISSUED
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM

Check Transactions
    [Tags]                          Transactions
    Goto Sidebar Order Status
    Sleep                           3 second
    Choose From Select Box          (${select control})[1]       ${customer_name} - ${shipto_name}
    Sleep                           2 second
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           1 second
    ${my transaction}               Get Row By Text     ${table xpath}      3   ${usage history sku}
    Set Suite Variable              ${my transaction}
    ${order number}                 Get Text    xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]
    Set Suite Variable              ${order number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${usage history sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]     ACTIVE
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            DELIVERED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Checking Usage History
    Goto Usage History
    Click Element                   xpath:${button filter}
    Click Element                   xpath:(${menu}${menu item})[1]
    Input Text                      xpath:${text field}     ${order number}
    Sleep                           7 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]     ${order number}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]     ${EMPTY}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]     ${shipto_name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]     ${EMPTY}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]     ${usage history sku}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]     Delivered
    Click Element                   xpath:${filter type}/button
    Sleep                           3 second

Sorting Usage History
    [Tags]                          Sorting
    Sorting React With Last Page    1
    Sorting React With Last Page    2
    Sorting React With Last Page    3
    Sorting React With Last Page    4
    Sorting React With Last Page    5
    Sorting React With Last Page    6
    Sorting React With Last Page    7
    Sorting React With Last Page    8

Filter Activity Log
    [Tags]                          Filter
    Filter Add                      1   1   98719701
    Filter Add                      2   2   1138
    Filter Add                      3   3   14096
    Filter Add                      4   4   test101
    Filter Add                      5   5   PAND F1X4LG6
    Filter Add                      6   6   1950

Delete Location
    Goto Locations
    Sleep                           5 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${level 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     ${sub 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     ${level 3}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]     ${sub 3}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[11]    ${usage history sku}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    RFID
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]    0
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[16]    30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[17]    60
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[19]    OFF
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
