*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             ImapLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot
*** Variable ***
${first po number}                  4550
${second po number}                 2393

*** Test Cases ***
Start Check Email
    [Tags]                          IMAP
    Open Mailbox                    host=imap.ukr.net               user=replenishment@ukr.net              password=srx-group      port=993
    Run Keyword And Ignore Error    Mailbox Open

Set Email In Settings
    [Tags]                          
    Goto Customers Notification Emails
    Input Text                      id:replenishmentListEmails_id               ${static email}
    Input Text                      id:activeReplenishmentListEmails_id         ${static email}
    Input Text                      id:discrepancyReplenishmentListEmails_id    ${static email}
    Element Should Be Enabled       css:#customer-settings-pane-notification-emails > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2)
    Click Element                   css:#customer-settings-pane-notification-emails > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2)
    Sleep                           3 second
    Click Element                   id:customer-details-tab-shiptos
    ${buffer po number}             Get Text        xpath:${shiptos pane}${table xpath}/tbody/tr[1]/td[3]/div
    Run Keyword If                  "${buffer po number}"!="${first po number}" and "${buffer po number}"!="${second po number}"    Edit PO Number
    Run Keyword If                  ${buffer po number}==${first po number}     First PO    ELSE IF     ${buffer po number}==${second po number}    Second PO       ELSE    Fail    Exceptional situation! Incorrect PO Number!
    Click Link                      xpath://*[@href="/settings"]
    Goto Notification Emails
    Sleep                           5 second
    Clear Element Text              id:replenishmentListEmails_id
    Press Key                       id:replenishmentListEmails_id           \ue004
    Element Should Be Visible       css:.fa-exclamation-circle > path:nth-child(1)
    Input Text                      id:replenishmentListEmails_id               ${replenishment email}
    Input Text                      id:activeReplenishmentListEmails_id         ${replenishment email}
    Input Text                      id:discrepancyReplenishmentListEmails_id    ${replenishment email}
    Click Element                   css:#enterprise-workflow-pane-notification-emails > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2)
    Sleep                           5 second
    Reload Page
    Goto Notification Emails
    Sleep                           1 second
    Checking Fields

Submit Quote After Settings
    Goto Customer Portal Sub
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[2]/a
    Sleep                           2 second
    Click Element                   xpath:${header xpath}/thead/tr/th[5]
    Click Element                   xpath:${header xpath}/thead/tr/th[5]
    ${current status}               Get Text    xpath:${table xpath}/tbody/tr[1]/td[5]/div
    Run Keyword If                  "${current status}"=="ACTIVE"   If Active   ELSE IF     "${current status}"=="QUOTED"   If Quoted   ELSE    If Other
    Sleep                           5 second
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[1]/a
    ${value}                        Get Element Attribute       id:po_number_field_id       value
    Should Be Equal                 ${current po number}        ${value}
    Run Keyword If                  ${current po number}==${first po number}    Set Second      ELSE IF     ${current po number}==${second po number}    Set First      ELSE    Fail    Exceptional situation! Incorrect PO Number!
    Click Element                   css:.control-button
    Sleep                           5 second

Checking From Settings
    [Tags]                          IMAP
    Run Keyword And Ignore Error    Checking Fail Email
    Run Keyword If                  "${latest}"!="string"   Fail    Letter delivered

Set Email In Warehouse
    Preparation
    Click Link                      xpath://*[@href="/settings"]
    Goto Notification Emails
    Sleep                           3 second
    Input Text                      id:replenishmentListEmails_id               ${static email}
    Input Text                      id:activeReplenishmentListEmails_id         ${static email}
    Input Text                      id:discrepancyReplenishmentListEmails_id    ${static email}
    Click Element                   css:#enterprise-workflow-pane-notification-emails > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2)
    Sleep                           5 second
    Click Link                      xpath://*[@href="/warehouses"]
    Click Element                   xpath:${table xpath}/tbody/tr[1]/td[1]/a
    Click Element                   id:warehouse-details-tab-notification-emails
    Clear Element Text              id:replenishmentListEmails_id
    Press Key                       id:replenishmentListEmails_id           \ue004
    Element Should Be Visible       css:.fa-exclamation-circle > path:nth-child(1)
    Checking Default Fields
    Input Text                      id:replenishmentListEmails_id               ${replenishment email}
    Input Text                      id:activeReplenishmentListEmails_id         ${replenishment email}
    Input Text                      id:discrepancyReplenishmentListEmails_id    ${replenishment email}
    Element Should Be Enabled       css:.control-button
    Click Element                   css:.control-button
    Sleep                           5 second
    Checking Fields

