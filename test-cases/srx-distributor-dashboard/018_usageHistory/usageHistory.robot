*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Checking New Item
    [Tags]                          Check new Record
    Click Element                   css:.button-right-margin
    Input Text                      xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/input       ${order number}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]/div         ${order number}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[9]/div         Delivered
    Click Element                   css:button.button-right-margin:nth-child(2)
    Sleep                           3 second

Sorting Usage History
    [Tags]                          Sorting
    Sorting Usage History           2
    Sorting Usage History           5
    Sorting Usage History           6
    Sorting Usage History           7
    Sorting Usage History           8
    Sorting Usage History           9

Usage History Filtration
    [Tags]                          Filtration
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/input         101
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/input         59
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/input         PAND F1X4LG6
    Filter Check First Fields       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[4]/div[2]/input         12

*** Keywords ***
Preparation
    Goto Transactions
    Click Element                   xpath:${header xpath}/thead/tr/th[8]/div[1]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]/div[1]
    ${order number}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[1]/div
    Set Global Variable             ${order number}
    Click Element                   xpath:${table xpath}/tbody/tr[1]/td[12]/div/div/button
    Go Down                         DELIVERED
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           3 second
    Click Link                      xpath://*[@href="/usage-history"]
    Section Is Present              css:div.btn
    Sleep                           1 second
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    Number Of Rows
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Global Variable             ${number of new row}

Go Down
    [Arguments]                     ${field type}
    Click Element                   xpath:${modal dialog}${select control}
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${modal dialog}${select control}/div[1]/div[2]            \ue007              
    ${text buffer sub}              Get Text                 xpath:${modal dialog}${select control}/div[1]/div[1]
    Sleep                           1 second
    Run Keyword If                  "${text buffer sub}"!="${field type}"        Go Down    ${field type}

Sorting Usage History
    [Arguments]                     ${column}
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer1up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    ${text buffer1down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer2up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    ${text buffer2down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
