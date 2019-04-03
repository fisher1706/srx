*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             OperatingSystem
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

***Variables***
${upload button}                    //label[contains(@for, 'file-upload')]

*** Test Cases ***
Import Catalog
    Sleep                           3 second
    ${catalog sku}                  Generate Random Name U
    Set Suite Variable              ${catalog sku}
    Create File                     ${CURDIR}/../../../resources/importCatalog.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u${\n}${catalog sku},,,${catalog sku},,,,,,,,,,10,,,,1.2,1.3,1.4,1.5,
    Sleep                           2 second
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importCatalog.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Сhecking Import
    React Last
    Sleep                           2 second
    ${number of row}                Get React Rows Count                                                                ${react table}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[1]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[2]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[3]              10
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[4]              1.2
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[5]              1.4
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[6]              1.3
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[7]              1.5

Update Catalog
    Sleep                           5 second
    Create File                     ${CURDIR}/../../../resources/updateCatalog.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u${\n}${catalog sku},,,${catalog sku},,,,,,,,,,20,,,,25,2,3.5,6.7,
    Sleep                           2 second
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/updateCatalog.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Сhecking Update Catalog
    Sleep                           2 second
    ${number of row}                Get React Rows Count                                                                ${react table}
    Is Full table                   ${number of row}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[1]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[2]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[3]              20
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[4]              25
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[5]              3.5
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[6]              2
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[7]              6.7

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Sidebar Catalog
    Sleep                           3 second
    ${number of row}                Get React Rows Count                                                  ${react table}
    Set Suite Variable              ${number of row}

Is Full table
    [Arguments]                     ${number of row}
    Run Keyword If                  ${number of row} >= 50        React Last