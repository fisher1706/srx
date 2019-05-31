*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             RequestsLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Create New Customer User
    ${buffer}                       Generate Random Name L  10
    Set Suite Variable              ${fob user email}       fob.${buffer}@example.com
    ${customer user number}         Get Element Count       xpath:${react table raw}
    ${my customer user}             Evaluate                ${customer user number}+1
    Set Suite Variable              ${my customer user}
    Click Element                   id:item-action-create
    Input By Name                   email                   ${fob user email}
    Select From Dropdown            (${dropdown menu})[1]   Customer Super User
    Input By Name                   firstName               ${user first name}
    Input By Name                   lastName                ${user last name}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking New Customer User
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[1]      ${fob user email}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[2]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[3]      ${user last name}
    Element Text Should Be          xpath:((${react table raw})[${my customer user}]${react table column})[4]      Customer Super User

Create First FOB
    Click Element                   xpath:(${react table raw})[${my customer user}]
    Sleep                           2 second
    Click Element                   xpath:(${tab element})[2]
    Sleep                           1 second
    Click Element                   id:item-action-create
    ${fob epc 1}                    Generate Random Name U  18
    Set Suite Variable              ${fob epc 1}
    Input By Name                   epc             ${fob epc 1}
    Input By Name                   firstName       fob1-${user first name}
    Input By Name                   lastName        fob1-${user last name}
    Click Element                   xpath:${button submit}
    Sleep                           3 second

Checking First FOB
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]      ${fob epc 1}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]      fob1-${user first name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]      fob1-${user last name}

Create Second FOB
    Click Element                   id:item-action-create
    ${fob epc 2}                    Generate Random Name U  18
    Set Suite Variable              ${fob epc 2}
    Input By Name                   epc             ${fob epc 2}
    Input By Name                   firstName       fob2-${user first name}
    Input By Name                   lastName        fob2-${user last name}
    Click Element                   xpath:${button submit}
    Sleep                           3 second

Checking Second FOB
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[1]      ${fob epc 2}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]      fob2-${user first name}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]      fob2-${user last name}

Request First FOB
    [Tags]                          RFID
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${fob epc 1}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Delete FOB
    Click Element                   xpath:(${react table raw})[1]${delete fob}
    Dialog Should Be About          ${fob epc 1}
    Click Element                   xpath:(${dialog}${button})[3]
    Sleep                           5 second
    ${fobs number}                  Get Element Count       xpath:${react table raw}
    Run Keyword If                  ${fobs number}!=1       Fail    There are more than 1 fob

First Checking Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     FOB
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     FOB_READ
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[4]     RFID Reader
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[8]     SUCCESS
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]     FOB
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]     FOB_DELETE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]     SUCCESS

Request Second FOB
    [Tags]                          RFID
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${fob epc 2}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Second Read Checking Activity Log
    Reload Page
    Sleep                           4 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]     FOB
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]     FOB_READ
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]     RFID Reader
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]     SUCCESS

Delete Customer User
    Goto Customer Users
    Sleep                           2 second
    Click Element                   xpath:(${react table raw})[${my customer user}]${delete user}
    Dialog Should Be About          ${user first name} ${user last name}
    Click Element                   xpath:(${dialog}${button})[3]
    Sleep                           5 second

Second Checking Activity Log
    Goto Sidebar Activity Feed
    Sleep                           4 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]     FOB
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]     FOB_DELETE
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]     SUCCESS

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Customer Users
    Sleep                           2 second