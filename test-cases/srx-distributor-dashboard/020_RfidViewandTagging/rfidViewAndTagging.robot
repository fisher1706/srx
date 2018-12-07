*** Settings ***

Library                             Selenium2Library
Library                             String
Library                             Collections
Library                             RequestsLibrary
Library                             OperatingSystem
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot
Suite Setup                         Goto Locations
Suite Teardown                      Close All Browsers

*** Test Cases ***

Prepare to testing ohi
    [Tags]                          Preparation
    Click Element                   id=pageDropDown
    Sleep                           1 second
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div[1]/span/ul/li[4]/a
    Sleep                           3 seconds

Check Changes From Button to Standart and back
    [Tags]                          Check Changes
    Different locations creating    1
    Sleep                           3 seconds
    Change SKU in location          ${dynamic sku}1
    Delete new location
    Different locations creating    2
    Sleep                           3 seconds
    Change SkU in location          ${dynamic sku}1
    Delete new location

Create two locations with the same sku and type
    [Tags]                          Creating the same two locations
    :FOR    ${var}      IN RANGE            1   5
    \    Different locations creating       ${var}
    \    Creating second the same location  ${var}
    \    Sleep                              3 seconds
    \    Delete new location

Creating new location for RFID tests
    [Tags]                          New location Creating
    Click Link                      xpath://*[@href="/locations"]
    Sleep                           3 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/button
    Input Text                      id=orderingConfig-product-partSku_id                    ${dynamic sku}2
    Input Text                      id=orderingConfig-currentInventoryControls-min_id       ${minValue}
    Input Text                      id=orderingConfig-currentInventoryControls-max_id       ${maxValue}
    Input Text                      id=attributeName1_id                                    ${locationName}
    Input Text                      id=attributeValue1_id                                   ${locationValue}
    Click Element                   css:.Select-placeholder
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue007
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]
    Sleep                           2 seconds
    ${numbers}                      Get Element Count      xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr                                   
    Set Global Variable             ${numbers}

Check Selector Input at RFID page
    [Tags]                          New location Creating
    Click Link                      xpath://*[@href="/rfid-view"]
    Input Text                      xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/input         SomeFloodHere
    ${text rfid sku}                Get Text               xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div
    Should Be Equal As Strings      ${text rfid sku}       No results found
    Reload Page
    Input Text                      xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/input         ${dynamic sku}2
    ${text rfid sku}                Get Text               xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div
    Should Be Equal As Strings      ${text rfid sku}       ${dynamic sku}2
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div

Adding RFID with false Transaction
    [Tags]                          False Transaction
    Click Element                   css:.rfid-create-button
    Input Text                      xpath://*[@id="transactionNumber_id"]                   195
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[3]
    Wait Until Page Contains        This transaction number is not for RFID location type
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[1]
    Sleep                           2 seconds

Adding three Rfid View and tagging
    [Tags]                          Adding two Rfids
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[2]
    :FOR       ${var}      IN RANGE            1   4
    \    Click Element              css:.rfid-create-button
    \    ${buffer}=                 Generate Random String      18      [LETTERS]
    \    ${random string}=          Convert To Uppercase        ${buffer}
    \    Input Text                 id=labelId_id                                           ${random string}
    \    Input Text                 id=labelData_id                                         ${RfidAssociatedData}
    \    Click Element              xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]
    \    ${ohiCount}=               Evaluate                    ${ohiCount}+5
    \    Sleep                      2 seconds
    \    Element Text Should Be     xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div[4]/div[4]          OHI:${ohiCount}
    \    ${rfidCount}               Evaluate                ${rfidCount}+1
    Set Global Variable             ${ohiCount}
    Set Global Variable             ${rfidCount}

Prepare to sorting
    [Tags]                          Preparation
    Click Link                      xpath://*[@href="/rfid-view"]
    Sleep                           3 seconds
    Click Element                   id=pageDropDown
    Sleep                           1 second
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[2]/div/div[1]/span/ul/li[4]/a
    Sleep                           4 seconds
    ${Sortnumbers}                  Get Element Count       xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr
    Sleep                           2 seconds                                    
    Set Global Variable             ${Sortnumbers}

Check values from Location page
    [Tags]                          Checking values from Location page
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div[2]/div[4]        Min:${minValue}
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div[3]/div[4]        Max:${maxValue}
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div[2]/div[1]        Location Name 1:${locationName}
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div[3]/div[1]        Location Value 1:${locationValue}


Sorting
    [Tags]                          Rfid New and Tagging page Sorting
    Set Global Variable             ${count}                 1
    :FOR    ${var}                  IN                       @{RfidVandTsortingFields}
    \       Make sorting            ${var}                   ${count}
    \       ${count}=               Evaluate                 ${count}+1

