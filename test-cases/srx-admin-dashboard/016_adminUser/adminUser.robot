*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Valid Add Admin User
    [Tags]                          ContentSuperUser                ValidAddAdminUser
    Set Global Variable             ${const number admin}           ${number of row}
    Click Element                   css:#distributor-details-tab-2
    Is Admin Users Tab
    Click Element                   css:.text-right > button:nth-child(1)
    Is Add User
    Input Text                      id:email_id                     ${admin email}
    Input Text                      id:firstName_id                 ${admin first}
    Input Text                      id:lastName_id                  ${admin last}
    Click Element                   css:.modal-dialog-ok-button

Checking New User
    [Tags]                          ContentSuperUser
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/div       ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div       ${admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${admin last}

Checking User On Distributor Portal
    [Tags]                          ContentSuperUser
    Goto Users Sub
    ${const number distributor}     Evaluate                ${number of row u}-1
    Set Global Variable             ${const number distributor}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[1]/div                ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[2]/div                ${admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[3]/div                ${admin last}

Edit From Distributor Portal
    [Tags]                          ContentSuperUser
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row u}]/td[6]/div/div[1]/button
    Input Text                      id:firstName_id             ${edit admin first}
    Input Text                      id:lastName_id              ${edit admin last}
    Click Element                   css:.modal-dialog-ok-button

Checking Edit User From Distributor Portal
    [Tags]                          ContentSuperUser
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[1]/div            ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[2]/div            ${edit admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[3]/div            ${edit admin last}
    Finish Suite
    Sleep                           5 second

Checking Edit User On Admin Portal
    [Tags]                          ContentSuperUser
    Preparation
    Click Element                   css:#distributor-details-tab-2
    Is Admin Users Tab
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/div       ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div       ${edit admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div       ${edit admin last}

Edit From Admin Portal
    [Tags]                          ContentSuperUser
    Click Element                   css:#distributor-details-tab-2
    Is Admin Users Tab
    Click Element                   ${edit user button}
    Input Text                      id:firstName_id         ${admin first}
    Input Text                      id:lastName_id          ${admin last}
    Click Element                   css:.modal-dialog-ok-button 

Checking Edit User From Admin Portal
    [Tags]                          ContentSuperUser
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/div       ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div       ${admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div       ${admin last}

Checking Edit User On Distributor Portal
    [Tags]                          ContentSuperUser
    Goto Users Sub
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[1]/div            ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[2]/div            ${admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row u}]/td[3]/div            ${admin last}

Delete User From Distributor Portal
    [Tags]                          ContentSuperUser
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row u}]/td[6]/div/div[2]/button
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]            ${admin email}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]            ${admin first}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]            ${admin last}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           2 second

Checking Users Number On Distributor Portal After Delete From Distributor Portal
    [Tags]                          ContentSuperUser
    Number Of Rows U
    Run Keyword If                  ${number of row u}==${const number distributor}     Log To Console      Pass    ELSE    Fail    Fail
    Finish Suite
    Sleep                           5 second

Checking Users Number On Admin Portal After Delete From Distributor Portal
    [Tags]                          ContentSuperUser
    Preparation
    Click Element                   css:#distributor-details-tab-2
    Is Admin Users Tab
    Number Of Rows
    Run Keyword If                  ${number of row}==${const number admin}     Log To Console      Pass    ELSE    Fail    Fail

Delete User From Admin Portal
    [Tags]                          ContentSuperUser
    Click Element                   css:.text-right > button:nth-child(1)
    Is Add User
    Input Text                      id:email_id             ${admin email}
    Input Text                      id:firstName_id         ${admin first}
    Input Text                      id:lastName_id          ${admin last}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           5 second
    Number Of Rows
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]/td[4]/div/div[2]/button
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]            ${admin email}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]            ${admin first}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]            ${admin last}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           2 second

Checking Users Number On Admin Portal After Delete From Admin Portal
    [Tags]                          ContentSuperUser
    Click Element                   css:#distributor-details-tab-2
    Is Admin Users Tab
    Number Of Rows
    Run Keyword If                  ${number of row}==${const number admin}     Log To Console      Pass    ELSE    Fail    Fail

Checking Users Number On Distributor Portal After Delete From Admin Portal
    [Tags]                          ContentSuperUser
    Goto Users Sub
    Number Of Rows U
    Run Keyword If                  ${number of row u}==${const number distributor}     Log To Console      Pass    ELSE    Fail    Fail
    Finish Suite
    Sleep                           5 second

Create Admin On Distributor Portal
    [Tags]                          AddSuperUser
    Goto Users Sub
    Click Element                   css:.btn-primary
    Input Text                      id:email_id                         ${admin email}
    Input Text                      id:firstName_id                     ${admin first}
    Input Text                      id:lastName_id                      ${admin last}
    Click Element                   css:div.checkbox:nth-child(1) > label:nth-child(1) > input:nth-child(1)
    Click Element                   css:.Select-control
    Press Key                       xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[4]/div/div/div/div[1]/div[2]        \ue007
    Click Element                   css:.modal-dialog-ok-button
    Set Global Variable             ${const number distributor 2}       ${number of row u}
    ${number of new row u}          Evaluate                            ${number of row u}+1
    Set Global Variable             ${number of new row u}

