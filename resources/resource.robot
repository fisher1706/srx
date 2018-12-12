*** Settings ***
Library                             XvfbRobot

*** Variables ***
${LOGIN URL}                        https://${HOST}/sign-in
${browser}                          ff
${X}                                1920
${Y}                                1080
${correct wrong email}              example@example.com
${incorrect email}                  example.agilevision.io
${element login button}             css:.btn

*** Keywords ***
Login In Distributor Portal
    Start Suite
    Enter Correct Email
    Enter Password
    Correct Submit Login
    Section Is Present              xpath://*[@href="/sign-out"]
    Sleep                           5 second

Login In Customer Portal
    Start Suite
    Enter Correct Email
    Enter Password
    Correct Submit Login
    Is Select A Shipto

Goto Customer Menu
    Goto Customer Management
    Number Of Rows C
    Number Of Static Row C
    Click Element                   xpath:${table xpath}/tbody/tr[${static row c}]/td[1]/a

Goto Security Groups
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/security-groups"]
    Sleep                           5 second

Goto Camera View
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/camera-view"]
    Sleep                           5 second

Goto Settings
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/settings"]
    Sleep                           3 second

Goto Usage History
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/usage-history"]
    Sleep                           5 second

Goto Transactions
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/transactions"]
    Sleep                           5 second

Goto Transaction Log
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/transaction-log"]
    Sleep                           5 second

Goto Locations
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/locations"]
    Sleep                           5 second

Goto Customer Management
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/customers"]
    Sleep                           5 second

Goto User Managemant
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/users"]
    Sleep                           5 second

Goto Fees
    Login In Admin Portal
    Click Link                      xpath://*[@href="/fees"]
    Sleep                           5 second

Goto Catalog
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/catalog"]
    Sleep                           5 second

Goto Pricing
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/pricing"]
    Sleep                           5 second

Goto Reports
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/reports"]
    Sleep                           5 second

Goto Customer Types
    Login In Admin Portal
    Click Link                      xpath://*[@href="/customer-types"]
    Sleep                           5 second

Goto Warehouses
    Login In Admin Portal
    Click Link                      xpath://*[@href="/warehouses"]
    Sleep                           5 second

Goto Market Types
    Login In Admin Portal
    Click Link                      xpath://*[@href="/market-types"]
    Sleep                           5 second

Goto Admin Users
    Login In Admin Portal
    Sleep                           7 second
    Click Element                   css:#pageDropDown
    Click Element                   css:li.dropdown-item:nth-child(4) > a:nth-child(1)
    Sleep                           2 second
    Number Of Rows E
    Number Of Static Row E
    Click Element                   xpath:${table xpath}/tbody/tr[${static row e}]/td[1]/a

Goto Customer Info
    Click Element                   id:customer-details-tab-general-info

Is Customer Info
    Element Should Be Visible       id:customer-details-pane-general-info

Goto Customer Contact Info
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-contact-info

Goto Customer Shipto
    Click Element                   id:customer-details-tab-shiptos

Is Customer Shipto
    Element Should Be Visible       id:customer-details-pane-shiptos

Goto Customer Users
    Click Element                   id:customer-details-tab-users

Is Customer Users
    Element Should Be Visible       id:customer-details-pane-users

Goto Customer Cost Saving
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-cost-savings

Login In Admin Portal
    Start Suite
    Enter Correct Email
    Enter Password
    Correct Submit Login
    Is Distributors Page

Enter Correct Email
    Input Text                      id:email        ${email}

Enter Password
    Input Text                      id:password     ${password}

Correct Submit Login
    Click Element                   ${element login button}

Sign Out
    Click Link                      xpath://*[@href="/sign-out"]

Start Suite
    Run Keyword If                  "${browser}"=="xvfb"    Run Xvfb    ELSE IF     "${browser}"=="chrome"      Run Chrome  ELSE    Run Ff
    Set Selenium Implicit Wait      20 second
    Set Selenium Timeout            10 second

Run Xvfb
    Start Virtual Display           ${X}                    ${Y}
    Open Browser                    ${LOGIN URL}
    Set Window Size                 ${X}                    ${Y}

Run Chrome
    Open Browser                    ${LOGIN URL}            chrome
Run Ff
    Open Browser                    ${LOGIN URL}            ff

