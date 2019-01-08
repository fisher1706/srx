*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Sort RFID
    [Tags]                          Sorting
    Sort Column                     1                   ${number of row}
    Sort Column                     2                   ${number of row}
    Sort Column                     3                   ${number of row}
    Sort Column                     4                   ${number of row}
    Sort Column                     5                   ${number of row}

Filter RFID User
    [Tags]                          Filter
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[1]       SYSTEM
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${table xpath}/tbody/tr[${index}]/td[4]   SYSTEM
    Click Element                   xpath:${button default}
    Sleep                           3 second

Filter RFID State
    [Tags]                          Filter
    Click Element                   xpath:${button right margin}
    Choose From Select Box          ${modal dialog}${select control}                ISSUED
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${table xpath}/tbody/tr[${index}]/td[2]   ISSUED
    Click Element                   xpath:${button default}
    Sleep                           3 second

Filter RFID Associated Data
    [Tags]                          Filter
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[4]       TestDATA
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[5]/div      TestDATA
    Click Element                   xpath:${button default}
    Sleep                           2 second

Filter RFID Date
    [Tags]                          Filter      FilterDate
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[2]       11/28/2018, 2:58 P
    Input Text                      xpath:(${modal dialog}${form control})[3]       11/28/2018, 3:00 P
    Sleep                           5 second
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[3]/div      11/28/2018, 2:59 PM
    Click Element                   xpath:${button default}
    Sleep                           2 second

*** Keywords ***
Preparation
    Goto RFID
    Input Text                      xpath:(${select control})[2]/div/div/input       STATIC SKU
    Press Key                       xpath:(${select control})[2]/div/div/input       \ue007
    Sleep                           3 second
    Open Full Table
    ${number of row}                Get Rows Count              ${table xpath}
    Set Suite Variable              ${number of row}