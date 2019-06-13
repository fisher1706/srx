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
Goto Fees
    Login In Admin Portal
    Click Link                      xpath://*[@href="/fees"]
    Sleep                           5 second

Goto Hardware
    Login In Admin Portal
    Click Link                      xpath://*[@href="/hardware"]
    Sleep                           5 second

Goto Customer Types
    Login In Admin Portal
    Click Link                      xpath://*[@href="/customer-types"]
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

Goto Sidebar Security Groups
    Click Element                   id:sidebar--user_groups
    Sleep                           5 second

Goto Sidebar Settings
    Click Element                   id:sidebar--settings
    Sleep                           5 second

Sign Out New
    Click Element                   id:sidebar-sign_out

Enter Correct Email
    Input Text                      id:email        ${email}

Enter Password
    Input Text                      id:password     ${password}

Correct Submit Login
    Click Element                   ${element login button}

Sign Out
    Click Link                      xpath://*[@href="/sign-out"]

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
    Sleep                           3 second
    Click Element                   xpath:${to portal}
    Sleep                           1 second

Start Customer
    Start Suite Adv                 https://${host_auth}
    Input Text                      id:email                ${email_cust}
    Input Text                      id:password             ${password_cust}
    Click Element                   xpath:${button submit}
    Sleep                           3 second
    Click Element                   xpath:${to portal}
    Sleep                           1 second

Start Permission
    Start Suite Adv                 https://${host_auth}
    Input Text                      id:email                ${email_perm}
    Input Text                      id:password             ${password_perm}
    Click Element                   xpath:${button submit}
    Sleep                           3 second
    Click Element                   xpath:${to portal}
    Sleep                           1 second

Start Suite Adv
    [Arguments]                     ${portal}
    Run Keyword If                  "${browser}"=="xvfb"    Run Xvfb Adv    ${portal}   ELSE IF     "${browser}"=="chrome"      Run Chrome Adv      ${portal}   ELSE    Run Ff Adv      ${portal}
    Set Selenium Implicit Wait      20 second
    Set Selenium Timeout            20 second

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
    ${to click}                     Set Variable    xpath:(${modal dialog}${tab pane})[1]//table/tbody/tr[${row}]/td[${column}+1]${checkbox type}
    ${checked}                      Get Element Attribute   ${to click}     checked
    Run Keyword If                  "${checked}"=="None"    Click Element   ${to click}

Set Settings Permission
    [Arguments]                     ${row}      ${column}
    ${to click}                     Set Variable    xpath:(${modal dialog}${tab pane})[2]//table/tbody/tr[${row}]/td[${column}+1]${checkbox type}
    ${checked}                      Get Element Attribute   ${to click}     checked
    Run Keyword If                  "${checked}"=="None"    Click Element   ${to click}

Clear All Permissions
    ${rows}                         Get Element Count   xpath:(${modal dialog}${tab pane})[1]//table/tbody/tr
    :FOR  ${index}  IN RANGE  1     ${rows}+1
    \   ${to click}                 Set Variable    (${modal dialog}${tab pane})[1]//table/tbody/tr[${index}]${checkbox type}
    \   ${checkboxes}               Get Element Count       xpath:${to click}
    \   Inloop Permission           ${to click}     ${checkboxes}

Inloop Permission
    [Arguments]                     ${to click}     ${checkboxes}
    :FOR    ${index 2}              IN RANGE  1     ${checkboxes}+1
    \   ${checked}                  Get Element Attribute   xpath:(${to click})[${index 2}]     checked
    \   Run Keyword If              "${checked}"=="true"    Click Element   xpath:(${to click})[${index 2}]

