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
    ${buffer}=                      Generate Random String      18      [LETTERS]
    ${epc}                          Convert To Uppercase        ${buffer}
    Set Suite Variable              ${epc}
    Input Text                      id:labelId_id               ${epc}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           5 second

Checking Assigned RFID
    Click Element                   xpath:${last page}
    Sleep                           7 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${epc}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]   ASSIGNED
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   ${email_dist}

Get Manifest
    ${manifest url}                 Get Manifest URL
    Set Suite Variable              ${manifest url}
    ${manifest}                     Generate Random String      18      [LETTERS]
    Create Session                  httpbin                 ${manifest url}     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Post Request            httpbin     /     data={"${manifest}"}    headers=${headers}
    Set Suite Variable              ${manifest id}          ${resp.json()['data']['id']}
    Sleep                           3 second

Add To Manifest
    ${shipto id}                    Get Shipto ID
    Set Suite Variable              ${shipto id}
    Create Session                  httpbin                 ${manifest url}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json     Authorization=${id token}
    ${resp}=                        Post Request            httpbin     /${manifest id}/shiptos/${shipto id}/items/add    data={"antennaPort": 21, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.36879Z"}    headers=${headers}
    Sleep                           3 second

Submit Manifest
    Create Session                  httpbin                 ${manifest url}     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Post Request            httpbin     /${manifest id}/submit   headers=${headers}
    Sleep                           5 second

Checking Manifest RFID
    Reload Page
    Sleep                           5 second
    Click Element                   xpath:${last page}
    Sleep                           7 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${epc}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]   MANIFEST
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   ${email_dist}

Webhook To Checkin
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Checkin RFID
    Reload Page
    Sleep                           5 second
    Click Element                   xpath:${last page}
    Sleep                           7 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${epc}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]   CHECK_IN
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   ${email_dist}

Get RFID ID
    ${putaway url}                  Get Putaway URL
    Set Suite Variable              ${putaway url}
    Create Session                  httpbin                ${putaway url}/shiptos/${shipto id}/rfids/search     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Get Request            httpbin     ?epc=${epc}      headers=${headers}
    Set Suite Variable              ${rfid id}      ${resp.json()['data']['id']}
    Sleep                           3 second

Put Away
    ${putaway url}                  Get Putaway URL
    Create Session                  httpbin                 ${putaway url}/shiptos/${shipto id}/rfids/${rfid id}/available     verify=true
    &{headers}=                     Create Dictionary       accept=application/json     Authorization=${id token}
    ${resp}=                        Post Request            httpbin     /       headers=${headers}

Checking Available RFID
    Reload Page
    Sleep                           5 second
    Click Element                   xpath:${last page}
    Sleep                           7 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${epc}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]   AVAILABLE
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   ${email_dist}

Webhook To Issued
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Checking Issued RFID
    Reload Page
    Sleep                           5 second
    Click Element                   xpath:${last page}
    Sleep                           7 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]   ${epc}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]   ISSUED
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]   ${email_dist}

*** Keywords ***
Preparation
    Goto RFID
    Sleep                           5 second
    ${id token}                     Execute Javascript              return (window.localStorage.toSource().match(/idToken':\"(.*?)"/))[1]
    Set Suite Variable              ${id token}
    Sleep                           5 second
    Input Text                      xpath:(${select control})[2]/div/div/input       STATIC SKU
    Press Key                       xpath:(${select control})[2]/div/div/input       \ue007
    Sleep                           5 second
    Click Element                   xpath:${last page}
    Sleep                           7 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Run Keyword If                  ${number of new row}==11    Set Suite Variable    ${number of new row}    1     ELSE    Set Suite Variable      ${number of new row}
    Set Suite Variable              ${number of row}
