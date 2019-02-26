*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${current fee panel 1}              //div[contains(@id,'current-fee-panel-1')]

*** Test Cases ***
Change Base Fees
    ${temp text1}                   Get Text        xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${edit year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  ${temp text1}
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${edit year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${button lg}
    Sleep                           20 second
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  $${edit year fee}

Checking Base Fees
    Goto Settings Sub
    Element Text Should Be          xpath:${current fee panel 1}/div[2]/div[1]/div[2]      $${edit year fee}
    Finish Suite
    Sleep                           5 second

Return Base Fees
    Preparation
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  $${edit year fee}
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${button lg}
    Sleep                           20 second
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  $${year fee}

Checking Returned Base Fees
    Goto Settings Sub
    Element Text Should Be          xpath:${current fee panel 1}/div[2]/div[1]/div[2]       $${year fee}

*** Keywords ***
Preparation
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/fees"]
    Sleep                           4 second

Goto Settings Sub
    Finish Suite
    Start Distributor
    Sleep                           5 second
    Goto Sidebar Settings
    Sleep                           2 second
    Click Element                   id:settings-tab-pricing-billing
    Sleep                           1 second
    Click Element                   id:pricing-billing-tab-pricing-calc
    Sleep                           3 second