Clear All Settings Permissions
    ${rows}                         Get Element Count   xpath:(${modal dialog}${tab pane})[2]//table/tbody/tr
    :FOR  ${index}  IN RANGE  1     ${rows}+1
    \   ${to click}                 Set Variable    (${modal dialog}${tab pane})[2]//table/tbody/tr[${index}]${checkbox type}
    \   ${checkboxes}               Get Element Count       xpath:${to click}
    \   Inloop Permission           ${to click}     ${checkboxes}

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
    ${current}                      Get Text        xpath:${select}/div/div
    Return From Keyword If          "${current}"=="${item}"
    Click Element                   xpath:${select}
    ${count}                        Get Element Count       xpath:${select}/../div[2]/div/div
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   ${text buffer sub}          Get Text                                xpath:${select}/../div[2]/div/div[${index}]
    \   Run Keyword If              "${text buffer sub}"=="${item}"         Select Element      ${select}   ${index}

Choose First From Select Box
    [Arguments]                     ${select}
    Click Element                   xpath:${select}
    Click Element                   xpath:${select}/../div[2]/div/div[1]

Choose Last From Select Box
    [Arguments]                     ${select}
    Click Element                   xpath:${select}
    ${count}                        Get Element Count       xpath:${select}/../div[2]/div/div
    Click Element                   xpath:${select}/../div[2]/div/div[${count}]

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
    Sleep                           2 second

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
    Sleep                           2 second

Get RFID URL
    Return From Keyword             https://${RFID_SN}:${RFID_SN}@api-${environment}.storeroomlogix.com/api/webhook/events/rfid

Get Locker URL
    Return From Keyword             https://${LOCKER_SN}:${LOCKER_SN}@api-${environment}.storeroomlogix.com/api/webhook/events/locker

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
    ${content}                      Get Text    xpath:((${react table raw})[2]${react table column})[${column}]
    Return From Keyword             ${content}

Expanded AL Element Should Be
    [Arguments]                     ${column}                   ${text}
    ${content}                      Check Last Expanded AL      ${column}
    Should Be Equal As Strings      ${content}                  ${text}

Select Location At Rfid Menu
    [Arguments]                     ${shipto}       ${sku}
    Click Element                   xpath:(${selector shipto})[1]/div
    ${count}                        Get Element Count       xpath:(${selector shipto})[1]/div[1]/div[2]/div[1]/div
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   ${text buffer sub}          Get Text                                xpath:(${selector shipto})[1]/div[1]/div[2]/div[1]/div[${index}]
    \   Run Keyword If              "${text buffer sub}"=="${shipto}"       Select Element      (${selector shipto})[1]   ${index}
    Sleep                           2 second
    Click Element                   xpath:(${selector shipto})[2]/div
    ${count}                        Get Element Count       xpath:(${selector shipto})[2]/div[1]/div[2]/div[1]/div
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   ${text buffer sub}          Get Text                                xpath:(${selector shipto})[2]/div[1]/div[2]/div[1]/div[${index}]
    \   Run Keyword If              "${text buffer sub}"=="${sku}"          Select Element      (${selector shipto})[2]   ${index}

Select Element
    [Arguments]                     ${select}   ${index}
    Click Element                   xpath:${select}/div[1]/div[2]/div[1]/div[${index}]
    Exit For Loop

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
    Click Element                   xpath:${pagination bottom}/div/div/button[2]
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
    Sleep                           2 second

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
    Sleep                           2 second

