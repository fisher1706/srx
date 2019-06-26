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
    Choose File                     id:upload-rfid-available            ${CURDIR}/../../../resources/importRfid.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}              STATIC SKU
    Sleep                           5 second
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
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ISSUED
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM

Check Transaction
    Goto Sidebar Order Status
    Sleep                           2 second
    Select Transaction Customer Shipto      ${customer_name} - ${shipto_name}
    Sleep                           2 second
    ${my transaction}               Get Row Number      3   STATIC SKU
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:((${react table raw})[${my transaction}]${react table column})[3]     STATIC SKU
    Element Text Should Be          xpath:((${react table raw})[${my transaction}]${react table column})[10]    ACTIVE
    Click Element                   xpath:(${react table raw})[${my transaction}]${edit transaction}
    Select From Dropdown            ${dialog}${dropdown menu}   SHIPPED
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Create Assigned RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Click Element                   ${create button}
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Input By Name                   labelId               ${epc}
    Click Element                   xpath:${button submit}
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
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
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

Checking Transaction In Activity Log
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     Transaction
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     UPDATE
    Click Element                   xpath:((${react table raw})[2]${react table column})[1]
    Element Text Should Be          xpath:((${react table raw})[6]${react table column})[2]     RFID
    Element Text Should Be          xpath:((${react table raw})[11]${react table column})[2]     DELIVERED
    Element Text Should Be          xpath:((${react table raw})[10]${react table column})[2]     STATIC SKU

*** Keywords ***
Preparation
    Start Distributor
    Set Order Status Settings
    Goto Sidebar RFID
    ${id token}                     Execute Javascript          return (document.cookie.match(/idToken=(.*?);/))[1]
    Set Suite Variable              ${id token}
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
