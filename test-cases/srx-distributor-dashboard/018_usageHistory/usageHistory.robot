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
    Sort Column With Last Page      2
    Sort Column With Last Page      5
    Sort Column With Last Page      6
    Sort Column With Last Page      7
    Sort Column With Last Page      8
    Sort Column With Last Page      9

Usage History Filtration
    [Tags]                          Filtration
    Filter Field                    1   2   qwerty
    Filter Field                    2   5   1000
    Filter Field                    3   6   AD
    Filter Field                    4   7   225

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Click Link                      xpath://*[@href="/order-status"]
    Sleep                           5 second
    Click Element                   xpath:${header xpath}/thead/tr/th[8]/div[1]
    Click Element                   xpath:${header xpath}/thead/tr/th[8]/div[1]
    ${order number}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[1]/div
    Set Suite Variable              ${order number}
    Click Element                   xpath:${table xpath}/tbody/tr[1]/td[12]${button success}
    Choose From Select Box          ${modal dialog}${select control}    DELIVERED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           3 second
    Click Link                      xpath://*[@href="/usage-history"]
    Section Is Present              css:div.btn
    Sleep                           1 second
    Click Element                   xpath:${last page}
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${number of row}