*** Settings ***
Library                             XvfbRobot
Resource                            path.robot
Resource                            ${set}

*** Variables ***
${X}                                1920
${Y}                                1080
${correct wrong email}              example@example.com
${incorrect email}                  example.agilevision.io
${incorrect password}               sxr-group1

*** Keywords ***
Login In Distributor Portal
    Start Suite
    Enter Correct Email
    Enter Password
    Correct Submit Login
    Section Is Present              id:sidebar-sign_out
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

Goto Activity Log
    Start Distributor
    Click Link                      xpath://*[@href="/activity-feed"]
    Sleep                           5 second

Goto RFID
    Start Distributor
    Click Link                      xpath://*[@href="/rfid-view"]
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
    Click Link                      xpath://*[@href="/order-status"]
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

Goto Hardware
    Login In Admin Portal
    Click Link                      xpath://*[@href="/hardware"]
    Sleep                           5 second

Goto Catalog
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/catalog"]
    Sleep                           5 second

Goto Pricing
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/settings"]
    Click Element                   id:settings-tab-erp-integration
    Sleep                           1 second
    Click Element                   id:erp-integration-tab-pricing-integration
    Sleep                           3 second
    Click Element                   xpath:(${pricing integrations}${radio button})[2]
    Click Element                   xpath:${pricing integrations}${control button}
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
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/distributors"]
    Open Full Table
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

Goto Sidebar Users  
    Click Element                   id:sidebar-users
    Sleep                           5 second

Goto Sidebar Warehouses
    Click Element                   id:sidebar-warehouses
    Sleep                           5 second

Goto Sidebar Customers
    Click Element                   id:sidebar-customers
    Sleep                           5 second

Goto Sidebar Catalog
    Click Element                   id:sidebar-catalog
    Sleep                           5 second

Goto Sidebar Usage History
    Click Element                   id:sidebar-usage_history
    Sleep                           5 second

Goto Sidebar Pricing
    Click Element                   id:sidebar-pricing
    Sleep                           5 second

Goto Sidebar Order Status
    Click Element                   id:sidebar-transactions
    Sleep                           5 second

Goto Sidebar Activity Feed
    Click Element                   id:sidebar-activity_feed
    Sleep                           5 second

Goto Sidebar Reports
    Click Element                   id:sidebar-reports
    Sleep                           5 second

Goto Sidebar RFID
    Click Element                   id:sidebar-rfid
    Sleep                           5 second

Goto Sidebar Locations
    Click Element                   id:sidebar-locations
    Sleep                           5 second

Goto Sidebar Security Groups
    Click Element                   id:sidebar--user_groups
    Sleep                           5 second

Goto Sidebar Settings
    Click Element                   id:sidebar--settings
    Sleep                           5 second

Sign Out New
    Click Element                   id:sidebar-sign_out

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

Enter Correct Email
    Input Text                      id:email        ${email}

Enter Password
    Input Text                      id:password     ${password}

Correct Submit Login
    Click Element                   ${element login button}

Sign Out
    Click Link                      xpath://*[@href="/sign-out"]

Start Suite
    Set Suite Variable              ${LOGIN URL}    https://${HOST}/sign-in
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

Start Admin
    Start Suite Adv                 https://${host_adm}/sign-in
    Input Text                      id:email                ${email_adm}
    Input Text                      id:password             ${password_adm}
    Click Element                   xpath:${button submit}

Start Distributor
    Start Suite Adv                 https://${host_auth}
    Input Text                      id:email                ${email_dist}
    Input Text                      id:password             ${password_dist}
    Click Element                   xpath:${button submit}
    Sleep                           4 second
    Click Element                   xpath:${to portal}
    Sleep                           1 second

Start Customer
    Start Suite Adv                 https://${host_auth}
    Input Text                      id:email                ${email_cust}
    Input Text                      id:password             ${password_cust}
    Click Element                   xpath:${button submit}
    Sleep                           4 second
    Click Element                   xpath:${to portal}
    Sleep                           1 second

Start Permission
    Start Suite Adv                 https://${host_auth}
    Input Text                      id:email                ${email_perm}
    Input Text                      id:password             ${password_perm}
    Click Element                   xpath:${button submit}
    Sleep                           4 second
    Click Element                   xpath:${to portal}
    Sleep                           1 second

Start Suite Adv
    [Arguments]                     ${portal}
    Run Keyword If                  "${browser}"=="xvfb"    Run Xvfb Adv    ${portal}   ELSE IF     "${browser}"=="chrome"      Run Chrome Adv      ${portal}   ELSE    Run Ff Adv      ${portal}
    Set Selenium Implicit Wait      20 second
    Set Selenium Timeout            10 second

