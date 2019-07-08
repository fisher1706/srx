*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${admin email}                  admin@example.com
${admin first}                  admin first
${admin last}                   admin last
${edit admin first}             edit admin first
${edit admin last}              edit admin last

*** Test Cases ***
Valid Add Admin User
    Set Suite Variable              ${const number admin}           ${number of row}
    Click Element                   id:distributor-details-tab-2
    Sleep                           2 second
    Click Element                   xpath:${distributors admin pane}${button info}
    Input Text                      id:email_id                     ${admin email}
    Input Text                      id:firstName_id                 ${admin first}
    Input Text                      id:lastName_id                  ${admin last}
    Click Element                   xpath:${button modal dialog ok}

Checking New User
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/div       ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[2]/div       ${admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of new row}]/td[3]/div       ${admin last}

Checking User On Distributor Portal
    Goto Users Sub
    ${const number distributor}     Evaluate                ${number of row u}-1
    Set Suite Variable              ${const number distributor}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[1]      ${admin email}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[2]      ${admin first}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[3]      ${admin last}

Edit From Distributor Portal
    Click Element                   xpath:(${react table raw})[${number of row u}]${edit super user}
    Input By Name                   firstName   ${edit admin first}
    Input By Name                   lastName    ${edit admin last}
    Click Element                   xpath:${button submit}

Checking Edit User From Distributor Portal
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[1]      ${admin email}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[2]      ${edit admin first}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[3]      ${edit admin last}
    Finish Suite
    Sleep                           5 second

Checking Edit User On Admin Portal
    Preparation
    Click Element                   id:distributor-details-tab-2
    Sleep                           2 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/div       ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div       ${edit admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div       ${edit admin last}

Edit From Admin Portal
    Click Element                   id:distributor-details-tab-2
    Sleep                           2 second
    Click Element                   ${edit user button}
    Input Text                      id:firstName_id         ${admin first}
    Input Text                      id:lastName_id          ${admin last}
    Click Element                   xpath:${button modal dialog ok} 

Checking Edit User From Admin Portal
    Sleep                           5 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/div       ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div       ${admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div       ${admin last}

Checking Edit User On Distributor Portal
    Goto Users Sub
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[1]      ${admin email}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[2]      ${admin first}
    Element Text Should Be          xpath:((${react table raw})[${number of row u}]${react table column})[3]      ${admin last}

Delete User From Distributor Portal
    Click Element                   xpath:(${react table raw})[${number of row u}]${delete super user}
    Dialog Should Be About          ${admin first} ${admin last}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking Users Number On Distributor Portal After Delete From Distributor Portal
    ${number of row u}              Get Element Count           xpath:${react table raw}
    Run Keyword If                  ${number of row u}==${const number distributor}     Log To Console      Pass    ELSE    Fail    Fail
    Finish Suite
    Sleep                           5 second

Checking Users Number On Admin Portal After Delete From Distributor Portal
    Preparation
    Click Element                   id:distributor-details-tab-2
    ${number of row}                Get Rows Count          ${table xpath}
    Run Keyword If                  ${number of row}==${const number admin}     Log To Console      Pass    ELSE    Fail    Fail

Delete User From Admin Portal
    Sleep                           2 second
    Click Element                   xpath:${distributors admin pane}${button info}
    Input Text                      id:email_id             ${admin email}
    Input Text                      id:firstName_id         ${admin first}
    Input Text                      id:lastName_id          ${admin last}
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second
    ${number of row}                Get Rows Count          ${table xpath}
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]            ${admin email}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]            ${admin first}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]            ${admin last}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

Checking Users Number On Admin Portal After Delete From Admin Portal
    Click Element                   id:distributor-details-tab-2
    ${number of row}                Get Rows Count          ${table xpath}
    Run Keyword If                  ${number of row}==${const number admin}     Log To Console      Pass    ELSE    Fail    Fail

Checking Users Number On Distributor Portal After Delete From Admin Portal
    Goto Users Sub
    ${number of row}                Get Element Count           xpath:${react table raw}
    Run Keyword If                  ${number of row u}==${const number distributor}     Log To Console      Pass    ELSE    Fail    Fail
    Finish Suite
    Sleep                           5 second

Create Admin On Distributor Portal
    Goto Users Sub
    Click Element                   ${create button}
    Input By Name                   email       ${admin email}
    Input By Name                   firstName   ${admin first}
    Input By Name                   lastName    ${admin last}
    Click Element                   xpath:${button submit}
    Sleep                           3 second
    Set Suite Variable              ${const number distributor 2}       ${number of row u}
    ${number of new row u}          Evaluate                            ${number of row u}+1
    Set Suite Variable              ${number of new row u}

Checking Admin On Distributor Portal
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[${number of new row u}]${react table column})[1]      ${admin email}
    Element Text Should Be          xpath:((${react table raw})[${number of new row u}]${react table column})[2]      ${admin first}
    Element Text Should Be          xpath:((${react table raw})[${number of new row u}]${react table column})[3]      ${admin last}

Edit Admin From Distributor Portal
    Click Element                   xpath:(${react table raw})[${number of new row u}]${edit super user}
    Input By Name                   firstName   ${edit admin first}
    Input By Name                   lastName    ${edit admin last}
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    Finish Suite
    Sleep                           5 second

Checking Admin On Admin Portal
    Preparation
    ${const number admin 2}         Evaluate                            ${number of row}-1
    Set Suite Variable              ${const number admin 2}
    Click Element                   id:distributor-details-tab-2
    Sleep                           2 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/div       ${admin email}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[2]/div       ${edit admin first}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]/div       ${edit admin last}

Delete Admin
    ${number of row}                Get Rows Count          ${table xpath}
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]            ${admin email}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]            ${edit admin first}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]            ${edit admin last}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           2 second

Checking Admins Number On Admin Portal After Delete From Admin Portal
    Click Element                   id:distributor-details-tab-2
    ${number of row}                Get Rows Count          ${table xpath}
    Run Keyword If                  ${number of row}==${const number admin 2}     Log To Console      Pass    ELSE    Fail    Fail

Checking Admins Number On Distributor Portal After Delete From Admin Portal
    Goto Users Sub
    ${number of row u}              Get Element Count           xpath:${react table raw}
    Run Keyword If                  ${number of row u}==${const number distributor 2}     Log To Console      Pass    ELSE    Fail    Fail
    Finish Suite
    Sleep                           5 second

*** Keywords ***
Preparation
    Goto Admin Users Sub
    ${number of row}                Get Rows Count          ${table xpath}
    ${number of new row}=           Evaluate                ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${edit user button}     xpath:${table xpath}/tbody/tr[${number of row}]${button success}
    Set Suite Variable              ${delete user button}   xpath:${table xpath}/tbody/tr[${number of row}]${button danger}

Goto Users Sub
    Finish Suite
    Sleep                           5 second
    Start Distributor
    Sleep                           5 second
    Goto Sidebar Users
    Sleep                           1 second
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    ${number of row u}              Get Element Count           xpath:${react table raw}
    Set Suite Variable              ${number of row u}

Goto Admin Users Sub
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/distributors"]
    Sleep                           3 second
    Open Full Table
    Sleep                           4 second
    ${static distributor}           Get Row By Text         ${table xpath}      1       ${distributor_name}
    Click Element                   xpath:${table xpath}/tbody/tr[${static distributor}]/td[1]/a