*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
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
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[12]/div      1138
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[18]/div      OFF

Create RFID
    Click Link                      xpath://*[@href="/rfid-view"]
    Sleep                           3 second
    Input Text                      xpath:(${select control})[2]/div/div/input       ${change sku 1}
    Press Key                       xpath:(${select control})[2]/div/div/input       \ue007
    Sleep                           1 second
    Click Element                   xpath:${button primary}
    ${buffer}=                      Generate Random String      18      [LETTERS]
    ${epc}                          Convert To Uppercase        ${buffer}
    Set Suite Variable              ${epc}
    Input Text                      id:labelId_id               ${epc}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second

Request RFID
    [Tags]                          RFID
    ${request url rfid}             Get Request URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking RFID Status
    Reload Page
    Sleep                           5 second
    Input Text                      xpath:(${select control})[2]/div/div/input      ${change sku 1}
    Press Key                       xpath:(${select control})[2]/div/div/input      \ue007
    Sleep                           1 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[1]          ${epc}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]          ISSUED
    Element Should Be Disabled      xpath:${table xpath}/tbody/tr[1]${button danger}

Check Transactions
    Click Link                      xpath://*[@href="/transactions"]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]         ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[9]         ACTIVE
    Click Element                   xpath:${table xpath}/tbody/tr[1]${button success}
    Choose From Select Box          ${modal dialog}${select control}       SHIPPED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Reload Page
    Sleep                           3 second

Check Transaction Log
    Click Link                      xpath://*[@href="/transaction-log"]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           1 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]         ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[6]         SHIPPED
    Reload Page
    Sleep                           3 second

Change Location SKU
    Click Link                      xpath://*[@href="/locations"]
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
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[12]/div      1138
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[18]/div      OFF

Check Transactions After Change SKU
    Click Link                      xpath://*[@href="/transactions"]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]         ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[9]         ACTIVE

Check Transaction Log After Change SKU
    Click Link                      xpath://*[@href="/transaction-log"]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           1 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]         ${change sku 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[6]         SHIPPED

Delete Location
    Click Link                      xpath://*[@href="/locations"]
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ${level 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${sub 1}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     ${level 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     ${sub 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]    ${change sku 2}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[12]    RFID
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]    30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    60
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[16]    0
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[17]    OFF
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           3 second
    ${number of new row}            Get Rows Count          ${table xpath}
    Should Be Equal As Integers     ${number of new row}    ${number of row}

*** Keywords ***
Preparation
    Goto Locations
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}

Get Request URL
    ${serial number}                Get RFID SN
    Return From Keyword If          "${HOST}"=="distributor-dev.storeroomlogix.com"                 https://${serial number}:${serial number}@api-dev.storeroomlogix.com/api/webhook/events/rfid
    Return From Keyword If          "${HOST}"=="distributor-staging.storeroomlogix.com"             https://${serial number}:${serial number}@api-staging.storeroomlogix.com/api/webhook/events/rfid