React Last
    ${count}                        Get Element Count       xpath:${pagination bottom}/div/div[2]/*
    ${count}                        Evaluate    ${count}-1
    Click Element                   xpath:${pagination bottom}/div/div[2]/button[${count}]

React First
    Click Element                   xpath:${pagination bottom}/div/div[2]/button[2]

Generate Random Name U
    [Arguments]                     ${number}=18
    ${buffer1}                      Generate Random String                              ${number}       [LETTERS]
    ${random name u}                Convert To Uppercase                                ${buffer1}
    Set Suite Variable              ${random name u}
    Return From Keyword             ${random name u}

Generate Random Name L
    [Arguments]                     ${number}=18
    ${buffer1}                      Generate Random String                              ${number}       [LETTERS]
    ${random name l}                Convert To Lowercase                                ${buffer1}
    Set Suite Variable              ${random name l}
    Return From Keyword             ${random name l}

Input By Name
    [Arguments]                     ${name}     ${text}
    Input Text                      xpath://input[contains(@name, '${name}')]           ${text}

Get Selected Text
    [Arguments]                     ${item}
    ${text}                         Get Text    xpath:${item}/../../../div[1]
    Return From Keyword             ${text}

Select First
    [Arguments]                     ${item}
    Press Key                       xpath:${item}       \ue015
    Press Key                       xpath:${item}       \ue015
    Press Key                       xpath:${item}       \ue007
    ${text}                         Get Selected Text   ${item}
    Return From Keyword             ${text}

Dialog Should Be About
    [Arguments]                     ${text}
    ${buffer}                       Get Text    xpath:${close dialog}/../..//b
    Run Keyword If                  "${buffer}"!="${text}"      Fail    Incorrect value in confirmation dialog: ${buffer}

Select From Dropdown
    [Arguments]                     ${item}     ${text}
    Press Key                       xpath:${item}       \ue015
    ${count}                        Get Element Count       xpath:${item}/../../../../../div[2]/div[1]/div
    : FOR   ${index}    IN RANGE    1       ${count}+2
    \   ${buffer}                   Get Text        xpath:${item}/../../../../../div[2]/div[1]/div[${index}]
    \   Run Keyword If              "${buffer}"=="${text}"         Select Dropdown Element      ${index}    ${item}

Select Dropdown Element
    [Arguments]                     ${index}    ${item}
    Click Element                   xpath:${item}/../../../../../div[2]/div[1]/div[${index}]
    Exit For Loop

Get React Row By Text
    [Arguments]                     ${column}   ${text}
    ${number}                       Get Element Count       xpath:${react table raw}
    : FOR   ${index}    IN RANGE    1   ${number}+1
    \   ${text buffer}              Get Text    xpath:((${react table raw})[${index}]${react table column})[${column}]
    \   Exit For Loop If            "${text}"=="${text buffer}"
    Return From Keyword             ${index}

Filter Add
    [Arguments]                     ${dialog index}     ${table index}      ${value}
    Click Element                   xpath:${button filter}
    Click Element                   xpath:(${menu}${menu item})[${dialog index}]
    Input Text                      xpath:${filter type}/div/div/input      ${value}
    Sleep                           5 second
    ${count}                        Get Element Count       xpath:${react table raw}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   Element Text Should Be      xpath:((${react table raw})[${index}]${react table column})[${table index}]     ${value}
    Click Element                   xpath:${filter type}/button
    Sleep                           2 second

Filter Add For Select Box
    [Arguments]                     ${dialog index}     ${table index}      ${value}
    Click Element                   xpath:${button filter}
    Click Element                   xpath:(${menu}${menu item})[${dialog index}]
    Sleep                           2 second
    Click Element                   xpath:${filter type}/div/div
    ${count}                        Get Element Count       xpath:${listbox}/*
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   ${buffer}                   Get Text                xpath:${listbox}/li[${index}]
    \   Run Keyword If              "${buffer}"=="${value}"     Select Filter Element   ${index}
    Sleep                           3 second
    ${count2}                        Get Element Count       xpath:${react table raw}
    : FOR   ${index}    IN RANGE    1       ${count2}+1
    \   Element Text Should Be      xpath:((${react table raw})[${index}]${react table column})[${table index}]     ${value}
    Click Element                   xpath:${filter type}/button
    Sleep                           2 second

Select Filter Element
    [Arguments]                     ${index}
    Click Element                   xpath:${listbox}/li[${index}]
    Exit For Loop

Sort React
    [Arguments]                     ${column}
    Click Element                   xpath:(${react header})[${column}+1]
    Sleep                           2 second
    ${text buffer1up}               Get Text                    xpath:(${react table column})[${column}]
    ${number of row}                Get Element Count           xpath:${react table raw}
    ${text buffer1down}             Get Text                    xpath:((${react table raw})[${number of row}]${react table column})[${column}]
    Click Element                   xpath:(${react header})[${column}+1]
    Sleep                           2 second
    ${text buffer2down}             Get Text                    xpath:((${react table raw})[${number of row}]${react table column})[${column}]
    ${text buffer2up}               Get Text                    xpath:(${react table column})[${column}]
    Run Keyword If                  "${text buffer1up}"!="${text buffer2down}"          Log To Console      Sorting ${column} is failed
    Run Keyword If                  "${text buffer1down}"!="${text buffer2up}"          Log To Console      Sorting ${column} is failed

Get React Rows Count
    [Arguments]                     ${table}
    ${number}                       Get Element Count           xpath:${react table}${react table raw}
    Return From Keyword If          ${number}!=1                ${number}
    ${columns}                      Get Element Count           xpath:${react table}${react table raw}${react table column}
    Return From Keyword If          ${columns}>1                1
    Return From Keyword If          ${columns}<=1               0

Goto Locations
    Go To                           https://distributor.${environment}.storeroomlogix.com/customers/${customer_id}/shiptos/${shipto_id}#vmi-list
    Sleep                           1 second

Goto Usage History
    Go To                           https://distributor.${environment}.storeroomlogix.com/customers/${customer_id}#usage-history
    Sleep                           1 second

Goto Customer Users
    Go To                           https://distributor.${environment}.storeroomlogix.com/customers/${customer_id}#users
    Sleep                           1 second

Is Full Table
    [Arguments]                     ${number of row}
    Run Keyword If                  ${number of row} >= 50        React Last

Simple Table Comparing
    [Arguments]                     ${head}     ${body}     ${raw}      ${table}=${table xpath}     ${header}=${header xpath}
    ${count}                        Get Element Count       xpath:${header}/thead/tr/th
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   ${buffer}       Get Text    xpath:${header}/thead/tr/th[${index}]
    \   Set Suite Variable          ${column}   ${index}
    \   Exit For Loop If            "${buffer}"=="${head}"
    \   Run Keyword If              ${index}==${count}      Fail    There is no such header
    Element Text Should Be          xpath:${table}/tbody/tr[${raw}]/td[${column}]     ${body}

Set Order Status Settings
    Go To                           https://distributor.${environment}.storeroomlogix.com/settings
    Sleep                           1 second
    Click Element                   id:settings-tab-erp-integration
    Sleep                           1 second
    Click Element                   id:erp-integration-tab-transaction-status
    Sleep                           1 second
    Click Element                   xpath:${order staus pane}${button primary}
    Sleep                           4 second
    ${check1}                       Get Element Attribute           css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)       checked
    ${check2}                       Get Element Attribute           css:div.checkbox:nth-child(2) > label:nth-child(1) > input:nth-child(1)       checked
    Log To Console                  ${check1}
    Log To Console                  ${check2}
    Run Keyword If                  "${check1}"=="None"             Click Element       css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Run Keyword If                  "${check2}"=="None"             Click Element       css:div.checkbox:nth-child(2) > label:nth-child(1) > input:nth-child(1)
    Click Element                   xpath:${order staus pane}${button primary}
    Sleep                           3 second

Simple Table Editing
    [Arguments]                     ${head}     ${body}     ${raw}      ${table}=${table xpath}     ${header}=${header xpath}
    ${count}                        Get Element Count       xpath:${header}/thead/tr/th
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   ${buffer}       Get Text    xpath:${header}/thead/tr/th[${index}]
    \   Set Suite Variable          ${column}   ${index}
    \   Exit For Loop If            "${buffer}"=="${head}"
    \   Run Keyword If              ${index}==${count}      Fail    There is no such header
    Click Element                   xpath:${table}/tbody/tr[${raw}]/td[${column}]
    Input Text                      xpath:${table}/tbody/tr[${raw}]/td[${column}]/div/div/input     ${body}
    Press Key                       xpath:${table}/tbody/tr[${raw}]/td[${column}]/div/div/input     \ue007

Select Shipto
    [Arguments]                     ${name}
    ${count}                        Get Element Count       xpath:${shipto}
    : FOR   ${index}    IN RANGE    1       ${count}+1
    \   ${buffer}       Get Text    xpath:(${shipto})[${index}]
    \   Run Keyword If      "${buffer}"=="${name}"      Shipto Selection    ${index}

Shipto Selection
    [Arguments]                     ${index}
    Click Element                   xpath:(${shipto})[${index}]
    Exit For Loop