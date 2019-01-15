*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             OperatingSystem
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${import rfid sku}                  IMPORT RFID SKU
${location value}                   location value 1
${location name}                    location name 1

*** Test Cases ***
Valid Create New Location
    Click Element                   xpath:${button primary}
    Input Text                      id:orderingConfig-product-partSku_id                    ${import rfid sku}
    Go Down Selector                (${modal dialog}${select control})[1]                   RFID
    Input Text                      id:orderingConfig-currentInventoryControls-min_id       30
    Input Text                      id:orderingConfig-currentInventoryControls-max_id       60
    Input Text                      id:attributeName1_id                                    ${location name}
    Input Text                      id:attributeValue1_id                                   ${location value}
    Click Element                   xpath:${button modal dialog ok}

Checking New Location
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${location name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       ${location value}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[11]/div      ${import rfid sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[12]/div      1138
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[13]/div      RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[18]/div      OFF

Import RFID
    Click Link                      xpath://*[@href="/rfid-view"]
    Sleep                           3 second
    Input Text                      xpath:(${select control})[2]/div/div/input       ${import rfid sku}
    Press Key                       xpath:(${select control})[2]/div/div/input       \ue007
    Sleep                           1 second
    ${buffer1}                      Generate Random String      18      [LETTERS]
    ${epc1}                         Convert To Uppercase        ${buffer1}
    ${buffer2}                      Generate Random String      18      [LETTERS]
    ${epc2}                         Convert To Uppercase        ${buffer2}
    Set Suite Variable              ${epc1}
    Set Suite Variable              ${epc2}
    Create File                     ${CURDIR}/../../../resources/importRfid.csv     RFID${\n}${epc1}${\n}${epc2}
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                  ${CURDIR}/../../../resources/importRfid.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}            Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Checking RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[1]          ${epc1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]          ASSIGNED
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[4]          SYSTEM
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[1]          ${epc2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[2]          ASSIGNED
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[4]          SYSTEM
    ${number of row}                Get Rows Count                                  ${table xpath}
    Should Be Equal As Integers     ${number of row}                                2

Delete Location
    Click Link                      xpath://*[@href="/locations"]
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ${location name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${location value}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]    ${import rfid sku}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[12]    RFID
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]    30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    60
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[16]    20
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[17]    OFF
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           3 second
    ${number of new row}            Get Rows Count          ${table xpath}
    Should Be Equal As Integers     ${number of new row}    ${number of row}

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Click Link                      xpath://*[@href="/locations"]
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}