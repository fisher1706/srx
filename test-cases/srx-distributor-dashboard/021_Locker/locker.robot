*** Settings ***

Library                             Selenium2Library
Library                             Collections
Library                             RequestsLibrary
Library                             OperatingSystem
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot
Suite Setup                         Goto Locations
Suite Teardown                      Close All Browsers

*** Test Cases ***
Create Locker
    [Tags]                          Locker creating
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/button
    Input Text                      id=orderingConfig-product-partSku_id                    ${dynamic sku}1
    Input Text                      id=orderingConfig-currentInventoryControls-min_id       ${minValue}
    Input Text                      id=orderingConfig-currentInventoryControls-max_id       ${maxValue}
    Input Text                      id=attributeName1_id                                    ${locationName}
    Input Text                      id=attributeValue1_id                                   ${locationValue}
    Click Element                   css:.Select-placeholder
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue007
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]
    Sleep                           2 seconds
    ${numbers}                      Get Element Count      xpath:${table xpath}/tbody/tr                                   
    Set Global Variable             ${numbers}
    Check Locker values             0                      ${dynamic sku}1

Change to another type
    [Tags]                          Checking modal window when changing 
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[13]
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[13]
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[13]/div/div/div/div[2]/div/div[1]
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]
    Sleep                           3 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div/div/button
    Sleep                           3 seconds
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[13]
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[13]
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[13]/div/div/div/div[2]/div/div[4]
    Press Key                       xpath:${table xpath}/tbody/tr[${numbers}]/td[13]/div/div/div/div[1]/div[1]/div[2]         \ue004
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div/div/button
    Sleep                           5 seconds
    Check Locker values             0                       ${dynamic sku}1

Locker Post Requests before Location Changes
    [Tags]                          Post Request
    ${ohiSum}                       Locker Request          10                      Available
    Check Locker values             10                      ${dynamic sku}1
    Locker Request                  5                       Issued
    Check Locker values             ${OHI val}              ${dynamic sku}1
    Open Transaction page           5

Change location SKU
    [Tags]                          SKU changes
    Change SKU in location          SKU_VALUE1
    ${OHI val}=                     Set Variable            0
    Set Global Variable             ${OHI val}
    Check Locker values             ${OHI val}              SKU_VALUE1
    Change SKU in location          ${dynamic sku}1
    Check Locker values             ${OHI val}             ${dynamic sku}1

Locker Post Requests after Location Changes
    Locker Request                  15                      Available
    Check Locker values             ${OHI val}              ${dynamic sku}1
    Locker Request                  10                      Issued
    Check Locker values             ${OHI val}              ${dynamic sku}1
    Open Transaction page           15

Returned Locker Requests
    Locker Request                  35                      Available
    Check Locker values             ${OHI val}              ${dynamic sku}1
    Locker Request                  35                      Returned
    Locker Request                  10                      Issued
    Check Locker values             ${OHI val}              ${dynamic sku}1
    Open Transaction page           25

Not Multiply Locker Requests 
    Locker Request Not Multiply     7                       Available
    Check Locker values             ${OHI val}              ${dynamic sku}1
    Locker Request Not Multiply     17                      Issued
    Check Locker values             ${OHI val}              ${dynamic sku}1
    Open Transaction page           25

Less Then Now Locker Request 
    Locker Request Not Multiply     100                      Issued
    Check Locker values             0                        ${dynamic sku}1
    Open Transaction page           125

When OHI Zero Locker Request
    Locker Request Not Multiply     100                      Issued
    Check Locker values             0                        ${dynamic sku}1
    Open Transaction page           225


Delete new location
    [Tags]                          Location deleting
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[1]/input
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/button
    Sleep                           1 second
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/button[2]
    Sleep                           2 seconds
    ${numbers}=                     Evaluate                ${numbers}-1
    Set Global Variable             ${numbers}

*** Keywords ***

Check Locker values
    [Tags]                          Checking of creation or changes
    [Arguments]                     ${expectedOHI}            ${expectedSKU}
    ${currentOHI}                   Get Text                  xpath:${table xpath}/tbody/tr[${numbers}]/td[17]
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${numbers}]/td[11]           ${expectedSKU}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${numbers}]/td[13]           LOCKER
    Should Be Equal As Strings      ${expectedOHI}            ${currentOHI}

Change SKU in location
    [Arguments]                     ${locationSKUname}
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[11]
    Click Element                   xpath:${table xpath}/tbody/tr[${numbers}]/td[11]
    Input Text                      xpath:${table xpath}/tbody/tr[${numbers}]/td[11]/div/div/input      ${locationSKUname}
    Press Key                       xpath:${table xpath}/tbody/tr[${numbers}]/td[11]/div/div/input      \ue004
    Sleep                           3 seconds
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]
    Sleep                           2 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div/div/button
    Sleep                           3 seconds

Locker Request
    [Arguments]                     ${OHIcounting}           ${stateType}
    Create Session                  httpbin                  https://${APIKEY}:${APIKEY}@api-dev.storeroomlogix.com/api/webhook/events/locker        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /        data={ "currentWeight": 0, "distributorSku": "${dynamic sku}1", "kioskId": 59, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": ${OHIcounting}, "quantityRequested": 10, "timestamp": "2018-10-30T11:22:48.806", "transactionStatus": "${stateType}", "weightOfProduct": 0 }    headers=${headers}
    Should Be Equal As Strings      ${resp.status_code}      200
    Reload Page
    Sleep                           2 seconds
    Run Keyword If                  '${stateType}' == 'Issued'      Decreasing OHI  ${OHIcounting}  ELSE     Increasing OHI  ${OHIcounting}

Locker Request Not Multiply
    [Arguments]                     ${OHIcounting}           ${stateType}
    Create Session                  httpbin                  https://${APIKEY}:${APIKEY}@api-dev.storeroomlogix.com/api/webhook/events/locker        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /        data={ "currentWeight": 0, "distributorSku": "${dynamic sku}1", "kioskId": 59, "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": ${OHIcounting}, "quantityRequested": 10, "timestamp": "2018-10-30T11:22:48.806", "transactionStatus": "${stateType}", "weightOfProduct": 0 }    headers=${headers}
    Should Be Equal As Strings      ${resp.status_code}      200
    Reload Page
    Sleep                           2 seconds

Open Transaction page
    [Arguments]                     ${expectedTransaction}
    Click Link                      xpath://*[@href="/transactions"]
    Sleep                           3 seconds
    Click Element                   xpath:${header xpath}/thead/tr/th[1]
    Sleep                           4 seconds
    Click Element                   xpath:${header xpath}/thead/tr/th[1]
    Sleep                           4 seconds
    ${lastTransaction}              Get Text                xpath:${table xpath}/tbody/tr[1]/td[5]/div
    Should Be Equal As Strings      ${lastTransaction}      ${expectedTransaction}
    Click Link                      xpath://*[@href="/locations"]

Increasing OHI
    [Arguments]                     ${inc val}
    ${OHI val}=                     Evaluate        ${OHI val}+${inc val}
    Set Global Variable             ${OHI val}

Decreasing OHI
    [Arguments]                     ${decr val}
    ${OHI val}=                     Evaluate        ${OHI val}-${decr val}
    Set Global Variable             ${OHI val}

*** Variables ***
${OHI val}                          0