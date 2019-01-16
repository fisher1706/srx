*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Keyword
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Deactivate
    ${my row}                       Get Row By Text                 ${table xpath}      1       Srx-group-test-distributor
    Set Suite Variable              ${my row}
    ${status}                       Get Text    xpath:${table xpath}/tbody/tr[${my row}]/td[6]
    Run Keyword If                  "${status}"=="ACTIVE"   Deactivate      ELSE IF     "${status}"=="INACTIVE"     No Operation    ELSE    Fail      Unexpected distributor status

#Login To Deactivate Distributor By Admin
#    ${SUB EMAIL}                    Return Sub Email
#    Set Suite Variable              ${SUB EMAIL}
#    Login On Distributor Portal Sub
#    Element Text Should Be          ${inactive account}     INACTIVE ACCOUNT
#    ${items}                        Get Element Count       ${sidebar item}
#    Should Be Equal As Integers     ${items}                3
#    Click Link                      xpath://*[@href="/settings"]
#    Click Element                   id:settings-tab-pricing-billing
#    Click Element                   id:pricing-billing-tab-billing-settings

Login To Deactivate Distributor By User
#    Sign Out
#    Sleep                           2 second
    ${SUB EMAIL}                    Return Permissions Email
    Set Suite Variable              ${SUB EMAIL}
    Login On Distributor Portal Sub
#    Enter Correct Email Sub
#    Enter Password
#    Correct Submit Login
#    Sleep                           5 second
    Element Text Should Be          ${inactive account}     INACTIVE ACCOUNT
    ${items}                        Get Element Count       ${sidebar item}
    Should Be Equal As Integers     ${items}                1
    Finish Suite
    Sleep                           5 second

Activate
    Preparation
    ${my row}                       Get Row By Text     ${table xpath}    1       Srx-group-test-distributor
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my row}]/td[6]      INACTIVE
    Click Element                   xpath:${table xpath}/tbody/tr[${my row}]${button primary}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     Srx-group-test-distributor
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]     INACTIVE
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           5 second

Login To Active Distributor By Admin
    ${SUB EMAIL}                    Return Sub Email
    Set Suite Variable              ${SUB EMAIL}
    Login On Distributor Portal Sub
    ${items}                        Get Element Count       ${sidebar item}
    Run Keyword If                  ${items}<10     Fail    User is not active      Else    No Operation

*** Keywords ***
Preparation
    Start Admin
    Sleep                           3 second
    Click Link                      xpath://*[@href="/distributors"]
    Sleep                           5 second
    ${SUB HOST}                     Return Sub Link
    Set Global Variable             ${SUB HOST}
    Open Full Table

Finish Keyword
    Finish Suite
    Sleep                           3 second
    Start Admin
    Sleep                           3 second
    Click Link                      xpath://*[@href="/distributors"]
    Sleep                           5 second
    Open Full Table
    ${my row}                       Get Row By Text                 ${table xpath}      1       Srx-group-test-distributor
    Set Suite Variable              ${my row}
    ${status}                       Get Text    xpath:${table xpath}/tbody/tr[${my row}]/td[6]
    Run Keyword If                  "${status}"=="INACTIVE"   Activate      ELSE IF     "${status}"=="ACTIVE"     No Operation    ELSE    Fail      Unexpected distributor status
    Finish Suite
    Sleep                           2 second

Login On Distributor Portal Sub
    Finish Suite
    Start Distributor
    Sleep                           5 second

Deactivate
    Click Element                   xpath:${table xpath}/tbody/tr[${my row}]${button info}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     Srx-group-test-distributor
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]     ACTIVE
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

Activate
    Click Element                   xpath:${table xpath}/tbody/tr[${my row}]${button primary}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           5 second