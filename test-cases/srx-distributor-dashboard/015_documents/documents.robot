*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Check Document Status In Settings
    Goto Documents
    ${status}                       Get Text        xpath:${documents pane}${table xpath}/tbody/tr/td[4]/div/span
    Set Suite Variable              ${status}

Checking Taxes Before Change
    Goto Taxes
    Run Keyword If                  "${status}"=="APPROVED"     Approved In Taxes    ELSE IF     "${status}"=="REJECTED"     Rejected In Taxes

Check Document Status In Documents
    Goto Documents Sub
    Sleep                           2 second
    Click Element                   css:#pageDropDown
    Sleep                           1 second
    Click Element                   css:li.dropdown-item:nth-child(4) > a:nth-child(1)
    Sleep                           5 second
    Number Of Rows
    :FOR    ${colomn}               IN RANGE        1       ${number of row}+1
    \   Set Suite Variable          ${colomn}
    \   ${text buffer}              Get Text    xpath:${table xpath}/tbody/tr[${colomn}]/td[1]/div
    \   Run Keyword If              "${text buffer}"=="Srx-group-test-distributor"   Exit For Loop
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${colomn}]/td[5]/div/span    ${status}

Change Document Status
    Run Keyword If                  "${status}"=="APPROVED"     Approved    ELSE IF     "${status}"=="REJECTED"     Rejected
    Sleep                           10 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${colomn}]/td[5]/div/span    ${restatus}
    Finish Suite
    Sleep                           5 second

Second Check Document Status In Settings
    Preparation
    Goto Documents
    Element Text Should Be          xpath:${documents pane}${table xpath}/tbody/tr/td[4]/div/span     ${restatus}

Checking Taxes After Change
    Goto Taxes
    Run Keyword If                  "${restatus}"=="APPROVED"     Approved In Taxes    ELSE IF     "${restatus}"=="REJECTED"     Rejected In Taxes

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Settings
    Sleep                           3 second

Goto Documents
    Click Element                   id:settings-tab-pricing-billing
    Sleep                           1 second
    Click Element                   id:pricing-billing-tab-documents
    Sleep                           3 second

Goto Taxes
    Click Element                   id:settings-tab-pricing-billing
    Sleep                           1 second
    Click Element                   id:pricing-billing-tab-taxes
    Sleep                           3 second

Rejected In Taxes
    Element Text Should Be          xpath:${taxes pane}${table xpath}/tbody/tr/td[1]/div     4.75 %
    Element Text Should Be          xpath:${taxes pane}${table xpath}/tbody/tr/td[2]/div     No

Approved In Taxes
    Element Text Should Be          xpath:${taxes pane}${table xpath}/tbody/tr/td[1]/div     0 %
    Element Text Should Be          xpath:${taxes pane}${table xpath}/tbody/tr/td[2]/div     Yes

Approved
    Click Element                   xpath:${table xpath}/tbody/tr[${colomn}]${button danger}
    Set Suite Variable              ${restatus}                 REJECTED

Rejected
    Click Element                   xpath:${table xpath}/tbody/tr[${colomn}]${button success}
    Set Suite Variable              ${restatus}                 APPROVED

Goto Documents Sub
    Finish Suite
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/documents"]
    Sleep                           3 second