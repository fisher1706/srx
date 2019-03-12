*** Settings ***
Test Setup                          Preparation
Test Teardown                       Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***
${amount}                           100000-150000
${value}                            200000
${edit amount}                      150001-200000
${edit value}                       300000

*** Test Cases ***
Button Monthly Fees
    [Tags]                          Button
    Testing Fees Tab                fees-tab-button-monthly-fee     ${button monthly pane}

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
    Input Text                      xpath:(${modal dialog}${form control})[1]       ${amount}
    Input Text                      xpath:(${modal dialog}${form control})[2]       ${value}
    Click Element                   xpath:${modal dialog}${button modal dialog ok}
    Sleep                           1 second
    Element Text Should Be          xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[1]       ${amount}
    Element Text Should Be          xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[2]       $${value}
    Click Element                   xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[1]
    Input Text                      xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[1]//input    ${edit amount}
    Press Key                       xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[1]//input    \ue007
    Click Element                   xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[2]
    Input Text                      xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[2]//input    ${edit value}
    Press Key                       xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[2]//input    \ue007
    Click Element                   xpath:${pane}${button lg}
    Sleep                           5 second
    Reload Page
    Sleep                           5 second
    Click Element                   id:${tab}
    Click Element                   xpath:${pane}${table xpath}/tbody/tr[${new rows count}]/td[3]${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]                  ${edit amount}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]                  $${edit value}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

    ${new rows count}               Get Rows Count                  ${pane}${table xpath}
    Should Be Equal As Integers     ${rows count}                   ${new rows count}


