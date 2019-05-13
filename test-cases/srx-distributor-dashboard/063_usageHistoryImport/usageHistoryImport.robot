*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             OperatingSystem
Library                             RequestsLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${usage history sku}                USAGE HISTORY

*** Test Cases ***
Import Usage history
    [Tags]                          ImportUsageHistory
    ${random id}                    Generate Random Name L
    Set Suite Variable              ${random id}
    Create File                     ${CURDIR}/../../../resources/importUsageHistory.csv    a,b,c,d,e,f,g${\n}${random id},${customer_name},${shipto_name},${shipto_id},STATIC SKU,50,2018/12/30 10:15:30
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importUsageHistory.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Reload Page
    Sleep                           5 second

Checking Usage History
    [Tags]                          CheckingUsageHistory
    Click Element                   xpath:${button filter}
    Click Element                   xpath:(${menu}${menu item})[1]
    Input Text                      xpath:${text field}                                         ${random id}
    Sleep                           5 second
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[1]     ${random id}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[2]     ${customer_name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[3]     ${shipto_name}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[4]     ${shipto_id}
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[5]     STATIC SKU
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[6]     50
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[7]     Sun Dec 30 2018
    Element Text Should Be          xpath:((${react table raw})[1]${react table column})[8]     Imported
    Click Element                   xpath:${filter type}/button

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Usage History
    Sleep                           5 second
    ${number of row}                Get React Rows Count                ${react table}
    ${number of new row}=           Evaluate                            ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
