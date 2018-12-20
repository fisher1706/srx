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
    ${temp text2}                   Get Text        xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${edit year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div/div/input        ${edit month fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div/div/input        \ue007
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  ${temp text1}
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div                  ${temp text2}
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${edit year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div/div/input        ${edit month fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${button lg}
    Sleep                           5 second
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  $${edit year fee}
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div                  $${edit month fee}

Checking Base Fees
    Goto Settings Sub
    Element Text Should Be          xpath:${current fee panel 1}/div[2]/div[1]/div[2]      $${edit year fee}
    Element Text Should Be          xpath:${current fee panel 1}/div[2]/div[2]/div[2]      $${edit month fee} per warehouse
    Finish Suite
    Sleep                           5 second

Return Base Fees
    Preparation
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div/div/input        ${month fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div/div/input        \ue007
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  $${edit year fee}
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div                  $${edit month fee}
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        ${year fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]
    Input Text                      xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div/div/input        ${month fee}
    Press Key                       xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div/div/input        \ue007
    Click Element                   xpath:${base fee pane}${button lg}
    Sleep                           5 second
    Reload Page
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[1]/td[2]/div                  $${year fee}
    Element Text Should Be          xpath:${base fee pane}${table xpath}/tbody/tr[2]/td[2]/div                  $${month fee}

Checking Returned Base Fees
    Goto Settings Sub
    Element Text Should Be          xpath:${current fee panel 1}/div[2]/div[1]/div[2]       $${year fee}
    Element Text Should Be          xpath:${current fee panel 1}/div[2]/div[2]/div[2]       $${month fee} per warehouse

*** Keywords ***
Preparation
    Goto Fees
    ${SUB HOST}                     Return Sub Link
    Set Global Variable             ${SUB HOST}
    ${SUB EMAIL}                    Return Sub Email
    Set Global Variable             ${SUB EMAIL}

Goto Settings Sub
    Finish Suite
    Run Keyword If                  "${browser}"=="xvfb"            Run Xvfb Sub    ELSE IF     "${browser}"=="chrome"      Run Chrome Sub      ELSE    Run Ff Sub
    Set Selenium Implicit Wait                                      20 second
    Set Selenium Timeout                                            10 second
    Enter Correct Email Sub
    Enter Password
    Correct Submit Login
    Sleep                           7 second
    Click Link                      xpath://*[@href="/settings"]
    Sleep                           2 second
    Click Element                   id:settings-tab-pricing-billing
    Sleep                           1 second
    Click Element                   id:pricing-billing-tab-pricing-calc
    Sleep                           3 second