Checking Admin On Distributor Portal
    [Tags]                          AddSuperUser
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row u}]/td[1]/div            ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row u}]/td[2]/div            ${admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row u}]/td[3]/div            ${admin last}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row u}]/td[5]/div            Super User (Admin)

Edit Admin From Distributor Portal
    [Tags]                          ContentSuperUser
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row u}]/td[6]/div/div[1]/button
    Input Text                      id:firstName_id             ${edit admin first}
    Input Text                      id:lastName_id              ${edit admin last}
    Click Element                   css:.modal-dialog-ok-button
    Sleep                           5 second
    Finish Suite
    Sleep                           3 second

Checking Admin On Admin Portal
    [Tags]                          AddSuperUser
    Preparation
    ${const number admin 2}         Evaluate                            ${number of row}-1
    Set Global Variable             ${const number admin 2}
    Click Element                   css:#distributor-details-tab-2
    Is Admin Users Tab
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/div       ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div       ${edit admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div       ${edit admin last}

Delete Admin
    [Tags]                          AddSuperUser
    Number Of Rows
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]/td[4]/div/div[2]/button
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]            ${admin email}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]            ${edit admin first}
    Element Text Should Be          xpath:/html/body/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]            ${edit admin last}
    Click Element                   css:button.btn:nth-child(2)
    Sleep                           2 second

Checking Admins Number On Admin Portal After Delete From Admin Portal
    [Tags]                          AddSuperUser
    Click Element                   css:#distributor-details-tab-2
    Is Admin Users Tab
    Number Of Rows
    Run Keyword If                  ${number of row}==${const number admin 2}     Log To Console      Pass    ELSE    Fail    Fail

Checking Admins Number On Distributor Portal After Delete From Admin Portal
    [Tags]                          AddSuperUser
    Goto Users Sub
    Number Of Rows U
    Run Keyword If                  ${number of row u}==${const number distributor 2}     Log To Console      Pass    ELSE    Fail    Fail
    Finish Suite
    Sleep                           5 second

*** Keywords ***
Preparation
    Goto Admin Users Sub
    Number Of Rows
    ${number of new row}=           Evaluate                ${number of row}+1
    Set Global Variable             ${number of new row}
    Set Global Variable             ${edit user button}     xpath:${table xpath}/tbody/tr[${number of row}]/td[4]/div/div[1]/button
    Set Global Variable             ${delete user button}   xpath:${table xpath}/tbody/tr[${number of row}]/td[4]/div/div[2]/button
    ${SUB HOST}                     Return Sub Link
    Set Global Variable             ${SUB HOST}
    ${SUB EMAIL}                    Return Sub Email
    Set Global Variable             ${SUB EMAIL}
    
Goto Users Sub
    Finish Suite
    Run Keyword If                  "${browser}"=="xvfb"            Run Xvfb Sub    ELSE IF     "${browser}"=="chrome"      Run Chrome Sub      ELSE    Run Ff Sub
    Set Selenium Implicit Wait                                      20 second
    Set Selenium Timeout                                            10 second
    Enter Correct Email Sub
    Enter Password
    Correct Submit Login
    Sleep                           7 second
    Click Link                      xpath://*[@href="/users"]
    Sleep                           2 second
    Number Of Rows U

Goto Admin Users Sub
    Login In Admin Portal
    Sleep                           7 second
    Click Element                   css:#pageDropDown
    Click Element                   css:li.dropdown-item:nth-child(4)
    Sleep                           2 second
    Number Of Rows Sub
    Number Of Static Row Sub
    Click Element                   xpath:${table xpath}/tbody/tr[${static row sub}]/td[1]/a

Number Of Rows U
    ${number of row u}              Get Element Count   xpath:${table xpath}/tbody/tr
    Set Global Variable             ${number of row u}

Number Of Rows Sub
    ${number of row sub}            Get Element Count   xpath:${table xpath}/tbody/tr
    Set Global Variable             ${number of row sub}

Number Of Static Row Sub
    : FOR   ${counter sub}          IN RANGE    1   ${number of row sub}+1
    \   ${text buffer1 sub}         Get Text    xpath:${table xpath}/tbody/tr[${counter sub}]/td[1]/a
    \   Exit For Loop If            "Srx-group-test-distributor"=="${text buffer1 sub}"
    Set Global Variable             ${static row sub}     ${counter sub}

Is Delete User
    Element Text Should Be          css:.modal-title                                    Removal Confirmation

Is Edit User
    Element Text Should Be          css:.modal-title                                    Edit user

Is Add User
    Element Text Should Be          css:.modal-title                                    Add user

Is Admin Users Tab
    Sleep                           1 second
    Element Text Should Be          css:#distributor-details-pane-2 > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1)     Admin Users