Finish Suite
    Close All Browsers

Is Customer Portal
    Element Text Should Be          xpath:/html/body/div/div/div/div[1]/div/div/div/div[2]/p[2]     ${email}

Is Customer Portal Sub
    Element Text Should Be          xpath:/html/body/div/div/div/div[1]/div/div/div/div[2]/p[2]     ${SUB EMAIL}

Is Select A Shipto
    Element Text Should Be          css:.ship-to-select-label                                   Select a ship-to record

Is Security Groups
    Element Text Should Be          css:.page-header > h1:nth-child(1)                          Security Groups

Is Customer Types
    Element Text Should Be          css:.customer-types-management-header > h1:nth-child(1)     Customer Types Management

Is Market Types
    Element Text Should Be          css:.market-types-management-header > h1:nth-child(1)       Market Types Management

Is Login Page
    Element Text Should Be          xpath:/html/body/div/div/div/div/div/form/div[4]/label      Password

Is Customer Management
    Element Text Should Be          css:.customer-management-header > h1:nth-child(1)           Customer Management

Is Distributors Page
    Element Text Should Be          xpath:/html/body/div/div/div/div[2]/div/div[1]/div/div/h1   Distributor Management
    Element Text Should Be          css:.sidebar-user-info > p:nth-child(2)                     ${email}

Is Distributor Info
    Element Text Should Be          css:.back-link                                              Back to Distributors List

Is Fees Managemant
    Element Text Should Be          css:.distributor-management-header > h1:nth-child(1)        Fees Management

Is Usage History
    Element Text Should Be          css:.page-header > h1:nth-child(1)                          Usage History

Is Transactions
    Element Text Should Be          css:.customer-management-header > h1:nth-child(1)           Transactions

Is Setting General Settings
    Element Text Should Be          css:#settings-pane-1 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h4:nth-child(1) > strong:nth-child(1)      Distributor logo:

Is Locations
    Element Text Should Be          css:.locations-management-header > h1:nth-child(1)          Locations

Is User Management
    Element Text Should Be          css:.user-management-header > h1:nth-child(1)               User Management

Is Warehouse Management
    Element Text Should Be          css:.warehouse-management-header > h1:nth-child(1)          Warehouse Management

Is Catalog
    Element Text Should Be          css:.customer-management-header > h1:nth-child(1)           Catalog

