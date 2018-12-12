*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***
${customer shiptos}                 100000-150000
${edit customer shiptos}            150001-200000
${monthly fee}                      19
${edit monthly fee}                 27
${number of buttons}                100000-150000
${monthly fee per button}           3

*** Test Cases ***
Invalid Add New Shipto Fee
    [Tags]                          InvalidAddNewSRXCloudFee                SRX
    Click Element                   css:#uncontrolled-tab-example-tab-3
    Is SRXCloud
    Click Element                   css:#uncontrolled-tab-example-pane-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Is Add SRXCloud Fee
    Click Element                   css:.close
    Is SRXCloud
    Click Element                   css:#uncontrolled-tab-example-pane-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Press Key                       id:numOfShiptos_id                      \ue004
    Element Should Be Visible       css:.fa-exclamation-circle > path:nth-child(1)
    Press Key                       id:value_id                             \ue004
     Element Should Be Visible      css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Input Text                      id:numOfShiptos_id                      2345
    Click Element                   id:value_id
    Element Should Be Visible       css:.fa-exclamation-circle > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Is SRXCloud

Valid Add New Shipto Fee
    [Tags]                          ValidAddNewSRXCloudFee                  SRX
    Click Element                   css:#uncontrolled-tab-example-tab-3
    Is SRXCloud
    Click Element                   css:#uncontrolled-tab-example-pane-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Is Add SRXCloud Fee
    Input Text                      id:numOfShiptos_id                      ${customer shiptos}
    Input Text                      id:value_id                             ${monthly fee}
    Click Element                   css:.modal-dialog-ok-button

Checking New Shipto Fee
    [Tags]                          SRX
    Sleep                           5 second
    Click Element                   css:#uncontrolled-tab-example-pane-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > button:nth-child(1)
    Click Element                   css:#uncontrolled-tab-example-pane-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > ul:nth-child(2) > li:nth-child(4) > a:nth-child(1)
    Sleep                           5 second
    Element Text Should Be          ${shiptos cell}                         ${customer shiptos}
    Element Text Should Be          ${fee cell}                             $${monthly fee}