Submit Quote After Warehouse
    Goto Customer Portal Sub
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[2]/a
    ${current status}               Get Text    xpath:${table xpath}/tbody/tr[1]/td[5]/div
    Run Keyword If                  "${current status}"=="ACTIVE"   If Active   ELSE IF     "${current status}"=="QUOTED"   If Quoted   ELSE    If Other
    Sleep                           5 second
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[1]/a
    Click Element                   css:.control-button
    Sleep                           5 second

Checking From Warehouse
    [Tags]                          IMAP
    Run Keyword And Ignore Error    Checking Fail Email
    Run Keyword If                  "${latest}"!="string"   Fail    Letter delivered

Set Email In Customer
    Preparation
    Click Link                      xpath://*[@href="/warehouses"]
    Click Element                   xpath:${table xpath}/tbody/tr[1]/td[1]/a
    Click Element                   id:warehouse-details-tab-notification-emails
    Input Text                      id:replenishmentListEmails_id               ${static email}
    Input Text                      id:activeReplenishmentListEmails_id         ${static email}
    Input Text                      id:discrepancyReplenishmentListEmails_id    ${static email}
    Element Should Be Enabled       css:.control-button
    Click Element                   css:.control-button
    Sleep                           5 second
    Click Link                      xpath://*[@href="/customers"]
    Click Element                   xpath:${table xpath}/tbody/tr[${static row c}]/td[1]/a
    Goto Customers Notification Emails
    Clear Element Text              id:replenishmentListEmails_id
    Press Key                       id:replenishmentListEmails_id           \ue004
    Element Should Be Visible       css:.fa-exclamation-circle > path:nth-child(1)
    Checking Default Fields
    Input Text                      id:replenishmentListEmails_id               ${replenishment email}
    Input Text                      id:activeReplenishmentListEmails_id         ${replenishment email}
    Input Text                      id:discrepancyReplenishmentListEmails_id    ${replenishment email}
    Element Should Be Enabled       css:#customer-settings-pane-notification-emails > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2)
    Click Element                   css:#customer-settings-pane-notification-emails > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2)
    Sleep                           5 second
    Reload Page
    Goto Customers Notification Emails
    Sleep                           1 second
    Checking Fields
    Click Element                   id:customer-details-tab-shiptos
    ${buffer po number}             Get Text        xpath:${shiptos pane}${table xpath}/tbody/tr[1]/td[3]/div
    Should Be Equal As Integers     ${buffer po number}     ${required po number}

Submit Quote After Customer
    Goto Customer Portal Sub
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[2]/a
    ${current status}               Get Text    xpath:${table xpath}/tbody/tr[1]/td[5]/div
    Run Keyword If                  "${current status}"=="ACTIVE"   If Active   ELSE IF     "${current status}"=="QUOTED"   If Quoted   ELSE    If Other
    Sleep                           5 second
    Click Element                   xpath:/html/body/div/div/div/div[1]/div/ul/li[1]/a
    Click Element                   css:.control-button
    Sleep                           5 second

Checking From Customer
    [Tags]                          IMAP
    Checking Email

*** Keywords ***
Preparation
    Goto Customer Menu
    ${SUB HOST}                     Return CSub Link
    Set Global Variable             ${SUB HOST}
    ${SUB EMAIL}                    Return CSub Email
    Set Global Variable             ${SUB EMAIL}

