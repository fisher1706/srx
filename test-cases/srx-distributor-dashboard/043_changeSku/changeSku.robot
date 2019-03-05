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
    Click Element                   xpath:${button primary}
    Input Text                      id:orderingConfig-product-partSku_id                    ${change sku 1}
    Go Down Selector                (${modal dialog}${select control})[1]                   RFID
    Input Text                      id:orderingConfig-currentInventoryControls-min_id       30
    Input Text                      id:orderingConfig-currentInventoryControls-max_id       60
    Input Text                      id:attributeName1_id                                    ${level 1}
    Input Text                      id:attributeValue1_id                                   ${sub 1}
    Input Text                      id:attributeName2_id                                    ${level 2}
    Input Text                      id:attributeValue2_id                                   ${sub 2}
    Click Element                   xpath:${button modal dialog ok}

Checking New Location
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${level 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       ${sub 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div       ${level 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div       ${sub 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div      ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[19]/div      OFF

Create RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    Static Customer - 2048      ${change sku 1}
    Sleep                           5 second
    ${buffer}                       Generate Random String      18      [LETTERS]
    ${epc}                          Convert To Uppercase        ${buffer}
    Set Suite Variable              ${epc}
    Create File                     ${CURDIR}/../../../resources/importRfid.csv     RFID ID,SKU,${\n}${epc},${change sku 1},
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
    Select Location At Rfid Menu    Static Customer - 2048          ${change sku 1}
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
    Select Location At Rfid Menu    Static Customer - 2048      ${change sku 1}
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ISSUED
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM

Check Transactions
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${change sku 1}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]      ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[9]      ACTIVE
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            SHIPPED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Change Location SKU
    Goto Sidebar Locations
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]
    Input Text                      xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div/div/input            ${change sku 2}
    Press Key                       xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div/div/input            \ue007
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           3 second
    Click Element                   xpath:${button lg}

Checking Edit Location
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${level 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       ${sub 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div       ${level 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]/div       ${sub 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div      ${change sku 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[19]/div      OFF

Check Transactions After Change SKU
    Goto Sidebar Order Status
    Sleep                           1 second
    ${my transaction}               Get Row By Text     ${table xpath}      2   ${change sku 1}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]      ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[9]      SHIPPED

Deliver Transaction
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}       DELIVERED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Delete Location
    Goto Sidebar Locations
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ${level 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${sub 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     ${level 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     ${sub 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]    ${change sku 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[12]    RFID
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]    0
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]    60
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[17]    0
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[18]    OFF
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Sidebar Locations
    Sleep                           3 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
