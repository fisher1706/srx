*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             Selenium2Library
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${price 1 1}                        $111.00
${uom 1 1}                          222
${price 1 2}                        $333.00
${uom 1 2}                          444
${price 2 1}                        $555.00
${uom 2 1}                          666
${price 2 2}                        $777.00
${uom 2 2}                          888
${date 1 1}                         Sat, Dec 12, 2020
${date 1 2}                         Thu, Nov 11, 2021
${date 2 1}                         Mon, Dec 12, 2022
${date 2 2}                         Sat, Nov 11, 2023

*** Test Case ***
Pricing Import
    Select Pricing Customer         Static Customer
    ${status}                       Get Text        xpath:((${react table raw})[1]${react table column})[3]
    Run Keyword If                  "${status}"=="${uom 1 1}"   If First Pricing    ELSE IF     "${status}"=="${uom 2 1}"   If Second Pricing   ELSE    Fail    Pricing data is incorrect
    Sleep                           5 second
    Page Should Contain             Validation status: valid
    Click Element                   xpath:(${dialog}${button})[2]
    Sleep                           10 second

Checking Pricing
    Run Keyword If                  "${restatus}"=="first"      First Pricing       ELSE IF     "${restatus}"=="second"      Second Pricing     ELSE    Fail    Unexpected Behaviour

Checking Pricing Report
    Goto Pricing Report
    Click Element                   xpath:${button info}
    Choose From Select Box          (${modal dialog}${select control})[1]     Static Customer
    Click Element                   xpath:${modal dialog}${button info}
    Run Keyword If                  "${restatus}"=="first"      First Pricing Report       ELSE IF     "${restatus}"=="second"      Second Pricing Report     ELSE    Fail    Unexpected Behaviour
    Sleep                           3 second

Checking Static Pricing Report
    [Tags]                          Report
    Goto Sidebar Reports
    Sleep                           3 second
    Click Element                   xpath:${button info}
    Choose From Select Box          (${modal dialog}${select control})[1]           Static Customer
    Choose From Select Box          (${modal dialog}${select control})[2]           2048
    Input Text                      xpath:(${modal dialog}${form control})[1]       12/12/2021, 12:00 A
    Input Text                      xpath:(${modal dialog}${form control})[2]       12/13/2021, 12:00 A
    Click Element                   xpath:${modal dialog}${button info}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[1]/div      AUTO_SUBMIT
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]/div      $5.00
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[3]/div      FT
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[4]/div      Sun, Dec 12, 2021

Sorting Pricing
    [Tags]                          Sorting
    Goto Sidebar Pricing
    Sleep                           1 second
    Select Pricing Customer         Customer A
    Sort React                      1
    Sort React                      2
    Sort React                      3
    Sort React                      4

*** Keywords ***
Preparation
    Start Distributor

If First Pricing
    First Pricing
    Choose File                     id:file-upload                  ${CURDIR}/../../../resources/pricing2.csv
    Set Suite Variable              ${restatus}     second

If Second Pricing
    Second Pricing
    Choose File                     id:file-upload                  ${CURDIR}/../../../resources/pricing1.csv
    Set Suite Variable              ${restatus}     first

First Pricing
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]     ${price 1 1}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]     ${uom 1 1}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]     ${date 1 1}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     ${price 1 2}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     ${uom 1 2}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[4]     ${date 1 2}

Second Pricing
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]     ${price 2 1}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]     ${uom 2 1}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]     ${date 2 1}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     ${price 2 2}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     ${uom 2 2}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[4]     ${date 2 2}

First Pricing Report
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[1]/td[2]/div      ${price 1 1}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[1]/td[3]/div      ${uom 1 1}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[1]/td[4]/div      ${date 1 1}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[2]/td[2]/div      ${price 1 2}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[2]/td[3]/div      ${uom 1 2}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[2]/td[4]/div      ${date 1 2}

Second Pricing Report
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[1]/td[2]/div      ${price 2 1}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[1]/td[3]/div      ${uom 2 1}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[1]/td[4]/div      ${date 2 1}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[2]/td[2]/div      ${price 2 2}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[2]/td[3]/div      ${uom 2 2}
    Element Text Should Be          xpath:${report pricing pane}${table xpath}/tbody/tr[2]/td[4]/div      ${date 2 2}

Goto Pricing Report
    Goto Sidebar Reports
    Sleep                           2 second
    Click Element                   id:reports-tab-pricing-report
    Sleep                           1 second


