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

*** Test Cases ***
Create RFID
    Click Element                   xpath:${add rfid button}
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Input Text                      id:labelId_id               ${epc}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           5 second

Checking Assigned RFID
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ASSIGNED
    Element Text Should Be          xpath:(${react table column})[4]      ${email_dist}

Checking Assigned RFID In Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Last AL Element Should Be       2   RFID
    Last AL Element Should Be       3   RFID_TAG_ASSIGN
    Last AL Element Should Be       5   USER
    Last AL Element Should Be       6   ${email_dist}
    Last AL Element Should Be       8   SUCCESS

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

Checking Manifest RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      MANIFEST
    Element Text Should Be          xpath:(${react table column})[4]      ${email_dist}

Checking Manifest RFID In Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Last AL Element Should Be       2   RFID
    Last AL Element Should Be       3   RFID_TAG_MANIFEST
    Last AL Element Should Be       5   USER
    Last AL Element Should Be       6   ${email_dist}
    Last AL Element Should Be       8   SUCCESS

Webhook To Checkin
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Checkin RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      CHECK_IN
    Element Text Should Be          xpath:(${react table column})[4]      ${email_dist}

Checking Checkin RFID In Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Last AL Element Should Be       2   RFID
    Last AL Element Should Be       3   RFID_TAG_READ
    Last AL Element Should Be       5   HARDWARE
    Last AL Element Should Be       6   ${RFID_SN}
    Last AL Element Should Be       8   SUCCESS

Get RFID ID
    ${putaway url}                  Get Putaway URL
    Set Suite Variable              ${putaway url}
    Create Session                  httpbin                ${putaway url}/shiptos/${shipto_id}/rfids/search     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Get Request            httpbin     ?epc=${epc}      headers=${headers}
    Set Suite Variable              ${rfid id}      ${resp.json()['data']['id']}
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

Webhook To Issued
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Issued RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ISSUED
    Element Text Should Be          xpath:(${react table column})[4]      ${email_dist}

Checking Issued RFID In Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Last AL Element Should Be       2   RFID
    Last AL Element Should Be       3   RFID_TAG_READ
    Last AL Element Should Be       5   HARDWARE
    Last AL Element Should Be       6   ${RFID_SN}
    Last AL Element Should Be       8   SUCCESS

*** Keywords ***
Preparation
    Start Distributor
    Goto Sidebar RFID
    Sleep                           5 second
    ${id token}                     Execute Javascript              return (document.cookie.match(/idToken=(.*?);/))[1]
    Set Suite Variable              ${id token}
    Sleep                           5 second
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second


