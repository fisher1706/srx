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
    Is Customer Shipto
    Click Element                   css:#customer-details-pane-shiptos > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
    Is Add Shipto
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Shipto
    Click Element                   css:#customer-details-pane-shiptos > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
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
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Customer Shipto

Valid Create New Shipto
    Goto Customer Shipto
    Sleep                           4 second
    Is Customer Shipto
    Click Element                   css:#customer-details-pane-shiptos > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
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
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is Customer Shipto

Checking New Shipto
    Sleep                           5 second
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[1]/div      ${dynamic name}
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[2]/div      ${dynamic full adress}
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[3]/div      ${test number}

Edit Shipto
    Click Element                   ${edit shipto button}
    Is Edit Shipto
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Shipto
    Click Element                   ${edit shipto button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Customer Shipto
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
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is Customer Shipto

Checking Edit Shipto
    Sleep                           5 second
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[1]/div      ${edit name}
    Element Text Should Be          xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]/td[2]/div      ${edit full adress}

Invalid Create New User
    [Tags]                          User
    Goto Customer Users
    Sleep                           4 second
    Is Customer Users
    Click Element                   css:#customer-details-pane-users > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
    Is Add User
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Users
    Click Element                   css:#customer-details-pane-users > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
    Press Key                       css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:firstName_id                                                                                     \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:lastName_id                                                                                      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(3) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       xpath:${select control}/div[1]/div[2]    \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(4) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Customer Users

Valid Create New User
    Goto Customer Users
    Sleep                           4 second
    Is Customer Users
    Click Element                   css:#customer-details-pane-users > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)
    Input Text                      css:.item-form-modal-body > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)                ${dynamic email}
    Input Text                      id:firstName_id             ${user first name}
    Input Text                      id:lastName_id              ${user last name}
    Click Element                   xpath:${select control}
    Press Key                       xpath:${select control}/div[1]/div[2]    \ue015
    Press Key                       xpath:${select control}/div[1]/div[2]    \ue004
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[5]/div/div[${number of new row s}]/label/input
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is Customer Users

Checking New User
    Sleep                           5 second
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[2]/div     ${dynamic email}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[3]/div     ${user first name}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[4]/div     ${user last name}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[5]/div     Customer User
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[6]/div     ${edit name}

Edit User
    Click Element                   ${edit user button}
    Is Edit User
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Users
    Click Element                   ${edit user button}
    Click Element                   css:.modal-dialog-cancel-button
    Sleep                           2 second
    Is Customer Users
    Click Element                   ${edit user button}
    Input Text                      id:firstName_id             ${edit first name}
    Input Text                      id:lastName_id              ${edit last name}
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div[1]/label/input
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div[${number of new row s}]/label/input
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           2 second
    Is Customer Users

Checking Edit User
    Sleep                           5 second
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[2]/div     ${dynamic email}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[3]/div     ${edit first name}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[4]/div     ${edit last name}
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[5]/div     Customer User
    Element Text Should Be          xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]/td[6]/div     2048

Delete User
    Click Element                   ${delete user button}
    Is Delete
    Click Element                   css:.close
    Sleep                           2 second
    Is Customer Users
    Click Element                   ${delete user button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Sleep                           2 second
    Is Customer Users
    Click Element                   ${delete user button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]      ${dynamic email}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]      ${edit first name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[4]      ${edit last name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]      Customer User
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[6]      2048
    Click Element                   css:button.btn-danger:nth-child(2)
    Sleep                           10 second

Delete Shipto
    Goto Customer Shipto
    Sleep                           4 second
    Is Customer Shipto
    Click Element                   ${delete shipto button}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]      ${edit name}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]      ${edit full adress}
    Click Element                   css:button.btn-danger:nth-child(2)
    Sleep                           5 second

Checking Customer Settings Replenishment Rules
    [Tags]                          CustomerSettings
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-replenishment-rules
    Element Should Be Enabled       xpath:(${customer repl rule}${radio button})[1]/input
    Element Should Be Enabled       xpath:(${customer repl rule}${radio button})[2]/input
    Element Should Be Enabled       xpath:(${customer repl rule}${radio button})[3]/input
    Click Element                   xpath:(${customer repl rule}${radio button})[3]/input
    Click Element                   css:#customer-settings-pane-replenishment-rules > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)
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
    Click Element                   css:#customer-settings-pane-replenishment-rules > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)
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
    [Tags]                          CustomerSettings
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-order-close-logic
    Click Element                   css:div.radio:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:#customer-settings-pane-order-close-logic > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Sleep                           5 second
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(4) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(2) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(1) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="true"        Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[1]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="true"           Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[2]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="true"           Log To Console      Pass    ELSE    Fail    Fail
    Click Element                   css:div.radio:nth-child(2) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:#customer-settings-pane-order-close-logic > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Sleep                           5 second
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(4) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(2) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="true"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(1) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[1]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="false"          Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[2]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="true"           Log To Console      Pass    ELSE    Fail    Fail
    Click Element                   css:div.radio:nth-child(4) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:#customer-settings-pane-order-close-logic > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Sleep                           5 second
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[1]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="true"           Log To Console      Pass    ELSE    Fail    Fail
    ${aria}                         Get Element Attribute       xpath:(${customer order close logic}${select control})[2]/div/div[2]     aria-disabled
    Run Keyword If                  "${aria}"=="false"          Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(4) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="true"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(2) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail
    ${checked}                      Get Element Attribute       css:div.radio:nth-child(1) > label:nth-child(1) > input:nth-child(1)     checked
    Run Keyword If                  "${checked}"=="None"        Log To Console      Pass    ELSE    Fail    Fail

*** Keywords ***
Preparation
    Goto Customer Menu
    Sleep                           1 second
    Goto Customer Shipto
    Sleep                           4 second
    Number Of Rows Shiptos
    ${number of new row s}=         Evaluate                        ${number of row s}+1
    Set Global Variable             ${number of new row s}
    Set Global Variable             ${edit shipto button}           xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]${button success}
    Set Global Variable             ${delete shipto button}         xpath:${shiptos pane}${table xpath}/tbody/tr[${number of new row s}]${button danger}
    Goto Customer Users
    Sleep                           4 second
    Is Customer Users
    Number Of Rows Users
    ${number of new row u}=         Evaluate                        ${number of row u}+1
    Set Global Variable             ${number of new row u}
    Set Global Variable             ${edit user button}             xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]${button success}
    Set Global Variable             ${delete user button}           xpath:${users pane}${table xpath}/tbody/tr[${number of new row u}]${button danger}

Is Add Shipto
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                Add shipto

Is Edit Shipto
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                Edit shipto

Is Add User
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                Add customer user

Is Edit User
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                Edit customer user

Is Delete
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                Removal Confirmation