Run Xvfb Adv
    [Arguments]                     ${portal}
    Start Virtual Display           ${X}                    ${Y}
    Open Browser                    ${portal}
    Set Window Size                 ${X}                    ${Y}

Run Chrome Adv
    [Arguments]                     ${portal}
    Open Browser                    ${portal}               chrome

Run Ff Adv
    [Arguments]                     ${portal}
    Open Browser                    ${portal}               ff

Finish Suite
    Close All Browsers

Is Customer Portal
    Element Text Should Be          xpath:/html/body/div/div/div/div[1]/div/div/div/div[2]/p[2]     ${email_cust}

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
    Element Should Be Enabled      xpath://label[contains(@for, 'password')]

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

Sort Column
    [Arguments]                     ${column}       ${count}
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer1up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    ${text buffer1down}             Get Text                    xpath:${table xpath}/tbody/tr[${count}]/td[${column}]
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer2up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    ${text buffer2down}             Get Text                    xpath:${table xpath}/tbody/tr[${count}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]

Sort Column With Last Page
    [Arguments]                     ${column}
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer1up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   xpath:${last page}
    ${count}                        Get Rows Count              ${table xpath}
    ${text buffer1down}             Get Text                    xpath:${table xpath}/tbody/tr[${count}]/td[${column}]
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]
    ${text buffer2up}               Get Text                    xpath:${table xpath}/tbody/tr[1]/td[${column}]
    Click Element                   xpath:${last page}
    ${text buffer2down}             Get Text                    xpath:${table xpath}/tbody/tr[${count}]/td[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed
    Click Element                   xpath:${header xpath}/thead/tr/th[${column}]

Number Of Rows C
    ${number of row c}              Get Element Count   xpath:${table xpath}/tbody/tr
    Set Suite Variable              ${number of row c}

Number Of Static Row C
    : FOR   ${counter c}            IN RANGE    1   ${number of row c}+1
    \   ${text buffer1 c}           Get Text    xpath:${table xpath}/tbody/tr[${counter c}]/td[1]/a
    \   Exit For Loop If            "Static Customer"=="${text buffer1 c}"
    Set Suite Variable              ${static row c}     ${counter c}

Number Of Rows E
    ${number of row e}              Get Element Count   xpath:${table xpath}/tbody/tr
    Set Suite Variable              ${number of row e}

Number Of Static Row E
    : FOR   ${counter e}            IN RANGE    1   ${number of row e}+1
    \   ${text buffer1 e}           Get Text    xpath:${table xpath}/tbody/tr[${counter e}]/td[1]/a
    \   Exit For Loop If            "${static name}"=="${text buffer1 e}"
    Set Suite Variable              ${static row e}     ${counter e}

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

Return Permissions Email
    Return From Keyword If          "${HOST}"=="distributor-dev.storeroomlogix.com"         srx-group+dev-permissions@agilevision.io
    Return From Keyword If          "${HOST}"=="distributor-staging.storeroomlogix.com"     srx-group+staging-permissions@agilevision.io
    Return From Keyword If          "${HOST}"=="admin-dev.storeroomlogix.com"               srx-group+dev-permissions@agilevision.io
    Return From Keyword If          "${HOST}"=="admin-staging.storeroomlogix.com"           srx-group+staging-permissions@agilevision.io

Get Api Key
    Return From Keyword If          "${HOST}"=="distributor-dev.storeroomlogix.com"         m4DAfPuRurdzlsVrlen2
    Return From Keyword If          "${HOST}"=="distributor-staging.storeroomlogix.com"     Ub6lJbV0UZDINvctedHm

Get RFID SN
    Get Api Key
    Return From Keyword If          "${HOST}"=="distributor-dev.storeroomlogix.com"         RFID230820106808
    Return From Keyword If          "${HOST}"=="distributor-staging.storeroomlogix.com"     

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
    Run Keyword If                  ${row}==5       Clear Only Read             ${row}
    Run Keyword If                  ${row}==11      Clear Only Read             ${row}
    Run Keyword If                  ${row}==16      Clear Only Read             ${row}
    Run Keyword If                  ${row}!=5 and ${row}!=11 and ${row}!=16     Clear Standart      ${row}

Clear Settings Permission
    [Arguments]                     ${row}
    Run Keyword If                  ${row}==14    Clear Settings Only Read      ${row}
    Run Keyword If                  ${row}==15    Clear Settings Only Read      ${row}
    Run Keyword If                  ${row}!=15 and ${row}!=14                   Clear Settings Standart     ${row}

Clear All Permissions
    Set Suite Variable              ${index}        1
    :FOR  ${index}  IN RANGE  1     18
    \   Clear Permission            ${index}

Clear All Settings Permissions
    Set Suite Variable              ${index}        1
    :FOR  ${index}  IN RANGE  1     17
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
    Set Suite Variable              ${check}            false
    Element Should Be Visible       ${section}
    Set Suite Variable              ${check}            true

Is Present
    [Arguments]                     ${section}
    Run Keyword And Ignore Error    Checking Sections   ${section}

Number Of Rows
    ${number of row}                Get Element Count           xpath:${table xpath}/tbody/tr
    Set Suite Variable              ${number of row}

Number Of Rows G
    ${number of row g}              Get Element Count           xpath:(${table xpath})[2]/tbody/tr
    Set Suite Variable              ${number of row g}

Number Of Static Row G
    : FOR   ${counter}              IN RANGE    1   ${number of row g}+1
    \   ${text buffer1 g}           Get Text    xpath:(${table xpath})[2]/tbody/tr[${counter}]/td[1]/div
    \   Exit For Loop If            "Permissions Test"=="${text buffer1 g}"
    Set Suite Variable              ${static row g}     ${counter}

Number Of Rows Shiptos
    ${number of row s}              Get Element Count               xpath:${shiptos pane}${table xpath}/tbody/tr
    Set Suite Variable              ${number of row s}

Number Of Rows Users
    ${number of row u}              Get Element Count               xpath:${users pane}${table xpath}/tbody/tr
    Set Suite Variable              ${number of row u}

Go Down Selector
    [Arguments]                     ${select}       ${item}
    Click Element                   xpath:${select}
    Press Key                       xpath:${select}/div[1]/div[2]           \ue015
    Sleep                           1 second
    Press Key                       xpath:${select}/div[1]/div[2]           \ue007
    ${text buffer sub}              Get Text                                xpath:${select}/div[1]/div[1]/span
    Sleep                           2 second
    Run Keyword If                  "${text buffer sub}"!="${item}"         Go Down Selector    ${select}       ${item}

Get Rows Count
    [Arguments]                     ${table}
    ${number}                       Get Element Count           xpath:${table}/tbody/tr
    Return From Keyword If          ${number}!=1                ${number}
    ${columns}                      Get Element Count           xpath:${table}/tbody/tr/td
    Return From Keyword If          ${columns}>1                1
    Return From Keyword If          ${columns}<=1               0

Get Row By Text
    [Arguments]                     ${table}    ${column}   ${text}
    ${number}                       Get Element Count           xpath:${table}/tbody/tr
    : FOR   ${index}    IN RANGE    1   ${number}+1
    \   ${text buffer}              Get Text    xpath:${table xpath}/tbody/tr[${index}]/td[${column}]
    \   Exit For Loop If            "${text}"=="${text buffer}"
    Return From Keyword             ${index}

Choose From Select Box
    [Arguments]                     ${select}       ${item}
    Click Element                   xpath:${select}
    ${count}                        Get Element Count       xpath:${select}/..${select menu outer}/div/div
    : FOR   ${index}    IN RANGE    1       ${count}+2
    \   Press Key                   xpath:${select}/div[1]/div[2]           \ue015
    \   ${text buffer sub}          Get Text                                xpath:${select}/..${select menu outer}${select is focused}
    \   Run Keyword If              "${text buffer sub}"=="${item}"         Select Element      ${select}

Select Element
    [Arguments]                     ${select}
    Press Key                       xpath:${select}/div[1]/div[2]           \ue007
    Exit For Loop

Open Full Table
    Sleep                           1 second
    Execute Javascript              for(var i = 0 ; i<document.getElementsByClassName("dropdown-menu").length; i++){ if((document.getElementsByClassName("dropdown-menu"))[i].attributes["aria-labelledby"]){ (document.getElementsByClassName("dropdown-menu"))[i].setAttribute("class","dropdown-menu open show") }}
    Sleep                           1 second
    Click Element                   xpath:(${dropdown menu item})[4]
    Sleep                           1 second

Open Minimum Table
    Sleep                           1 second
    Execute Javascript              for(var i = 0 ; i<document.getElementsByClassName("dropdown-menu").length; i++){ if((document.getElementsByClassName("dropdown-menu"))[i].attributes["aria-labelledby"]){ (document.getElementsByClassName("dropdown-menu"))[i].setAttribute("class","dropdown-menu open show") }}
    Sleep                           1 second
    Click Element                   xpath:(${dropdown menu item})[1]
    Sleep                           1 second

Filter Field
    [Arguments]                     ${dialog index}     ${table index}      ${value}
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[${dialog index}]         ${value}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${table xpath}/tbody/tr[${index}]/td[${table index}]      ${value}
    Click Element                   xpath:${button default}
    Sleep                           3 second

Filter Select Box
    [Arguments]                     ${dialog index}     ${table index}      ${value}
    Click Element                   xpath:${button right margin}
    Choose From Select Box          (${modal dialog}${select control})[${dialog index}]             ${value}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Rows Count      ${table xpath}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:${table xpath}/tbody/tr[${index}]/td[${table index}]      ${value}
    Click Element                   xpath:${button default}
    Sleep                           3 second

Get RFID URL
    Return From Keyword             https://${RFID_SN}:${RFID_SN}@api-${environment}.storeroomlogix.com/api/webhook/events/rfid

Get Locker URL
    Return From Keyword             https://${API_key}:${API_key}@api-${environment}.storeroomlogix.com/api/webhook/events/locker

Get Manifest URL
    Return From Keyword             https://api-${environment}.storeroomlogix.com/distributor-portal/distributor/manifest

Get Putaway URL
    Return From Keyword             https://api-${environment}.storeroomlogix.com/distributor-portal/distributor/putaway

Check Last AL
    [Arguments]                     ${column}
    ${content}                      Get Text    xpath:(${react table raw}${react table column})[${column}]
    Return From Keyword             ${content}

Last AL Element Should Be
    [Arguments]                     ${column}       ${text}
    ${content}                      Check Last AL   ${column}
    Should Be Equal As Strings      ${content}      ${text}

Expand Last AL
    Click Element                   xpath:(${react table raw}${react table column})[1]

Check Last Expanded AL
    [Arguments]                     ${column}
    ${content}                      Get Text    xpath:(${expanded react table}${react table column})[${column}]
    Return From Keyword             ${content}

Expanded AL Element Should Be
    [Arguments]                     ${column}                   ${text}
    ${content}                      Check Last Expanded AL      ${column}
    Should Be Equal As Strings      ${content}                  ${text}

Select Location At Rfid Menu
    [Arguments]                     ${shipto}       ${sku}
    Input Text                      xpath:(${srx select})[1]/div/div/div/div[2]/div/input       ${shipto}
    Press Key                       xpath:(${srx select})[1]/div/div/div/div/div/input          \ue007
    Sleep                           1 second
    Input Text                      xpath:(${srx select})[2]/div/div/div/div[2]/div/input       ${sku}
    Press Key                       xpath:(${srx select})[2]/div/div/div/div/div/input          \ue007

Sorting React With Last Page
    [Arguments]                     ${column}
    Click Element                   xpath:(${react header})[${column}+1]
    Sleep                           2 second
    ${text buffer1up}               Get Text                    xpath:(${react table column})[${column}]
    React Last
    Sleep                           2 second
    ${number of row}                Get Element Count           xpath:${react table raw}
    ${text buffer1down}             Get Text                    xpath:((${react table raw})[${number of row}]${react table column})[${column}]
    Click Element                   xpath:(${react header})[${column}+1]
    Sleep                           2 second
    ${text buffer2down}             Get Text                    xpath:((${react table raw})[${number of row}]${react table column})[${column}]
    Click Element                   xpath:(${page link})[2]
    Sleep                           2 second
    ${text buffer2up}               Get Text                    xpath:(${react table column})[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed

Filter React Field
    [Arguments]                     ${dialog index}     ${table index}      ${value}
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${modal dialog}${form control})[${dialog index}]         ${value}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Element Count       xpath:${react table raw}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:((${react table raw})[${index}]${react table column})[${table index}]   ${value}
    Click Element                   xpath:${button default}
    Sleep                           3 second

Filter React Select Box
    [Arguments]                     ${dialog index}     ${table index}      ${value}
    Click Element                   xpath:${button right margin}
    Choose From Select Box          (${modal dialog}${select control})[${dialog index}]             ${value}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           2 second
    ${count}                        Get Element Count       xpath:${react table raw}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:((${react table raw})[${index}]${react table column})[${table index}]   ${value}
    Click Element                   xpath:${button default}
    Sleep                           3 second

React Last
    ${count}                        Get Element Count       xpath:${page link}
    ${count}                        Evaluate    ${count}-1
    Click Element                   xpath:(${page link})[${count}]

Generate Random Name U
    ${buffer1}                      Generate Random String                              18          [LETTERS]
    ${random name u}                Convert To Uppercase                                ${buffer1}
    Set Suite Variable              ${random name u}
    Return From Keyword             ${random name u}

Generate Random Name L
    ${buffer1}                      Generate Random String                              18          [LETTERS]
    ${random name l}                Convert To Lowercase                                ${buffer1}
    Set Suite Variable              ${random name l}
    Return From Keyword             ${random name l}