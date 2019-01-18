*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             RequestsLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Valid Create New Serial Number
    Click Element                   xpath:${button primary}
    Choose From Select Box          (${modal dialog}${select control})[1]       RFID Reader
    Choose From Select Box          (${modal dialog}${select control})[2]       Static Test
    Input Text                      xpath:${modal dialog}${form control}        12/12/2021, 12:00 A
    Click Element                   xpath:${button modal dialog ok}

Checking New Serial Number
    Sleep                           5 second
    ${serial number}                Get Text        xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]
    Set Suite Variable              ${serial number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]       RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       Static Test
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[10]       12/12/2021, 12:00 AM

Edit Serial Number
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            Srx-group-test-distributor
    Clear Element Text              xpath:${modal dialog}${form control}
    Input Text                      xpath:${modal dialog}${form control}        10/10/2022, 11:00 P
    Click Element                   xpath:${button modal dialog ok}

Checking Edit Serial Number
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]       ${serial number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]       RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       Srx-group-test-distributor
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[10]      10/10/2022, 11:00 PM

Checking Serial Number On Distributor Portal
    Goto Settings Sub
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[1]       ${serial number}
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[2]       RFID
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[10]      10/10/2022, 11:00 PM

Change Serial Number On Distributor Portal
    Click Element                   xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]${button success}
    Input Text                      id:deviceName_id                    MyDeviceRFID
    Choose From Select Box          (${modal dialog}${select control})[1]   Static Customer - 2048
    Choose From Select Box          (${modal dialog}${select control})[2]   First AZ Last AZ
    Choose From Select Box          (${modal dialog}${select control})[3]   srx group
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Checking Serial Number On Distributor Portal After Change
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[1]       ${serial number}
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[2]       RFID
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[3]       MyDeviceRFID
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[5]       Static Customer - 2048
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[7]       First AZ Last AZ\n(az_user@example.com)
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[9]       srx group\n(srx-group+dev-customer@agilevision.io)
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[10]      10/10/2022, 11:00 PM

Create RFID
    Click Link                      xpath://*[@href="/rfid-view"]
    Click Element                   xpath:${button primary}
    ${buffer}=                      Generate Random String      18      [LETTERS]
    Set Global Variable             ${buffer}
    Input Text                      id:labelId_id               ${buffer}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           3 second
    Click Element                   xpath:${last page}
    Sleep                           5 second
    ${my rfid}                      Get Row By Text  ${table xpath}     1       ${buffer}
    Element text Should Be          xpath:${table xpath}/tbody/tr[${my rfid}]/td[2]     ASSIGNED
    Finish Suite
    Sleep                           5 second

#Request RFID
#    [Tags]                          RFID
#    ${request url rfid}             Get Request URL
#    Create Session                  httpbin                  ${request url rfid}        verify=true
#    &{headers}=                     Create Dictionary        Content-Type=application/json
#    ${resp}=                        Post Request             httpbin    /issued        data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${buffer}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
#    Should Be Equal As Strings      ${resp}                  <Response [200]>

#Checking RFID Status
#    Reload Page
#    Sleep                           7 second
#    Open Full Table
#    ${my rfid}                      Get Row By Text  ${table xpath}     1       ${buffer}
#    Element text Should Be          xpath:${table xpath}/tbody/tr[${my rfid}]/td[2]     ISSUED
#    Finish Suite
#    Sleep                           5 second

Delete Serial Number
    Preparation
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]       ${serial number}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]       RFID
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]       Srx-group-test-distributor
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]       Static Customer - 2048
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]       First AZ Last AZ\n(az_user@example.com)
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[8]       srx group\n(srx-group+dev-customer@agilevision.io)
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[9]       10/10/2022, 11:00 PM
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

Sorting Serial Numbers
    [Tags]                          Sorting
    ${count}                        Get Rows Count      ${table xpath}
    Sort Column                     1       ${count}
    Sort Column                     2       ${count}
    Sort Column                     3       ${count}
    Sort Column                     4       ${count}
    Sort Column                     6       ${count}
    Sort Column                     10      ${count}

Filter Serial Numbers
    [Tags]                          Filter
    Click Element                   ${button right margin}
    Choose From Select Box          (${modal dialog}${select control})[1]       RFID Reader
    Click Element                   ${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${table xpath}/tbody/tr[${index}]/td[2]       RFID
    Click Element                   xpath:${button default}
    Sleep                           3 second
    Click Element                   ${button right margin}
    Choose From Select Box          (${modal dialog}${select control})[2]       Srx-group-test-distributor
    Click Element                   ${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${table xpath}/tbody/tr[${index}]/td[6]       Srx-group-test-distributor

*** Keywords ***
Preparation
    Start Admin
    Sleep                           3 second
    Click Link                      xpath://*[@href="/hardware"]
    Sleep                           5 second
    Open Full Table
    ${number of row}                Get Rows Count                  ${table xpath}
    ${number of new row}=           Evaluate                        ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${number of row}

Goto Settings Sub
    Finish Suite
    Start Distributor
    Sleep                           3 second
    Click Link                      xpath://*[@href="/settings"]
    Sleep                           1 second
    Click Element                   id:settings-tab-erp-integration
    Sleep                           1 second
    Click Element                   id:erp-integration-tab-claiming-hardware
    Sleep                           1 second
    ${my serial number}             Get Row By Text     ${claiming hardware pane}${table xpath}       1       ${serial number}
    Set Suite Variable              ${my serial number}