Sorting Column
    [Arguments]                     ${column}
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer1up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    ${text buffer1down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer2up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    ${text buffer2down}             Get Text                    xpath:${table xpath}/tbody/tr[${number of row}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]

Number Of Rows C
    ${number of row c}              Get Element Count   xpath:${table xpath}/tbody/tr
    Set Global Variable             ${number of row c}

Number Of Static Row C
    : FOR   ${counter c}            IN RANGE    1   ${number of row c}+1
    \   ${text buffer1 c}           Get Text    xpath:${table xpath}/tbody/tr[${counter c}]/td[1]/a
    \   Exit For Loop If            "Static Customer"=="${text buffer1 c}"
    Set Global Variable             ${static row c}     ${counter c}

Number Of Rows E
    ${number of row e}              Get Element Count   xpath:${table xpath}/tbody/tr
    Set Global Variable             ${number of row e}

Number Of Static Row E
    : FOR   ${counter e}            IN RANGE    1   ${number of row e}+1
    \   ${text buffer1 e}           Get Text    xpath:${table xpath}/tbody/tr[${counter e}]/td[1]/a
    \   Exit For Loop If            "${static name}"=="${text buffer1 e}"
    Set Global Variable             ${static row e}     ${counter e}

Successfull Upload
    Pass Execution                  Successfully imported!

Fail Upload
    Fail                            Operation failed!

Return Sub Link
    Return From Keyword If          "${HOST}"=="admin-dev.storeroomlogix.com"               distributor-dev.storeroomlogix.com
    Return From Keyword If          "${HOST}"=="distributor-dev.storeroomlogix.com"         admin-dev.storeroomlogix.com
    Return From Keyword If          "${HOST}"=="admin-staging.storeroomlogix.com"           distributor-staging.storeroomlogix.com
    Return From Keyword If          "${HOST}"=="distributor-staging.storeroomlogix.com"     admin-staging.storeroomlogix.com
    
Return Sub Email
    Return From Keyword If          "${HOST}"=="admin-dev.storeroomlogix.com"               srx-group+dev-distributor@agilevision.io
    Return From Keyword If          "${HOST}"=="distributor-dev.storeroomlogix.com"         srx-group+dev@agilevision.io
    Return From Keyword If          "${HOST}"=="admin-staging.storeroomlogix.com"           srx-group+staging-distributor@agilevision.io
    Return From Keyword If          "${HOST}"=="distributor-staging.storeroomlogix.com"     srx-group+staging@agilevision.io

Return CSub Link
    Return From Keyword If          "${HOST}"=="customer-dev.storeroomlogix.com"            distributor-dev.storeroomlogix.com
    Return From Keyword If          "${HOST}"=="distributor-dev.storeroomlogix.com"         customer-dev.storeroomlogix.com
    Return From Keyword If          "${HOST}"=="customer-staging.storeroomlogix.com"        distributor-staging.storeroomlogix.com
    Return From Keyword If          "${HOST}"=="distributor-staging.storeroomlogix.com"     customer-staging.storeroomlogix.com
    
Return CSub Email
    Return From Keyword If          "${HOST}"=="customer-dev.storeroomlogix.com"            srx-group+dev-distributor@agilevision.io
    Return From Keyword If          "${HOST}"=="distributor-dev.storeroomlogix.com"         srx-group+dev-customer@agilevision.io
    Return From Keyword If          "${HOST}"=="customer-staging.storeroomlogix.com"        srx-group+staging-distributor@agilevision.io
    Return From Keyword If          "${HOST}"=="distributor-staging.storeroomlogix.com"     srx-group+staging-customer@agilevision.io

Run Xvfb Sub
    Start Virtual Display           1920                            1080
    Open Browser                    https://${SUB HOST}/sign-in
    Set Window Size                 1920                            1080

Run Chrome Sub
    Open Browser                    https://${SUB HOST}/sign-in     chrome
    
Run Ff Sub
    Open Browser                    https://${SUB HOST}/sign-in     ff

Run Xvfb Out
    Start Virtual Display           1920                            1080
    Open Browser                    ${OUT HOST}
    Set Window Size                 1920                            1080

Run Chrome Out
    Open Browser                    ${OUT HOST}                     chrome
    
Run Ff Out
    Open Browser                    ${OUT HOST}                     ff

Enter Correct Email Sub
    Input Text                      id:email                        ${SUB EMAIL}

Filter Check First Fields
    [Arguments]                     ${inputField}            ${inputText}
    Click Element                   css:.button-right-margin
    Input Text                      ${inputField}            ${inputText}
    ${result} =                     Fetch From Left          ${inputField}    2]/input
    ${newString}=                   Strip String             ${result}1]/div
    ${fieldName}                    Get Text                 ${newString}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           2 seconds
    ${rowNum}                       Get Element Count        xpath:${header xpath}/thead/tr/th
    ${rowNum}=                      Evaluate                 ${rowNum}+1
     :FOR    ${var}                 IN RANGE             1   ${rowNum}
    \        ${textInfo}            Get Text                 xpath:${header xpath}/thead/tr/th[${var}]
    \       Run Keyword If          "${textInfo}" == "${fieldName}"      Field Comparing First Fields   ${var}        ${inputText}
    Click Element                   css:button.button-right-margin:nth-child(2)
    Sleep                           2 seconds

Field Comparing First Fields
    [Arguments]                     ${rowNum}       ${expectedValue}
    ${rowValue}        Get Text     xpath:${table xpath}/tbody/tr/td[${rowNum}]
    Should Be Equal As Strings      ${rowValue}     ${expectedValue}

Set Permission
    [Arguments]                     ${row}      ${column}
    ${checked}                      Get Element Attribute       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[1]/div/table/tbody/tr[${row}]/td[${column}+1]/label/input     checked
    Run Keyword If                  "${checked}"=="None"        Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[1]/div/table/tbody/tr[${row}]/td[${column}+1]/label/input

Set Settings Permission
    [Arguments]                     ${row}      ${column}
    ${checked}                      Get Element Attribute       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/table/tbody/tr[${row}]/td[${column}+1]/label/input     checked
    Run Keyword If                  "${checked}"=="None"        Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/table/tbody/tr[${row}]/td[${column}+1]/label/input

