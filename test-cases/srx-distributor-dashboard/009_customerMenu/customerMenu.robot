*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Invalid Create New Shipto
    Goto Customer Shipto
    Sleep                           4 second
    Click Element                   xpath:${shiptos pane}${button primary}
    Press Key                       css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                    \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:address.line1_id                                                                                     \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:address.city_id                                                                                      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(5) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:address.zipCode_id                                                                                   \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(6) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           5 second

Valid Create New Shipto
    Click Element                   xpath:${shiptos pane}${button primary}
    Input Text                      css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                    ${dynamic name}
    Input Text                      id:address.line1_id     ${dynamic adress1}
    Input Text                      id:address.line2_id     ${dynamic adress2}
    Input Text                      id:address.city_id      ${dynamic city}
    Click Element                   xpath:${select control}
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue015
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue007
    Input Text                      id:address.zipCode_id   ${dynamic code}
    Input Text                      id:poNumber_id          ${test number}
    Click Element                   xpath:${button modal dialog ok}

Checking New Shipto
    Sleep                           5 second
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[1]/div      ${dynamic name}
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[2]/div      ${dynamic full adress}
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[3]/div      ${test number}

Edit Shipto
    Click Element                   ${edit shipto button}
    Input Text                      css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                    ${edit name}
    Input Text                      id:address.line1_id     ${edit adress1}
    Input Text                      id:address.line2_id     ${edit adress2}
    Input Text                      id:address.city_id      ${edit city}
    Click Element                   xpath:${select control}
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue013
    Press Key                       xpath:${select control}/div[1]/div[2]            \ue007
    Input Text                      id:address.zipCode_id   ${edit code}
    Clear Element Text              id:poNumber_id
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           2 second

Checking Edit Shipto
    Sleep                           5 second
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[1]/div      ${edit name}
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[2]/div      ${edit full adress}

Invalid Create New User
    [Tags]                          User
    Goto Customer Users
    Click Element                   xpath:${users pane}${button primary}
    Press Key                       css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:firstName_id                                                                                     \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:lastName_id                                                                                      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       xpath:${select control}/div[1]/div[2]    \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   xpath:${button modal dialog cancel}
    Sleep                           5 second

Valid Create New User
    Click Element                   xpath:${users pane}${button primary}
    Input Text                      css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                ${dynamic email}
    Input Text                      id:firstName_id             ${user first name}
    Input Text                      id:lastName_id              ${user last name}
    Click Element                   xpath:${select control}
    Press Key                       xpath:${select control}/div[1]/div[2]    \ue015
    Press Key                       xpath:${select control}/div[1]/div[2]    \ue004
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div[${number of new row s}]/label/input
    Click Element                   xpath:${button modal dialog ok}

Checking New User
    Sleep                           5 second
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[2]/div     ${dynamic email}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[3]/div     ${user first name}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[4]/div     ${user last name}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[5]/div     Customer User
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[6]/div     ${edit name}

Edit User
    Click Element                   ${edit user button}
    Input Text                      id:firstName_id             ${edit first name}
    Input Text                      id:lastName_id              ${edit last name}
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div[1]/label/input
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div[${number of new row s}]/label/input
    Click Element                   xpath:${button modal dialog ok}

Checking Edit User
    Sleep                           5 second
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[2]/div     ${dynamic email}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[3]/div     ${edit first name}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[4]/div     ${edit last name}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[5]/div     Customer User
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[6]/div     2048

Delete User
    Click Element                   ${delete user button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]      ${dynamic email}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]      ${edit first name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]      ${edit last name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]      Customer User
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]      2048
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           10 second

Sorting Customer Users
    [Tags]                          Sorting
    Sort Customer Users             2   ${number of row u}
    Sort Customer Users             3   ${number of row u}
    Sort Customer Users             4   ${number of row u}
    Sort Customer Users             5   ${number of row u}

Customer Users Filtration
    [Tags]                          Filter
    Filter Customer Users           1   2   srx-group+dev-customer@agilevision.io
    Filter Customer Users           2   3   srx
    Filter Customer Users           3   4   group

Delete Shipto
    Goto Customer Shipto
    Sleep                           4 second
    Click Element                   ${delete shipto button}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]      ${edit name}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]      ${edit full adress}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

Sorting Shiptos
    [Tags]                          Sorting
    Sort Shiptos                    1   ${number of row s}
    Sort Shiptos                    3   ${number of row s}

Shiptos Filtration
    [Tags]                          Filter
    Filter Shiptos                  1   1   4096
    Filter Shiptos                  2   3   9000

Checking Customer Settings Replenishment Rules
    [Tags]                          CustomerSettings
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-replenishment-rules
    Sleep                           3 second
    Element Should Be Enabled       xpath:(${customer repl rule}${radio button})[1]/input
    Element Should Be Enabled       xpath:(${customer repl rule}${radio button})[2]/input
    Element Should Be Enabled       xpath:(${customer repl rule}${radio button})[3]/input
    Click Element                   xpath:(${customer repl rule}${radio button})[3]/input
    Click Element                   xpath:${customer repl rule}${button primary}
    Sleep                           5 second
    Reload Page
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-replenishment-rules
    Sleep                           3 second
    ${checked}                      Get Element Attribute       xpath:(${customer repl rule}${radio button})[3]/input     checked
    Run Keyword If                  "${checked}"=="true"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       xpath:(${customer repl rule}${radio button})[1]/input     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       xpath:(${customer repl rule}${radio button})[2]/input     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    Click Element                   xpath:(${customer repl rule}${radio button})[2]/input
    Click Element                   xpath:${customer repl rule}${button primary}
    Sleep                           5 second
    Reload Page
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-replenishment-rules
    Sleep                           3 second
    ${checked}                      Get Element Attribute       xpath:(${customer repl rule}${radio button})[2]/input     checked
    Run Keyword If                  "${checked}"=="true"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       xpath:(${customer repl rule}${radio button})[1]/input     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       xpath:(${customer repl rule}${radio button})[3]/input     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail

Checking Customer Settings Order Close Logic
    [Tags]                          CustomerSettings    OrderCloseLogic
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-order-close-logic
    Sleep                           3 second
    Click Element                   xpath:(${customer order close logic}${radio button type})[1]
    Click Element                   xpath:${customer order close logic}${button primary}
    Sleep                           5 second
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[3]     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[2]     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[1]     checked
    Run Keyword If                  "${checked}"=="true"        Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[1]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="true"           Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[2]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="true"           Log To Console      Pass    ELSE    Fail    Fail
    Click Element                   (${customer order close logic}${radio button type})[2]
    Click Element                   xpath:${customer order close logic}${button primary}
    Sleep                           5 second
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[3]     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[2]     checked
    Run Keyword If                  "${checked}"=="true"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[1]     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[1]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="false"          Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[2]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="true"           Log To Console      Pass    ELSE    Fail    Fail
    Click Element                   (${customer order close logic}${radio button type})[3]
    Click Element                   xpath:${customer order close logic}${button primary}
    Sleep                           5 second
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[1]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="true"           Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[2]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="false"          Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[3]     checked
    Run Keyword If                  "${checked}"=="true"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[2]     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       (${customer order close logic}${radio button type})[1]     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Click Link                      xpath://*[@href="/customers"]
    Sleep                           5 second
    ${my customer}                  Get Row By Text     ${table xpath}      1   Static Customer
    Set Suite Variable              ${my customer}
    Click Element                   xpath:${table xpath}/tbody/tr[${my customer}]/td[1]/a
    Sleep                           1 second
    Goto Customer Shipto
    Sleep                           4 second
    Number Of Rows Shiptos
    ${number of new row s}=         Evaluate                        ${number of row s}+1
    Set Suite Variable              ${number of new row s}
    Set Suite Variable              ${edit shipto button}           xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]${button success}
    Set Suite Variable              ${delete shipto button}         xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]${button danger}
    Goto Customer Users
    Sleep                           4 second
    Number Of Rows Users
    ${number of new row u}=         Evaluate                        ${number of row u}+1
    Set Suite Variable              ${number of new row u}
    Set Suite Variable              ${edit user button}             xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]${button success}
    Set Suite Variable              ${delete user button}           xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]${button danger}

Filter Customer Users
    [Arguments]                     ${dialog index}     ${table index}      ${value}
    Click Element                   xpath:${users pane}${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[${dialog index}]         ${value}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${users pane}${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${users pane}${table xpath}/tbody/tr[${index}]/td[${table index}]      ${value}
    Click Element                   xpath:${users pane}${button default}
    Sleep                           3 second

Sort Customer Users
    [Arguments]                     ${column}       ${count}
    Click Element                   xpath:${users pane}${header xpath}/thead/tr/th[${column}]
    ${text buffer1up}               Get Text                    xpath:${users pane}${table xpath}/tbody/tr[1]/td[${column}]
    ${text buffer1down}             Get Text                    xpath:${users pane}${table xpath}/tbody/tr[${count}]/td[${column}]
    Click Element                   xpath:${users pane}${header xpath}/thead/tr/th[${column}]
    ${text buffer2up}               Get Text                    xpath:${users pane}${table xpath}/tbody/tr[1]/td[${column}]
    ${text buffer2down}             Get Text                    xpath:${users pane}${table xpath}/tbody/tr[${count}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${users pane}${header xpath}/thead/tr/th[${column}]

Filter Shiptos
    [Arguments]                     ${dialog index}     ${table index}      ${value}
    Click Element                   xpath:${shiptos pane}${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[${dialog index}]         ${value}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${shiptos pane}${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${shiptos pane}${table xpath}/tbody/tr[${index}]/td[${table index}]      ${value}
    Click Element                   xpath:${shiptos pane}${button default}
    Sleep                           3 second

Sort Shiptos
    [Arguments]                     ${column}       ${count}
    Click Element                   xpath:${shiptos pane}${header xpath}/thead/tr/th[${column}]
    ${text buffer1up}               Get Text                    xpath:${shiptos pane}${table xpath}/tbody/tr[1]/td[${column}]
    ${text buffer1down}             Get Text                    xpath:${shiptos pane}${table xpath}/tbody/tr[${count}]/td[${column}]
    Click Element                   xpath:${shiptos pane}${header xpath}/thead/tr/th[${column}]
    ${text buffer2up}               Get Text                    xpath:${shiptos pane}${table xpath}/tbody/tr[1]/td[${column}]
    ${text buffer2down}             Get Text                    xpath:${shiptos pane}${table xpath}/tbody/tr[${count}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${shiptos pane}${header xpath}/thead/tr/th[${column}]