*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Invalid Create New Customer Type
    [Tags]                          InvalidCreateNewCustomer
    Click Element                   css:.btn-primary
    Is Add Customer Type
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Types
    Click Element                   css:.btn-primary
    Press Key                       id:name_id                      \ue004
    Element Should Be Enabled       css:.fa-exclamation-circle > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Customer Types

Valid Create New Customer Type
    Click Element                   css:.btn-primary
    Is Add Customer Type
    Input Text                      id:name_id                      ${test type}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           1 second
    Is Customer Types

Checking New Customer Type In Table
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div              ${test type}

Checking New Customer Type On Distributor Portal
    [Tags]                          CheckingOnDistributorPortal
    Goto Customer Menu Sub
    Click Element                   ${edit customer button sub}
    Go Down
    Sleep                           1 second
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${static row c}]/td[4]/div      ${test type}
    Click Element                   ${edit customer button sub}
    Go Up
    Sleep                           1 second
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${static row c}]/td[4]/div      Not specified
    Finish Suite

Edit Customer Type
    Sleep                           5 second
    Preparation
    Click Element                   ${edit button}
    Is Edit Customer Type
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Types
    Click Element                   ${edit button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Customer Types
    Click Element                   ${edit button}
    Input Text                      id:name_id                      ${edit test type}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           1 second
    Is Customer Types

Delete Customer Type
    Click Element                   ${delete button}
    Is Delete Customer Type
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Types
    Click Element                   ${delete button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Is Customer Types
    Click Element                   ${delete button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]          ${edit test type}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           5 second

Sorting Customer Types By Id
    [Tags]                          Sorting
    Click Element                   css:th.sort-column:nth-child(1)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[1]/div
    Click Element                   css:th.sort-column:nth-child(1)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}-1]/td[1]/div
    Should Be Equal                 ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(1)

Sorting Customer Types By Type
    [Tags]                          Sorting
    Click Element                   css:th.sort-column:nth-child(2)
    ${text buffer1}                 Get Text            xpath:${table xpath}/tbody/tr[1]/td[2]/div
    Click Element                   css:th.sort-column:nth-child(2)
    ${text buffer2}                 Get Text            xpath:${table xpath}/tbody/tr[${number of row}-1]/td[2]/div
    Should Be Equal                 ${text buffer1}     ${text buffer2}
    Click Element                   css:th.sort-column:nth-child(2)

*** Keywords ***
Goto Customer Menu Sub
    Finish Suite
    Run Keyword If                  "${browser}"=="xvfb"            Run Xvfb Sub    ELSE IF     "${browser}"=="chrome"      Run Chrome Sub      ELSE    Run Ff Sub
    Set Selenium Implicit Wait                                      20 second
    Set Selenium Timeout                                            10 second
    Enter Correct Email Sub
    Enter Password
    Correct Submit Login
    Click Link                      xpath://*[@href="/customers"]
    Sleep                           5 second
    Is Customer Management
    Number Of Rows Sub
    Number Of Static Row Sub
    Set Global Variable             ${edit customer button sub}     xpath:${table xpath}/tbody/tr[${static row c}]/td[6]/div/div[1]/button

Preparation
    Goto Customer Types
    Sleep                           1 second
    Is Customer Types
    Number Of Rows
    ${number of new row}=           Evaluate                        ${number of row}+1
    Set Global Variable             ${number of new row}
    Set Global Variable             ${edit button}                  xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div/div[1]/button
    Set Global Variable             ${delete button}                xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div/div[2]/button
    ${SUB HOST}                     Return Sub Link
    Set Global Variable             ${SUB HOST}
    ${SUB EMAIL}                    Return Sub Email
    Set Global Variable             ${SUB EMAIL}

Is Add Customer Type
    Element Text Should Be          css:.modal-title                Add customer type

Is Edit Customer Type
    Element Text Should Be          css:.modal-title                Edit customer type

Is Delete Customer Type
    Element Text Should Be          css:.modal-title                Removal Confirmation

Number Of Rows Sub
    ${number of row sub}            Get Element Count               xpath:${table xpath}/tbody/tr
    Set Global Variable             ${number of row sub}

Number Of Static Row Sub
    : FOR   ${counter c sub}        IN RANGE    1   ${number of row sub}+1
    \   ${text buffer1 c sub}       Get Text    xpath:${table xpath}/tbody/tr[${counter c sub}]/td[1]/a
    \   Exit For Loop If            "Customer Z"=="${text buffer1 c sub}"
    Set Global Variable             ${static row c}     ${counter c sub}

Go Down
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]            \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]            \ue007
    ${text buffer sub}              Get Text                                    xpath:(${select control})[1]/div[1]/div[1]/span
    Sleep                           1 second
    Run Keyword If                  "${text buffer sub}"!="${test type}"        Go Down

Go Up
    Click Element                   css:.Select-control
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]            \ue015
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]            \ue007
    ${text buffer sub}              Get Text                                    xpath:(${select control})[1]/div[1]/div[1]/span
    Sleep                           1 second
    Run Keyword If                  "${text buffer sub}"!="Not specified"       Go Down