*** Settings ***
Test Setup                          Preparation
Test Teardown                       Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***
${customer shiptos}                 100000-150000
${edit customer shiptos}            150001-200000
${monthly fee}                      19
${edit monthly fee}                 27
${number of buttons}                100000-150000
${monthly fee per button}           3

*** Test Cases ***
Button Monthly Fees
    [Tags]                          Button
    Testing Fees Tab                fees-tab-button-monthly-fee     ${button monthly pane}

Shipto Monthly Fees
    [Tags]                          Shipto
    Testing Fees Tab                fees-tab-shipto-monthly-fee     ${shipto monthly pane}

Label Monthly Fees
    [Tags]                          Label
    Testing Fees Tab                fees-tab-label-monthly-fee      ${label monthly pane}

Rfid Monthly Fees
    [Tags]                          Rfid
    Testing Fees Tab                fees-tab-rfid-monthly-fee       ${rfid monthly pane}

Deeplens Monthly Fees
    [Tags]                          Deeplens
    Testing Fees Tab                fees-tab-deeplens-monthly-fee   ${deeplens monthly pane}

*** Keywords ***
Preparation
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/fees"]

Testing Fees Tab
    [Arguments]                     ${tab}      ${pane}
    Click Element                   id:${tab}
    Sleep                           1 second
    ${rows count}                   Get Rows Count      ${pane}${table xpath}
    ${new rows count}               Evaluate    ${rows count}+1
    Click Element                   xpath:${pane}${button primary}
    Input Text                      xpath:(${modal dialog}${form control})[1]       100000-150000
    Input Text                      xpath:(${modal dialog}${form control})[2]       200000
    Click Element                   xpath:${modal dialog}${button modal dialog ok}
    Sleep                           1 second
    Element Text Should Be          xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[1]       100000-150000
    Element Text Should Be          xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[2]       $200000
    Click Element                   xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[3]/div/div/button
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]                  100000-150000
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]                  $200000
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second
    ${new rows count}               Get Rows Count      ${pane}${table xpath}
    Should Be Equal As Integers     ${rows count}       ${new rows count}