Goto Customer Portal Sub
    Finish Suite
    Run Keyword If                  "${browser}"=="xvfb"            Run Xvfb Sub    ELSE IF     "${browser}"=="chrome"      Run Chrome Sub      ELSE    Run Ff Sub
    Set Selenium Implicit Wait                                      20 second
    Set Selenium Timeout                                            10 second
    Enter Correct Email Sub
    Enter Password
    Correct Submit Login
    Is Select A Shipto
    Click Element                   xpath:/html/body/div/div/div/div/div/div/button[1]
    Click Element                   css:.select-shipto-button
    Is Customer Portal Sub

First PO
    Set Global Variable             ${current po number}    ${first po number}
    Set Global Variable             ${required po number}   ${second po number}

Second PO
    Set Global Variable             ${current po number}    ${second po number}
    Set Global Variable             ${required po number}   ${first po number}

Set Second
    Input Text                      id:po_number_field_id           ${second po number}

Set First
    Input Text                      id:po_number_field_id           ${first po number}

Goto Notification Emails
    Click Element                   id:settings-tab-enterprise-workflow
    Sleep                           1 second
    Click Element                   id:enterprise-workflow-tab-notification-emails
    Sleep                           3 second

Checking Fields
    ${first field}                  Get Element Attribute       id:replenishmentListEmails_id               value
    Should Be Equal As Strings      ${first field}              ${replenishment email}
    ${first field}                  Get Element Attribute       id:activeReplenishmentListEmails_id         value
    Should Be Equal As Strings      ${first field}              ${replenishment email}
    ${first field}                  Get Element Attribute       id:discrepancyReplenishmentListEmails_id    value
    Should Be Equal As Strings      ${first field}              ${replenishment email}

Checking Default Fields
    ${first field}                  Get Element Attribute       id:replenishmentListEmails_default_id               value
    Should Be Equal As Strings      ${first field}              ${static email}
    ${first field}                  Get Element Attribute       id:activeReplenishmentListEmails_default_id         value
    Should Be Equal As Strings      ${first field}              ${static email}
    ${first field}                  Get Element Attribute       id:discrepancyReplenishmentListEmails_default_id    value
    Should Be Equal As Strings      ${first field}              ${static email}

Checking Fail Email
    Set Global Variable             ${latest}                       string
    ${latest}=                      Wait For Email                  sender=srx-group@agilevision.io         timeout=11         status=UNSEEN    subject=Replenishment List Submitted by Static Customer (1138)
    Delete All Emails
    Set Global Variable             ${latest}

Checking Email
    ${latest}=                      Wait For Email                  sender=srx-group@agilevision.io         timeout=120        status=UNSEEN    subject=Replenishment List Submitted by Static Customer (1138)
    ${body}=                        Get Email Body                  ${latest}
    Delete All Emails
    Sleep                           5 second
    Finish Suite
    Sleep                           5 second

If Active
    Element Should Be Disabled      xpath:${table xpath}/tbody/tr[1]/td[8]/button

If Quoted
    Element Should Be Enabled       xpath:${table xpath}/tbody/tr[1]/td[8]/button
    Click Element                   xpath:/html/body/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[8]/button
    Sleep                           3 second

If Other
    ${disabled}                     Get Element Attribute       xpath:${table xpath}/tbody/tr[1]/td[8]/button        disabled
    ${current status}               Get Text    xpath:${table xpath}/tbody/tr[1]/td[5]/div
    Log To Console                  Exceptional situation!\nStatus: ${current status}\nButton disabled: ${disabled}
    Fail                            Fail

Mailbox Open
    ${latest}=                      Wait For Email                  sender=replenish@storeroomlogix.com         timeout=11         status=UNSEEN    subject=Replenishment List Submitted by Static Customer (1138)
    Delete All Emails

Goto Customers Notification Emails
    Click Element                   id:customer-details-tab-settings
    Sleep                           1 second
    Click Element                   id:customer-settings-tab-notification-emails

Edit PO Number
    Click Element                   xpath:${shiptos pane}${table xpath}/tbody/tr[1]${button success}
    Input Text                      id:poNumber_id          ${first po number}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           2 second
    ${buffer po number}             Get Text        xpath:${shiptos pane}${table xpath}/tbody/tr[1]/td[3]/div
    Set Suite Variable              ${buffer po number}

