*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             OperatingSystem
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variable ***
${view product}                     //button[contains(@title, 'View Details')]

*** Test Cases ***
Import Catalog
    ${catalog sku}                  Generate Random Name U
    Set Suite Variable              ${catalog sku}
    Create File                     ${CURDIR}/../../../resources/importCatalog.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v${\n}${catalog sku},,,${catalog sku},,,,,,,,,,10,,,,1.2,1.3,1.4,1.5,
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
    ${number of row}                Get React Rows Count                                                                ${react table raw}
    Set Suite Variable              ${number of row}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[1]              ${catalog sku}
    Click Element                   xpath:(${react table raw})[${number of row}]${view product}
    Sleep                           3 second
    Element Text Should Be          xpath://table/tbody/tr[2]/td[2]                                                     ACTIVE
    Click Element                   xpath:${close dialog}
    Sleep                           3 second

Import Lifecycle Status
    Click Element                   xpath:(${tab element})[3]
    Sleep                           2 second
    Create File                     ${CURDIR}/../../../resources/importLifecycleStatus.csv      a,b${\n}${catalog sku},mature
    Sleep                           2 second
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importLifecycleStatus.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           7 second

Сhecking Lifecycle Status
    Click Element                   xpath:(${tab element})[1]
    Sleep                           2 second
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[1]              ${catalog sku}
    Click Element                   xpath:(${react table raw})[${number of row}]${view product}
    Sleep                           3 second
    Element Text Should Be          xpath://table/tbody/tr[2]/td[2]                                                     MATURE
    Click Element                   xpath:${close dialog}
    Sleep                           3 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           1 second
    Goto Sidebar Catalog
    Sleep                           2 second