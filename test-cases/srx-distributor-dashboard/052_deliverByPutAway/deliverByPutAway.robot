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

*** Test Cases ***
Create Available RFID
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Create File                     ${CURDIR}/../../../resources/importRfid.csv     RFID ID,SKU,${\n}${epc},STATIC SKU,
    Sleep                           5 second
    Click Element                   xpath:${import rfid button}
    Sleep                           2 second
    Execute Javascript              document.getElementById("upload-rfid-available").style.display='block'
    Sleep                           1 second
    Choose File                     id:upload-rfid-available            ${CURDIR}/../../../resources/importRfid.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Select Location At Rfid Menu    Static Customer - 2048              STATIC SKU
    Sleep                           10 second
    Element Text Should Be          xpath:(${react table column})[1]    ${epc}
    Element Text Should Be          xpath:(${react table column})[2]    AVAILABLE
    Element Text Should Be          xpath:(${react table column})[4]    SYSTEM

Request RFID
    [Tags]                          RFID
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking RFID Status
    Select Location At Rfid Menu    Static Customer - 2048      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ISSUED
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM

Check Transactions
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]
    Sleep                           1 second
    ${my transaction}               Get Row By Text     ${table xpath}      2   STATIC SKU
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[2]      STATIC SKU
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[9]      ACTIVE
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            SHIPPED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Create Assigned RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    Static Customer - 2048      STATIC SKU
    Sleep                           5 second
    Click Element                   xpath:${add rfid button}
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Input Text                      id:labelId_id               ${epc}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           5 second

Get Manifest
    ${manifest url}                 Get Manifest URL
    Set Suite Variable              ${manifest url}
    ${manifest}                     Generate Random Name U
    Create Session                  httpbin                 ${manifest url}     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Post Request            httpbin     /     data={"${manifest}"}    headers=${headers}
    Set Suite Variable              ${manifest id}          ${resp.json()['data']['id']}
    Sleep                           3 second

Add To Manifest
    Set Suite Variable              ${shipto_id}
    Create Session                  httpbin                 ${manifest url}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json     Authorization=${id token}
    ${resp}=                        Post Request            httpbin     /${manifest id}/shiptos/${shipto_id}/items/add    data={"antennaPort": 21, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.36879Z"}    headers=${headers}
    Sleep                           3 second

Submit Manifest
    Create Session                  httpbin                 ${manifest url}     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Post Request            httpbin     /${manifest id}/submit   headers=${headers}
    Sleep                           5 second

Webhook To Checkin
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Get RFID ID
    ${putaway url}                  Get Putaway URL
    Set Suite Variable              ${putaway url}
    Create Session                  httpbin                 ${putaway url}/shiptos/${shipto_id}/rfids/search     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Get Request             httpbin     ?epc=${epc}      headers=${headers}
    Set Suite Variable              ${rfid id}              ${resp.json()['data']['id']}
    Sleep                           3 second

Put Away
    ${putaway url}                  Get Putaway URL
    Create Session                  httpbin                 ${putaway url}/shiptos/${shipto_id}/rfids/${rfid id}/available     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Post Request            httpbin     /       headers=${headers}

Checking Available RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    Static Customer - 2048      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      AVAILABLE
    Element Text Should Be          xpath:(${react table column})[4]      ${email_dist}

Checking Available RFID In Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Last AL Element Should Be       2   RFID
    Last AL Element Should Be       3   RFID_TAG_PUTAWAY
    Last AL Element Should Be       5   USER
    Last AL Element Should Be       6   ${email_dist}
    Last AL Element Should Be       8   SUCCESS
    Expand Last AL
    Sleep                           1 second
    Expanded AL Element Should Be   2   ${epc}
    Expanded AL Element Should Be   6   AVAILABLE
    Expanded AL Element Should Be   9   STATIC SKU

Checking Transaction In Activity Log
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[2]             Transaction
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[3]             UPDATE
    Click Element                   xpath:((${react table raw})[3]${react table column})[1]
    Element Text Should Be          xpath:((${expanded react table})[2]${react table column})[3]        RFID
    Element Text Should Be          xpath:((${expanded react table})[2]${react table column})[7]        DELIVERED
    Element Text Should Be          xpath:((${expanded react table})[2]${react table column})[11]       STATIC SKU

*** Keywords ***
Preparation
    Start Distributor
    Goto Sidebar RFID
    ${id token}                     Execute Javascript          return (document.cookie.match(/idToken=(.*?);/))[1]
    Set Suite Variable              ${id token}
    Sleep                           5 second
    Select Location At Rfid Menu    Static Customer - 2048      STATIC SKU
    Sleep                           5 second
