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
Valid Create New Serial Number
    Click Element                   xpath:${button info}
    Choose From Select Box          (${modal dialog}${select control})[1]       RFID Reader
    Choose From Select Box          (${modal dialog}${select control})[2]       Static Test
    Input Text                      xpath:${modal dialog}${form control}        12/12/2021, 12:00 A
    Click Element                   xpath:${modal dialog}${button modal dialog ok}

Checking New Serial Number
    Sleep                           5 second
    ${serial number}                Get Text        xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]
    Set Suite Variable              ${serial number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]       RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       Static Test
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[10]      12/12/2021, 12:00 AM

Edit Serial Number
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            ${distributor_name}
    Clear Element Text              xpath:${modal dialog}${form control}
    Input Text                      xpath:${modal dialog}${form control}        10/10/2022, 11:00 P
    Click Element                   xpath:${button modal dialog ok}

Checking Edit Serial Number
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]       ${serial number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]       RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       ${distributor_name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[10]      10/10/2022, 11:00 PM

Checking Serial Number On Distributor Portal
    Goto Settings Sub
    Element Text Should Be          xpath:((${react table raw})[${my serial number}]${react table column})[1]       ${serial number}
    Element Text Should Be          xpath:((${react table raw})[${my serial number}]${react table column})[2]       RFID
    Element Text Should Be          xpath:((${react table raw})[${my serial number}]${react table column})[7]       10/10/2022, 11:00 PM

Change Serial Number On Distributor Portal
    Click Element                   xpath:(${react table raw})[${my serial number}]${edit serial number}
    Input By Name                   deviceName      MyDeviceRFID
    Select From Dropdown            (${dialog}${dropdown menu})[1]      ${customer_name} - ${shipto_name}
    Sleep                           5 second
    ${dist user}                    Select First    (${dialog}${dropdown menu})[2]
    ${cust user}                    Select First    (${dialog}${dropdown menu})[3]
    Click Element                   xpath:${button submit}
    Set Suite Variable              ${dist user}
    Set Suite Variable              ${cust user}
    Sleep                           5 second

Checking Serial Number On Distributor Portal After Change
    ${my serial number}             Get Row Number      1       ${serial number}
    Set Suite Variable              ${my serial number}
    Element Text Should Be          xpath:((${react table raw})[${my serial number}]${react table column})[1]       ${serial number}
    Element Text Should Be          xpath:((${react table raw})[${my serial number}]${react table column})[2]       RFID
    Element Text Should Be          xpath:((${react table raw})[${my serial number}]${react table column})[3]       MyDeviceRFID
    Element Text Should Be          xpath:((${react table raw})[${my serial number}]${react table column})[4]       ${customer_name} - ${shipto_name}
    ${buffer}                       Get Text    xpath:((${react table raw})[${my serial number}]${react table column})[5]
    ${name}     ${email}            Split String    ${buffer}   (
    ${name}                         Strip String    ${name}     mode=right
    Should Be Equal As Strings      ${dist user}    ${name}
    ${buffer}                       Get Text    xpath:((${react table raw})[${my serial number}]${react table column})[6]
    ${name}     ${email}            Split String    ${buffer}   (
    ${name}                         Strip String    ${name}     mode=right
    Should Be Equal As Strings      ${cust user}    ${name}
    Element Text Should Be          xpath:((${react table raw})[${my serial number}]${react table column})[7]       10/10/2022, 11:00 PM

Create RFID
    Goto Sidebar RFID
    Sleep                           5 second
    ${epc}                          Generate Random Name U
    Set Suite Variable              ${epc}
    Create File                     ${CURDIR}/../../../resources/importRfid.csv     RFID ID,SKU,${\n}${epc},STATIC SKU,
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Choose File                     id:upload-rfid-available        ${CURDIR}/../../../resources/importRfid.csv
    Sleep                           5 second
    Page Should Contain             Validation status: valid
    Click Element                   xpath:(${dialog}${button})[2]
    Sleep                           10 second

Checking Available RFID
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      AVAILABLE
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM

Request RFID
    [Tags]                          RFID
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                  ${request url rfid}        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /issued        data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${epc}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                  <Response [200]>

Checking Issued RFID
    Select Location At Rfid Menu    ${customer_name} - ${shipto_name}      STATIC SKU
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc}
    Element Text Should Be          xpath:(${react table column})[2]      ISSUED
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM

Delete Serial Number
    Preparation
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]       ${serial number}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]       RFID
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]       ${distributor_name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]       ${customer_name} - ${shipto_name}
    ${buffer}                       Get Text    xpath:${modal dialog}${simple table}/tbody/tr/td[7]
    ${name}     ${email}            Split String    ${buffer}   \n
    Should Be Equal As Strings      ${dist user}    ${name}
    ${buffer}                       Get Text    xpath:${modal dialog}${simple table}/tbody/tr/td[8]
    ${name}     ${email}            Split String    ${buffer}   \n
    Should Be Equal As Strings      ${cust user}    ${name}
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
    Choose From Select Box          (${modal dialog}${select control})[2]       ${distributor_name}
    Click Element                   ${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${table xpath}/tbody/tr[${index}]/td[6]       ${distributor_name}

*** Keywords ***
Preparation
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/hardware"]
    Sleep                           7 second
    Open Full Table
    ${number of row}                Get Rows Count                  ${table xpath}
    ${number of new row}=           Evaluate                        ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${number of row}

Goto Settings Sub
    Finish Suite
    Start Distributor
    Go To                           https://distributor.${environment}.storeroomlogix.com/settings#hardware-integration
    Sleep                           3 second
    ${my serial number}             Get Row Number      1       ${serial number}
    Set Suite Variable              ${my serial number}