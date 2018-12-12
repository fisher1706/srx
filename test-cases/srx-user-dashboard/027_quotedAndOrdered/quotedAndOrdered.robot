*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${index}                            1

*** Test Cases ***
Checking Quoted And Ordered List
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[2]/a
    Click Element                   xpath:${header xpath}/thead/tr/th[5]
    Click Element                   xpath:${header xpath}/thead/tr/th[5]
    Click Element                   xpath:${table xpath}/tbody/tr[1]/td[8]/button
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[1]/a
    Click Element                   css:.control-button
    Sleep                           5 second

Sorting List
    [Tags]                          Sorting
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[2]/a
    Click Element                   xpath:${header xpath}/thead/tr/th[5]
    Sorting List                    1
    Sorting List                    2
    Sorting List                    3
    Sorting List                    4
    Sorting List                    5
    Sorting List                    6

Filter List
    [Tags]                          Filter
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[2]/a
    Click Element                   css:.button-right-margin
    Input Text                      css:div.row-spaced:nth-child(1) > div:nth-child(2) > input:nth-child(1)     STATIC SKU
    Input Text                      css:div.row-spaced:nth-child(2) > div:nth-child(2) > input:nth-child(1)     10
    Click Element                   xpath:${select control}
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue013
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue007
    Click Element                   css:button.btn:nth-child(2)
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[1]/div     STATIC SKU
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]/div     10
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[5]/div     QUOTED

*** Keywords ***
Preparation
    Login In Customer Portal
    Click Element                   xpath:/html/body/div/div/div/div/div/div/button[1]
    Click Element                   css:.select-shipto-button
    Is Customer Portal

Sorting List
    [Arguments]                     ${column}
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    Sleep                           1 second
    ${text buffer1up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    Number Of Rows
    ${text buffer1down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    Sleep                           1 second
    ${text buffer2up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    ${text buffer2down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    Sleep                           1 second