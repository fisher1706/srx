*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Sorting Activity Log
    [Tags]                          Sorting
    Sorting React With Last Page    2
    Sorting React With Last Page    3
    Sorting React With Last Page    4
    Sorting React With Last Page    5
    Sorting React With Last Page    6
    Sorting React With Last Page    7
    Sorting React With Last Page    8

Filter Activity Log
    [Tags]                          Filter
    Filter React Select Box         1   2   Transaction
    Filter Action                   Transaction     SPLIT
    Filter React Select Box         3   8   FAIL
    Filter React Select Box         4   5   HARDWARE

Filter Activity Log Date
    [Tags]                          Filter      FilterDate
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[1]       2/7/2019, 6:15 A
    Input Text                      xpath:(${modal dialog}${form control})[2]       2/7/2019, 6:17 A
    Sleep                           2 second
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    Element Text Should Be          xpath:(${react table column})[7]      2/7/2019, 6:16 AM
    Click Element                   xpath:${button default}
    Sleep                           2 second

*** Keywords ***
Preparation
    Goto Activity Log
    Sleep                           5 second

Filter Action
    [Arguments]                     ${value type}      ${value action}
    Click Element                   xpath:${button right margin}
    Choose From Select Box          (${modal dialog}${select control})[1]             ${value type}
    Choose From Select Box          (${modal dialog}${select control})[2]             ${value action}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Element Count                   xpath:${react table raw}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:((${react table raw})[${index}]${react table column})[3]   ${value action}
    Click Element                   xpath:${button default}
    Sleep                           3 second