Post Request 
    [Tags]                          Post Request
    ${RFIDnumberOne}                Get Text                 xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[1]
    ${RFIDnumberTwo}                Get Text                 xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[2]/td[1]
    Post Requests                   ${RFIDnumberOne}
    Post Requests                   ${RFIDnumberTwo}

Check Filtres
    [Tags]                          Filter check
    Sleep                           3 seconds
    ${RFIDname}                     Get Text                 xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[1]
    ${creationDate}                 Get Text                 xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[3]
    Field Selector Check Tr         xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]                        AVAILABLE
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/input               ${email}                   4
    Filter Check Date               xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div/div/div/input   ${creationDate}            3          FROM
    Filter Check Date               xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[4]/div[2]/div/div/div/input   ${creationDate}            3          TO
    Filter Check                    xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[5]/div[2]/input               ${RfidAssociatedData}      5


Check OHI at this location
    [Tags]                          Check OHI at all pages
    ${ohiCount}=                    Evaluate                 ${ohiCount}-10
    Click Link                      xpath://*[@href="/locations"]
    Sleep                           3 seconds
    ${ohiLocPageValue}              Get Text                 xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[17]
    Should Be Equal                 "${ohiLocPageValue}"     "${ohiCount}"
    Click Link                      xpath://*[@href="/rfid-view"]
    Sleep                           3 seconds
    Click Link                      xpath://*[@href="/rfid-view"]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[2]
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div[4]/div[4]          OHI:${ohiCount}
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[1]/table/thead/tr/th[2]
    Sleep                           2 seconds
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${rfidCount}]/td[2]                    ISSUED

Change type to button and back
    Click Link                      xpath://*[@href="/locations"]
    Sleep                           3 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[13]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[13]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[13]/div/div/div/div[2]/div/div[1]
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]
    Sleep                           3 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div/div/button
    Sleep                           3 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[13]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[13]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[13]/div/div/div/div[2]/div/div[3]
    Press Key                       xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[13]/div/div/div/div[1]/div[1]/div[2]         \ue004
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div/div/button
    Sleep                           2 seconds

Check at RFID View and Tagging page issued RFIDs
    Click Link                      xpath://*[@href="/rfid-view"]
    Sleep                           3 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[2]
    Sleep                           2 seconds
    ${issuedRFIDSnow}               Get Element Count      xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr/td[1]
    Should Be Equal                 ${IssuedRFIDS}         ${IssuedRFIDSnow}

Delete new location
    Click Link                      xpath://*[@href="/locations"]
    Sleep                           3 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[1]/input
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/button
    Sleep                           1 second
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/button[2]
    Sleep                           2 seconds
    ${numbers}=                     Evaluate                ${numbers}-1
    Set Global Variable             ${numbers}

Open Transaction page
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[1]/div/ul/li[6]/a
    Sleep                           3 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div/div/div[3]/div/div/div/div/div[1]/div[1]/table/thead/tr/th[1]
    Sleep                           4 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div/div/div[3]/div/div/div/div/div[1]/div[1]/table/thead/tr/th[1]
    Sleep                           4 seconds
    ${lastTransaction}              Get Text                xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[3]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[5]/div
    Should Be Equal As Strings      ${lastTransaction}      10

*** Keywords ***

Different locations creating
    [Arguments]                     ${locationType}
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/button
    Input Text                      id=orderingConfig-product-partSku_id                    ${dynamic sku}2
    Input Text                      id=orderingConfig-currentInventoryControls-min_id       ${minValue}
    Input Text                      id=orderingConfig-currentInventoryControls-max_id       ${maxValue}
    Input Text                      id=attributeName1_id                                    ${locationName}+${locationType}
    Input Text                      id=attributeValue1_id                                   ${locationValue}
    Click Element                   css:.Select-placeholder
    :FOR    ${var}     IN RANGE     0    ${locationType}
    \           Press Key           xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue007
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]
    Sleep                           2 seconds
    ${numbers}                      Get Element Count      xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr                                   
    Set Global Variable             ${numbers}
    Sleep                           2 seconds

Delete new location
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[1]/input
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/button
    Sleep                           1 second
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/button[2]
    Sleep                           2 seconds
    ${numbers}=                     Evaluate                ${numbers}-1
    Set Global Variable             ${numbers}

OHI Check not RFID
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[17]           -

OHI Check RFID
    Element Text Should Not Be      xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[17]           -

