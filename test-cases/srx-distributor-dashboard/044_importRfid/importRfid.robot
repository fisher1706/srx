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
    Go Down Selector                (${modal dialog}${select control})[2]                   CUSTOMER
    Click Element                   xpath:${button modal dialog ok}

Checking New Location
    Sleep                           7 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       CUSTOMER
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[4]/div       ${location name}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[5]/div       ${location value}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[12]/div      ${import rfid sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[14]/div      RFID
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[15]/div      0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[16]/div      30
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[17]/div      60
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[20]/div      OFF

Import RFID
    Goto Sidebar RFID
    Sleep                           5 second
    Select Location At Rfid Menu    Static Customer - 2048      ${import rfid sku}
    Sleep                           5 second
    ${epc1}                         Generate Random Name U
    ${epc2}                         Generate Random Name U
    Set Suite Variable              ${epc1}
    Set Suite Variable              ${epc2}
    Create File                     ${CURDIR}/../../../resources/importRfid.csv     RFID${\n}${epc1}${\n}${epc2}
    Sleep                           5 second
    Click Element                   xpath:${import rfid button}
    Sleep                           2 second
    Execute Javascript              document.getElementById("upload-rfid-csv").style.display='block'
    Sleep                           1 second
    Choose File                     id:upload-rfid-csv              ${CURDIR}/../../../resources/importRfid.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}            Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Checking RFID
    Select Location At Rfid Menu    Static Customer - 2048      ${import rfid sku}
    Sleep                           5 second
    Element Text Should Be          xpath:(${react table column})[1]      ${epc2}
    Element Text Should Be          xpath:(${react table column})[2]      ASSIGNED
    Element Text Should Be          xpath:(${react table column})[4]      SYSTEM
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[1]     ${epc1}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     ASSIGNED
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[4]     SYSTEM
    ${number of row}                Get Element Count   xpath:${react table raw}
    Should Be Equal As Integers     ${number of row}    2

Delete Location
    Goto Locations
    Sleep                           5 second
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${location name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     ${location value}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[11]    ${import rfid sku}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]    RFID
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    0
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]    30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[16]    60
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[19]    OFF
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           7 second
    ${number of new row}            Get Rows Count          ${table xpath}
    Should Be Equal As Integers     ${number of new row}    ${number of row}

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Locations
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}