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
    Create File                     ${CURDIR}/../../../resources/importUsageHistory.csv    a,b,c,d,e${random id},2048,STATIC SKU,50,2018/12/30 10:15:30
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
    ${number of row}                Get Rows Count                                                  ${table xpath}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]           CUSTOMER
    

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Usage History
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}