Creating second the same location
    [Arguments]                     ${locationType}
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/button
    Input Text                      id=orderingConfig-product-partSku_id                    ${dynamic sku}2
    Input Text                      id=orderingConfig-currentInventoryControls-min_id       ${minValue}
    Input Text                      id=orderingConfig-currentInventoryControls-max_id       ${maxValue}
    Input Text                      id=attributeName1_id                                    ${locationName}+${locationType}
    Input Text                      id=attributeValue1_id                                   ${locationValue}
    Click Element                   css:.Select-placeholder
    :FOR    ${var}     IN RANGE     0    ${locationType}
    \           Press Key           xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/div/div/div/div/div[2]           \ue007
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]
    Wait Until Page Contains        Operation failed!
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[1]/button/span[1]
    Sleep                           2 seconds

Make sorting
    [Arguments]                     ${field}                 ${rownum}
    Click Element                   ${field}
    Sleep                           3 seconds
    ${firstField}                   Get Text                 xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[${rownum}]
    Sleep                           2 seconds
    Click Element                   ${field}
    Sleep                           2 seconds
    ${lastField}                    Get Text                 xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${Sortnumbers}]/td[${rownum}]
    Should Be Equal                 ${firstField}            ${lastField}
    Sleep                           1 second
    Click Element                   ${field}
    Sleep                           2 seconds

Post Requests
    [Arguments]                     ${rfidNum}
    Create Session                  httpbin                  https://${apiKey}:${apiKey}@api-dev.storeroomlogix.com/api/webhook/events/rfid        verify=true
    &{headers}=                     Create Dictionary        Content-Type=application/json
    ${resp}=                        Post Request             httpbin    /issued        data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${rfidNum}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp.status_code}      200
    Sleep                           2 seconds
    ${IssuedRFIDS}                  Evaluate                 ${IssuedRFIDS}+1
    Set Global Variable             ${IssuedRFIDS}

Filter Check
    [Arguments]                     ${inputField}            ${inputText}     ${checkingField}
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[1]/div/button
    Input Text                      ${inputField}            ${inputText}
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/button[2]
    Sleep                           3 seconds
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[${checkingField}]            ${inputText}
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[1]/div/button[2]
    Sleep                           3 seconds

Field Selector Check Tr
    [Arguments]                     ${fieldAdr}             ${fieldType}
    Click Element                   css:.button-right-margin
    ${result} =                     Fetch From Left         ${fieldAdr}    2]/div/div/div/div/div[1]
    ${newString}=                   Strip String            ${result}1]/div
    ${fieldName}                    Get Text                ${newString}
    Go Down                         ${fieldAdr}             ${fieldType}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           3 seconds
    ${rowNum}                       Get Element Count       xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[1]/table/thead/tr/th
    ${rowNum}=                      Evaluate                ${rowNum}+1
     :FOR   ${var}                  IN RANGE            1   ${rowNum}
    \       ${textInfo}             Get Text                xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[1]/table/thead/tr/th[${var}]
    \       Run Keyword If          "${textInfo}" == "${fieldName}"      Field Comparing   ${var}        ${fieldType}
    Click Element                   css:button.button-right-margin:nth-child(2)
    Sleep                           2 seconds

Go Down
    [Arguments]                     ${fieldAdr}             ${field type}
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div[2]            \ue015
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div[2]            \ue007              
    ${text buffer sub}              Get Text                 xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div[1]
    Sleep                           1 second
    Run Keyword If                  "${text buffer sub}"!="${field type}"        Go Down    ${fieldAdr}    ${field type}

Field Comparing
    [Arguments]                     ${rowNum}               ${expectedValue}
    ${rowValue}                     Get Text                xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr/td[${rowNum}]
    Should Be Equal As Strings      ${rowValue}             ${expectedValue}

Change SKU in location
    [Arguments]                     ${locationSKUname}
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[11]
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[11]
    Input Text                      xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[11]/div/div/input      ${locationSKUname}
    Press Key                       xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[${numbers}]/td[11]/div/div/input      \ue004
    Sleep                           2 seconds
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div/div/button
    Sleep                           3 seconds

Filter Check Date
    [Arguments]                     ${inputField}            ${inputText}     ${checkingField}      ${fromTO}
    ${resultFrom} =                 Fetch From Left          ${inputText}      M
    ${leftPart} =                   Fetch From Left          ${resultFrom}     2018
    ${rightPart} =                  Fetch From Right         ${resultFrom}     2018
    ${resultTo} =                   Strip String             ${leftPart}2020${rightPart}
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[1]/div/button
    Run Keyword If                  "${fromTO}" == "TO"      Input Text        ${inputField}            ${resultTo}     ELSE        Input Text        ${inputField}            ${resultFrom}
    Sleep                           2 seconds
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/button[2]
    Sleep                           3 seconds
    Element Text Should Be          xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[${checkingField}]            ${inputText}
    Click Element                   xpath://*[@id="root"]/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[1]/div/button[2]
    Sleep                           3 seconds

*** Variables ****

${rfidCount}                        0
${ohiCount}                         0
${IssuedRFIDS}                      0
