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
    Choose From Select Box          (${modal dialog}${select control})[1]               DeepLens
    Click Element                   xpath:(${select control})[2]
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]          \ue015
    Press Key                       xpath:(${select control})[2]/div[1]/div[2]          \ue007
    ${device}                       Get Text        xpath:(${select control})[2]/div[1]/div[1]/span
    Set Suite Variable              ${device}
    Input Text                      xpath:${modal dialog}${form control}           12/12/2021, 12:00 A
    Click Element                   xpath:${button modal dialog ok}

Checking New Serial Number
    Sleep                           5 second
    ${serial number}                Get Text        xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]
    Set Suite Variable              ${serial number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]       DEEPLENS
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]       ${device}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[10]       12/12/2021, 12:00 AM

Edit Serial Number
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]${button success}
    Choose From Select Box          (${modal dialog}${select control})[2]           Srx-group-test-distributor
    Clear Element Text              xpath:${modal dialog}${form control}
    Input Text                      xpath:${modal dialog}${form control}            10/10/2022, 11:00 P
    Click Element                   xpath:${button modal dialog ok}

Checking Edit Serial Number
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]       ${serial number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]       DEEPLENS
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]       ${device}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[6]       Srx-group-test-distributor
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[10]       10/10/2022, 11:00 PM

Checking Serial Number On Distributor Portal
    Goto Settings Sub
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[1]       ${serial number}
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[2]       DEEPLENS
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[10]       10/10/2022, 11:00 PM

Change Serial Number On Distributor Portal
    Click Element                   xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]${button success}
    Input Text                      id:deviceName_id                    MyDeviceDeepLens
    Choose From Select Box          (${modal dialog}${select control})[1]   Static Customer - 2048
    Sleep                           5 second
    Click Element                   xpath:(${modal dialog}${select control})[2]
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${modal dialog}${select control})[2]/div[1]/div[2]        \ue007
    ${dist user}                    Get Text    xpath:(${modal dialog}${select control})[2]/div/div/span
    Click Element                   xpath:(${modal dialog}${select control})[3]
    Press Key                       xpath:(${modal dialog}${select control})[3]/div[1]/div[2]        \ue015
    Press Key                       xpath:(${modal dialog}${select control})[3]/div[1]/div[2]        \ue007
    ${cust user}                    Get Text    xpath:(${modal dialog}${select control})[3]/div/div/span
    Click Element                   xpath:${button modal dialog ok}
    Set Suite Variable              ${dist user}
    Set Suite Variable              ${cust user}
    Sleep                           5 second

Checking Serial Number On Distributor Portal After Change
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[1]       ${serial number}
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[2]       DEEPLENS
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[3]       MyDeviceDeepLens
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[5]       Static Customer - 2048
    ${buffer}                       Get Text    xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[7]
    ${name}     ${email}            Split String    ${buffer}   \n
    Should Be Equal As Strings      ${dist user}    ${name}
    ${buffer}                       Get Text    xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[9]
    ${name}     ${email}            Split String    ${buffer}   \n
    Should Be Equal As Strings      ${cust user}    ${name}
    Element Text Should Be          xpath:${claiming hardware pane}${table xpath}/tbody/tr[${my serial number}]/td[10]      10/10/2022, 11:00 PM
    Finish Suite
    Sleep                           5 second

Delete Serial Number
    Preparation
    ${start rows}                   Evaluate        ${number of row}-1
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]       ${serial number}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]       DEEPLENS
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]       ${device}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]       MyDeviceDeepLens
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]       Srx-group-test-distributor
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]       Static Customer - 2048
    ${buffer}                       Get Text    xpath:${modal dialog}${simple table}/tbody/tr/td[7]
    ${name}     ${email}            Split String    ${buffer}   \n
    Should Be Equal As Strings      ${dist user}    ${name}
    ${buffer}                       Get Text    xpath:${modal dialog}${simple table}/tbody/tr/td[8]
    ${name}     ${email}            Split String    ${buffer}   \n
    Should Be Equal As Strings      ${cust user}    ${name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[9]       10/10/2022, 11:00 PM
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second
    ${finish rows}                  Get Rows Count                  ${table xpath}
    Should Be Equal As Integers     ${finish rows}                  ${start rows}

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
