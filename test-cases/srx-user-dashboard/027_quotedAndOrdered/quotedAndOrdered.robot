*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Sorting List
    [Tags]                          Sorting
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[2]/a
    Open Minimum Table
    Sort Column With Last Page      1
    Sort Column With Last Page      2
    Sort Column With Last Page      3
    Sort Column With Last Page      4
    Sort Column With Last Page      5
    Sort Column With Last Page      6

Filter List
    [Tags]                          Filter
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[2]/a
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[1]       TEST_DSN
    Input Text                      xpath:(${modal dialog}${form control})[2]       4
    Input Text                      xpath:(${modal dialog}${form control})[3]       G030PM036107NGQ5
    Choose From Select Box          ${select control}       DELIVERED
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[1]/div      TEST_DSN
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]/div      4
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[4]/div      G030PM036107NGQ5
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[5]/div      DELIVERED

*** Keywords ***
Preparation
    Start Customer
    Sleep                           2 second
    Click Element                   xpath:/html/body/div/div/div/div/div/div/button[1]
    Click Element                   css:.select-shipto-button
    Is Customer Portal
