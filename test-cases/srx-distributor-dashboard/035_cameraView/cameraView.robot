*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             String
Library                             SeleniumLibrary
Library                             DateTime
Library                             RequestsLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Case ***
Checking Date Of Last Screen
    [Tags]                          Test
    ${date}     ${full time}        Split String        ${full date string}        ,
    ${time}     ${AM PM}            Split String        ${full time}
    ${hours}    ${minutes}          Split String        ${time}                    :
    ${full date without AM PM}      Get Substring       ${full date string}        0    -3
    ${formatted full date}          Convert Date        ${full date without AM PM}     date_format=%m/%d/%Y, %H:%M
    Set Global Variable             ${hours}
    Set Global Variable             ${full date without AM PM}
    Set Global Variable             ${formatted full date}
    Run Keyword If                  "${AM PM}"=="PM"    If PM
    Run Keyword If                  "${AM PM}"=="AM"    If AM

Create Request
    ${buffer time}                  Subtract Time From Date     ${correct time and date}      01:59:00
    ${date}     ${time}             Split String                ${buffer time}
    Create Session                  httpbin                     https://${APIKEY}:${APIKEY}@api-dev.storeroomlogix.com/api/webhook/events/locker        verify=true
    &{headers}=                     Create Dictionary           Content-Type=application/json
    ${error}=                       Post Request                httpbin    /        data={ "currentWeight": 100, "distributorSku": "AB 1492-J3", "kioskId": 59, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 1313, "quantityIssued": 10, "quantityRequested": 10, "timestamp": "${date}T${time}", "transactionStatus": "Issued", "weightOfProduct": 10 }    headers=${headers}
    Should Be Equal As Strings      ${error}                    <Response [200]>

Checking New Item
    Reload Page
    Sleep                           5 second
    Set Suite Variable              ${search counter}       1
    Set Global Variable             ${ok}       false
    :FOR  ${search counter}         IN RANGE    1           100
    \   Set Global Variable         ${search index}         1
    \   Search Loop
    \   Exit For Loop If            "${ok}"=="true"
    \   Click Element               css:li.page-item:nth-child(6) > a:nth-child(1)
    \   Sleep                       1 second

Sorting Camera View
    [Tags]                          Sorting
    Sorting Camera View Column      2

*** Keywords ***
Preparation
    Goto Camera View
    Set Suite Variable              ${checing counter}   1
    Set Global Variable             ${ok}       false
    :FOR  ${checing counter}        IN RANGE    1        100
    \   Set Global Variable         ${checking index}    1
    \   Checking Loop
    \   Exit For Loop If            "${ok}"=="true"
    \   Click Element               css:li.page-item:nth-child(6) > a:nth-child(1)
    \   Sleep                       1 second

If PM
    Set Global Variable             ${correct time and date}    ${formatted full date}
    Run Keyword If                  ${hours}!=12                If Not Twelve

If Not Twelve
    ${correct time and date}        Add Time To Date            ${formatted full date}      12:00:00
    Set Global Variable             ${correct time and date}

If AM
    Set Global Variable             ${correct time and date}    ${formatted full date}
    Run Keyword If                  ${hours}==12                If Twelve

If Twelve
    ${correct time and date}        Subtract Time From Date     ${formatted full date}      12:00:00
    Set Global Variable             ${correct time and date}

Check Date
    ${full date string}             Get Text                    xpath:${table xpath}/tbody/tr[${checking index}]/td[2]/div
    Set Global Variable             ${full date string}
    Set Global Variable             ${ok}                       true

Check By Date
    ${locker}                       Get Text        xpath:${table xpath}/tbody/tr[${checking index}]/td[4]/div
    ${sku}                          Get Text        xpath:${table xpath}/tbody/tr[${checking index}]/td[5]/div
    Should Be Equal As Strings      ${locker}       1313
    Should Be Equal As Strings      ${sku}          AB 1492-J3
    Set Global Variable             ${ok}           true

Checking Loop
    :FOR  ${checking index}  IN RANGE        1           11
    \   Set Global Variable         ${checking index}
    \   ${rfid}                     Get Text        xpath:${table xpath}/tbody/tr[${checking index}]/td[3]/div
    \   ${locker}                   Get Text        xpath:${table xpath}/tbody/tr[${checking index}]/td[4]/div
    \   ${sku}                      Get Text        xpath:${table xpath}/tbody/tr[${checking index}]/td[5]/div
    \   Run Keyword If              "${rfid}"=="" and "${locker}"=="" and "${sku}"==""      Check Date
    \   Exit For Loop If            "${ok}"=="true"

Search Loop
    :FOR  ${search index}  IN RANGE        1           11
    \   Set Global Variable         ${search index}
    \   ${search date}              Get Text        xpath:${table xpath}/tbody/tr[${search index}]/td[2]/div
    \   Run Keyword If              "${search date}"=="${full date string}"     Check By Date
    \   Exit For Loop If            "${ok}"=="true"

Sorting Camera View Column
    [Arguments]                     ${column}
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer1up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    Number Of Rows
    ${text buffer1down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer2up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    ${text buffer2down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]