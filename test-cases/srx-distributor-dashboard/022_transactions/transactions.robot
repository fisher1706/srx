*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Sorting Transactions
    [Tags]                          Sorting
    Sorting Transactions Column     1
    Sorting Transactions Column     2
    Sorting Transactions Column     3
    Sorting Transactions Column     5
    Sorting Transactions Column     6
    Sorting Transactions Column     7
    Sorting Transactions Column     8
    Sorting Transactions Column     9

Transactions Filtration
    [Tags]                          Filter
    Filter Check Tr                 xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/input                      STATIC SKU
    Filter Check Tr                 xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/input                      SSKU
    Filter Check Tr                 xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/input                      30
    Filter Check Tr                 xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[4]/div[2]/input                      4550
    Field Selector Check Tr         xpath:/html/body/div[2]/div[2]/div/div/div[2]/div[6]/div[2]/div/div/div/div/div[1]     CUSTOMER

*** Keywords ***
Preparation
    Goto Transactions

Sorting Transactions Column
    [Arguments]                     ${column}
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    Sleep                           3 second
    ${text buffer1up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    Number Of Rows
    ${text buffer1down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    Sleep                           3 second
    ${text buffer2up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   css:li.page-item:nth-child(7) > a:nth-child(1)
    ${text buffer2down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]

Filter Check Tr
    [Arguments]                     ${inputField}            ${inputText}
    Click Element                   css:.button-right-margin
    Input Text                      ${inputField}            ${inputText}
    ${result} =                     Fetch From Left          ${inputField}    2]/input
    ${newString}=                   Strip String             ${result}1]/div
    ${fieldName}                    Get Text                 ${newString}
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/button[2]
    Sleep                           2 seconds
    ${rowNum}                       Get Element Count        xpath:${header xpath}/thead/tr/th
    ${rowNum}=                      Evaluate                 ${rowNum}+1
     :FOR   ${var}                  IN RANGE            1    ${rowNum}
    \       ${textInfo}             Get Text                 xpath:${header xpath}/thead/tr/th[${var}]
    \       Run Keyword If          "${textInfo}" == "${fieldName}"      Field Comparing   ${var}        ${inputText}
    Click Element                   css:button.button-right-margin:nth-child(2)
    Sleep                           2 seconds

Field Comparing
    [Arguments]                     ${rowNum}               ${expectedValue}
    ${rowValue}                     Get Text                xpath:${table xpath}/tbody/tr/td[${rowNum}]
    Should Be Equal As Strings      ${rowValue}             ${expectedValue}

Field Selector Check Tr
    [Arguments]                     ${fieldAdr}             ${fieldType}
    Click Element                   css:.button-right-margin
    ${result} =                     Fetch From Left         ${fieldAdr}    2]/div/div/div/div/div[1]
    ${newString}=                   Strip String            ${result}1]/div
    ${fieldName}                    Get Text                ${newString}
    Go Down                         ${fieldAdr}             ${fieldType}
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[3]/button[2]
    Sleep                           3 seconds
    ${rowNum}                       Get Element Count       xpath:${header xpath}/thead/tr/th
    ${rowNum}=                      Evaluate                ${rowNum}+1
     :FOR   ${var}                  IN RANGE            1   ${rowNum}
    \       ${textInfo}             Get Text                xpath:${header xpath}/thead/tr/th[${var}]
    \       Run Keyword If          "${textInfo}" == "${fieldName}"      Field Comparing   ${var}        ${fieldType}
    Click Element                   css:button.button-right-margin:nth-child(2)
    Sleep                           2 seconds

Go Down
    [Arguments]                     ${fieldAdr}             ${field type}
    Click Element                   ${fieldAdr}
    ${result} =                     Fetch From Left         ${fieldAdr}    div/div[1]
    ${newString}=                   Strip String            ${result}div[1]/div[2]
    Press Key                       ${newString}            \ue015
    Press Key                       ${newString}            \ue007              
    ${text buffer sub}              Get Text                 ${fieldAdr}
    Sleep                           1 second
    Run Keyword If                  "${text buffer sub}"!="${field type}"        Go Down    ${fieldAdr}    ${field type}