Clear Permission
    [Arguments]                     ${row}
    Run Keyword If                  ${row}==6       Clear Only Read             ${row}
    Run Keyword If                  ${row}==11      Clear Only Read             ${row}
    Run Keyword If                  ${row}==14      Clear Only Read             ${row}
    Run Keyword If                  ${row}!=6 and ${row}!=11 and ${row}!=14     Clear Standart              ${row}

Clear Settings Permission
    [Arguments]                     ${row}
    Run Keyword If                  ${row}==13    Clear Settings Only Read      ${row}
    Run Keyword If                  ${row}==14    Clear Settings Only Read      ${row}
    Run Keyword If                  ${row}!=13 and ${row}!=14                   Clear Settings Standart     ${row}

Clear All Permissions
    Set Suite Variable              ${index}        1
    :FOR  ${index}  IN RANGE  1     16
    \   Clear Permission            ${index}

Clear All Settings Permissions
    Set Suite Variable              ${index}        1
    :FOR  ${index}  IN RANGE  1     15
    \   Clear Settings Permission   ${index}

Clear Only Read
    [Arguments]                     ${row}
    Set Permission                  ${row}          2
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[1]/div/table/tbody/tr[${row}]/td[3]/label/input

Clear Standart
    [Arguments]                     ${row}
    ${checked}                      Get Element Attribute       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[1]/div/table/tbody/tr[${row}]/td[2]/label/input     checked
    Run Keyword If                  "${checked}"=="None"        Double Click    ${row}      ELSE IF     "${checked}"=="true"    Click Element       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[1]/div/table/tbody/tr[${row}]/td[2]/label/input

Clear Settings Only Read
    [Arguments]                     ${row}
    Set Settings Permission         ${row}          2
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/table/tbody/tr[${row}]/td[3]/label/input

Clear Settings Standart
    [Arguments]                     ${row}
    ${checked}                      Get Element Attribute       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/table/tbody/tr[${row}]/td[2]/label/input     checked
    Run Keyword If                  "${checked}"=="None"        Double Settings Click    ${row}      ELSE IF     "${checked}"=="true"    Click Element       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/table/tbody/tr[${row}]/td[2]/label/input

Double Click
    [Arguments]                     ${row}
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[1]/div/table/tbody/tr[${row}]/td[2]/label/input
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[1]/div/table/tbody/tr[${row}]/td[2]/label/input

Double Settings Click
    [Arguments]                     ${row}
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/table/tbody/tr[${row}]/td[2]/label/input
    Click Element                   xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/table/tbody/tr[${row}]/td[2]/label/input

Section Is Present
    [Arguments]                     ${section}
    Run Keyword And Ignore Error    Checking Sections   ${section}
    Run Keyword If                  "${check}"!="true"  Fail    Fail

Section Is Not Present
    [Arguments]                     ${section}
    Run Keyword And Ignore Error    Checking Sections   ${section}
    Run Keyword If                  "${check}"!="false"  Fail    Fail

Checking Sections
    [Arguments]                     ${section}
    Set Global Variable             ${check}            false
    Element Should Be Visible       ${section}
    Set Global Variable             ${check}            true

Number Of Rows
    ${number of row}                Get Element Count           xpath:${table xpath}/tbody/tr
    Set Global Variable             ${number of row}

Number Of Rows G
    ${number of row g}              Get Element Count           xpath:(${table xpath})[2]/tbody/tr
    Set Global Variable             ${number of row g}

Number Of Static Row G
    : FOR   ${counter}              IN RANGE    1   ${number of row g}+1
    \   ${text buffer1 g}           Get Text    xpath:(${table xpath})[2]/tbody/tr[${counter}]/td[1]/div
    \   Exit For Loop If            "Permissions Test"=="${text buffer1 g}"
    Set Global Variable             ${static row g}     ${counter}

Number Of Rows Shiptos
    ${number of row s}              Get Element Count               xpath:${shiptos pane}${table xpath}/tbody/tr
    Set Global Variable             ${number of row s}

Number Of Rows Users
    ${number of row u}              Get Element Count               xpath:${users pane}${table xpath}/tbody/tr
    Set Global Variable             ${number of row u}