Delete Shipto Fee
    [Tags]                          SRX
    Click Element                   css:#uncontrolled-tab-example-tab-3
    Is SRXCloud
    Click Element                   ${remove fee button}
    Is Delete SRXCloud Fee
    Click Element                   css:.close
    Is SRXCloud
    Click Element                   ${remove fee button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Is SRXCloud
    Click Element                   ${remove fee button}
    Element Text Should Be          css:td.text-center:nth-child(1)         ${customer shiptos}
    Element Text Should Be          css:td.text-center:nth-child(2)         $${monthly fee}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           1 second

Invalid Add New Button Fee
    [Tags]                          Button
    Click Element                   css:#uncontrolled-tab-example-tab-2
    Is Button Monthly Fee
    Click Element                   css:#uncontrolled-tab-example-pane-2 > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Is Add Button Fee
    Click Element                   css:.close
    Is Button Monthly Fee  
    Click Element                   css:#uncontrolled-tab-example-pane-2 > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Press Key                       id:numOfButtons_id                      \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(1) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Press Key                       id:value_id                             \ue004
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Input Text                      id:numOfButtons_id                      2345
    Click Element                   id:value_id
    Element Should Be Visible       css:div.item-form-field:nth-child(2) > div:nth-child(2) > span:nth-child(2) > svg:nth-child(1) > path:nth-child(1)
    Click Element                   css:.modal-dialog-cancel-button
    Is Button Monthly Fee

Valid Add New Button Fee
    [Tags]                          Button
    Click Element                   css:#uncontrolled-tab-example-tab-2
    Is Button Monthly Fee
    Click Element                   css:#uncontrolled-tab-example-pane-2 > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)
    Is Add Button Fee
    Input Text                      id:numOfButtons_id                      ${number of buttons}
    Input Text                      id:value_id                             ${monthly fee per button}
    Click Element                   css:.modal-dialog-ok-button

Checking New Button Fee
    [Tags]                          Button
    Sleep                           5 second
    Click Element                   css:#uncontrolled-tab-example-pane-2 > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > button:nth-child(1)
    Click Element                   css:#uncontrolled-tab-example-pane-2 > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > ul:nth-child(2) > li:nth-child(4) > a:nth-child(1)
    Sleep                           5 second
    Element Text Should Be          ${number of buttons cell}               ${number of buttons}
    Element Text Should Be          ${monthly fee cell}                     $${monthly fee per button}

Delete Button Monthly Fee
    [Tags]                          Button
    Click Element                   css:#uncontrolled-tab-example-tab-2
    Is Button Monthly Fee
    Click Element                   ${remove monthly fee button}
    Is Delete Button Fee
    Click Element                   css:.close
    Is Button Monthly Fee
    Click Element                   ${remove monthly fee button}
    Click Element                   css:.modal-footer > button:nth-child(1)
    Is Button Monthly Fee
    Click Element                   ${remove monthly fee button}
    Element Text Should Be          css:td.text-center:nth-child(1)         ${number of buttons}
    Element Text Should Be          css:td.text-center:nth-child(2)         $${monthly fee per button}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           1 second

*** Keywords ***
Preparation
    Goto Fees
    Click Element                   css:#uncontrolled-tab-example-tab-3
    Sleep                           4 second
    Click Element                   css:#uncontrolled-tab-example-pane-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > button:nth-child(1)
    Click Element                   css:#uncontrolled-tab-example-pane-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > ul:nth-child(2) > li:nth-child(4) > a:nth-child(1)
    Sleep                           4 second
    Number Of Rows SRX
    Click Element                   css:#uncontrolled-tab-example-tab-2
    Sleep                           4 second
    Click Element                   css:#uncontrolled-tab-example-pane-2 > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > button:nth-child(1)
    Click Element                   css:#uncontrolled-tab-example-pane-2 > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > ul:nth-child(2) > li:nth-child(4) > a:nth-child(1)
    Sleep                           4 second
    Number Of Rows Button
    ${srx row number}=              Evaluate                                ${srx row}+1
    ${button row number}=           Evaluate                                ${button row}+1
    Set Global Variable             ${srx row number}
    Set Global Variable             ${button row number}
    Set Global Variable             ${shiptos cell}                         xpath:${monthly pane}${table xpath}/tbody/tr[${srx row number}]/td[1]/div
    Set Global Variable             ${fee cell}                             xpath:${monthly pane}${table xpath}/tbody/tr[${srx row number}]/td[2]/div
    Set Global Variable             ${remove fee button}                    xpath:${monthly pane}${table xpath}/tbody/tr[${srx row number}]/td[3]/div/div/button
    Set Global Variable             ${number of buttons cell}               xpath:${button pane}${table xpath}/tbody/tr[${button row number}]/td[1]/div
    Set Global Variable             ${monthly fee cell}                     xpath:${button pane}${table xpath}/tbody/tr[${button row number}]/td[2]/div
    Set Global Variable             ${remove monthly fee button}            xpath:${button pane}${table xpath}/tbody/tr[${button row number}]/td[3]/div/div/button

Number Of Rows SRX
    ${srx row}                      Get Element Count                       xpath:${monthly pane}${table xpath}/tbody/tr
    Set Global Variable             ${srx row}

Number Of Rows Button
    ${button row}                   Get Element Count                       xpath:${button pane}${table xpath}/tbody/tr
    Set Global Variable             ${button row}

Is Delete Button Fee
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                        Removal Confirmation

Is Delete SRXCloud Fee
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                        Removal Confirmation

Is Add Button Fee
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                        Add new button fee

Is Add SRXCloud Fee
    Sleep                           1 second
    Element Text Should Be          css:.modal-title                        Add new ShipTo fee

Is SRXCloud
    Sleep                           1 second
    Element Text Should Be          xpath:/html/body/div/div/div/div[2]/div/div[2]/div/div/div/div[3]/div/div/div[2]/div/button     Add new ShipTo fee

Is Button Monthly Fee
    Sleep                           1 second
    Element Text Should Be          xpath:/html/body/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/button     Add new button fee
