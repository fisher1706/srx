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
Base Fees
    [Tags]                          Base
    Click Element                   id:fees-tab-base-fees
    Click Element                   xpath:${table xpath}/tbody/tr/td[2]
    Input Text                      xpath:${table xpath}/tbody/tr/td[2]/div/div/*               5000
    Press Key                       xpath:${table xpath}/tbody/tr/td[2]/div/div/*               \ue004
    Press Key                       ${button success}                                           \ue007
    Sleep                           5 second
    Click Element                   ${button success}
    Reload Page
    Sleep                           3 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr/td[2]                         $5000
    Click Element                   xpath:${table xpath}/tbody/tr/td[2]
    Input Text                      xpath:${table xpath}/tbody/tr/td[2]/div/div/*               4320
    Press Key                       xpath:${table xpath}/tbody/tr/td[2]/div/div/*               \ue004
    Press Key                       ${button success}                                           \ue007
    Sleep                           5 second
    Click Element                   ${button success}
    Sleep                           5 second

Triggers Monthly Fees
    [Tags]                          Triggers
    Testing Fees Tab                fees-tab-triggers-monthly-fee       ${triggers monthly pane}

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


