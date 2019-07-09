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