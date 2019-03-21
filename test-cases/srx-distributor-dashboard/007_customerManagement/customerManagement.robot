*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***


*** Test Cases ***
Create New Customer
    Click Element                   id:item-action-create
    Input By Name                   name            ${user first name}
    ${customer type}                Select First    (${dropdown menu})[1]
    Set Suite Variable              ${customer type}
    ${market type}                  Select First    (${dropdown menu})[2]
    Set Suite Variable              ${market type}
    ${buffer}                       Select First    (${dropdown menu})[3]
    ${warehouse}                    Get Lines Matching Regexp   ${current warehouse}    ^\((.{0,})\)
    Set Suite Variable              ${warehouse}
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Checking New Customer
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]      ${user first name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[2]      ${EMPTY}
    ${current warehouse}            Get Text    xpath:((${react table raw})[${number of new row}]${react table column})[3]
    ${necessary warehouse}          Get Lines Matching Regexp   ${current warehouse}    ${warehouse}\((.{0,})\)
    Should Be Equal As Strings      ${current warehouse}        ${necessary warehouse}

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Customers
    ${number of row}                Get Element Count           xpath:${react table raw}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}