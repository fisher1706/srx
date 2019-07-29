*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

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
    Sleep                           10 second
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  $${edit year fee}

Checking Base Fees
    Goto Settings Sub
    Page Should Contain             ${edit year fee}
    Finish Suite
    Sleep                           5 second

Return Base Fees
    Preparation
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${button lg}
    Sleep                           10 second
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  $${year fee}

Checking Returned Base Fees
    Goto Settings Sub
    Page Should Contain             ${year fee}

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
    Go To                           https://distributor.${environment}.storeroomlogix.com/settings#pricing-billing
    Sleep                           2 second