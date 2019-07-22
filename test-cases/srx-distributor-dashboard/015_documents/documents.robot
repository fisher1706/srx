*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Check Document Status In Settings
    Click Element                   (${tab element})[5]
    ${status}                       Get Text        xpath:(((${react table})[1]${react table raw})[1]${react table column})[4]
    Set Suite Variable              ${status}

Checking Taxes Before Change
    Click On Card                   Taxes
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
    \   Run Keyword If              "${text buffer}"=="${distributor_name}"   Exit For Loop
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${colomn}]/td[5]/div/span    ${status}

Change Document Status
    Run Keyword If                  "${status}"=="APPROVED"     Approved    ELSE IF     "${status}"=="REJECTED"     Rejected
    Sleep                           10 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${colomn}]/td[5]/div/span    ${restatus}
    Finish Suite
    Sleep                           5 second

Second Check Document Status In Settings
    Preparation
    Click Element                   (${tab element})[5]
    Element Text Should Be          xpath:(((${react table})[1]${react table raw})[1]${react table column})[4]      ${restatus}

Checking Taxes After Change
    Click On Card                   Taxes
    Run Keyword If                  "${restatus}"=="APPROVED"     Approved In Taxes    ELSE IF     "${restatus}"=="REJECTED"     Rejected In Taxes

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Settings
    Sleep                           3 second

Rejected In Taxes
    Element Text Should Be          xpath:(((${react table})[2]${react table raw})[1]${react table column})[1]    4.75 %
    Element Text Should Be          xpath:(((${react table})[2]${react table raw})[1]${react table column})[2]    NO

Approved In Taxes
    Element Text Should Be          xpath:(((${react table})[2]${react table raw})[1]${react table column})[1]    0 %
    Element Text Should Be          xpath:(((${react table})[2]${react table raw})[1]${react table column})[2]    YES

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