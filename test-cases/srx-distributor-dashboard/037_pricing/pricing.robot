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
    Go Down
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    ${status}                       Get Text        xpath:${table xpath}/tbody/tr[1]/td[3]/div
    Run Keyword If                  "${status}"=="${uom 1 1}"   If First Pricing    ELSE IF     "${status}"=="${uom 2 1}"   If Second Pricing   ELSE    Fail    Pricing data is incorrect
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}            Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Checking Pricing
    Run Keyword If                  "${restatus}"=="first"      First Pricing       ELSE IF     "${restatus}"=="second"      Second Pricing     ELSE    Unexpected Behaviour

*** Keywords ***
Preparation
    Login In Distributor Portal
    Click Link                      xpath://*[@href="/pricing"]
    #Goto Pricing

Go Down
    Click Element                   xpath:(${select control})[1]
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]            \ue015
    Sleep                           1 second
    Press Key                       xpath:(${select control})[1]/div[1]/div[2]            \ue007
    ${text buffer sub}              Get Text                                    xpath:(${select control})[1]/div[1]/div[1]/span
    Sleep                           3 second
    Run Keyword If                  "${text buffer sub}"!="Static Customer"        Go Down

If First Pricing
    First Pricing
    Choose File                     id:file-upload                  ${CURDIR}/../../../resources/pricing2.csv
    Set Global Variable             ${restatus}     second

If Second Pricing
    Second Pricing
    Choose File                     id:file-upload                  ${CURDIR}/../../../resources/pricing1.csv
    Set Global Variable             ${restatus}     first

First Pricing
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]/div      ${price 1 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[3]/div      ${uom 1 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[4]/div      ${date 1 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[2]/div      ${price 1 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[3]/div      ${uom 1 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[4]/div      ${date 1 2}

Second Pricing
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[2]/div      ${price 2 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[3]/div      ${uom 2 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[4]/div      ${date 2 1}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[2]/div      ${price 2 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[3]/div      ${uom 2 2}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[2]/td[4]/div      ${date 2 2}


