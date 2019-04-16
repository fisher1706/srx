*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             OperatingSystem
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Import Catalog
    Sleep                           3 second
    ${catalog sku}                  Generate Random Name U
    Set Suite Variable              ${catalog sku}
    Create File                     ${CURDIR}/../../../resources/importCatalog.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v${\n}${catalog sku},,,${catalog sku},,,,,,,,,,10,,,,1.2,1.3,1.4,1.5,active
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
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[3]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[4]              10
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[5]              1.2
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[6]              1.4
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[7]              1.3
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[8]              1.5

Update Catalog
    Sleep                           5 second
    Create File                     ${CURDIR}/../../../resources/updateCatalog.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v${\n}${catalog sku},,,${catalog sku},,,,,,,,,,20,,,,25,2,3.5,6.7,active
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
    Is Full Table                   ${number of row}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[1]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[3]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[4]              20
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[5]              25
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[6]              3.5
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[7]              2
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[8]              6.7

Import Inventory Data
    Sleep                           4 second
    Click Element                   xpath:(${tab element})[2]
    Sleep                           2 second
    Create File                     ${CURDIR}/../../../resources/importInventory.csv      a,b,c,d,e${\n}${catalog sku},123,124,125,stock
    Sleep                           2 second
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importInventory.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Сhecking Import Inventory
    Sleep                           2 second
    ${number of row}                Get React Rows Count                                                                    ${react table}
    Log To Console                  ${number of row}
    Is Full Table                   ${number of row}
    Sleep                           5 second
    ${number of new row}            Get React Rows Count                                                                    ${react table}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[2]              123
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[3]              124
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[4]              125
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]              stock

Update Inventory
    Sleep                           5 second
    Create File                     ${CURDIR}/../../../resources/updateInventory.csv      a,b,c,d,e${\n}${catalog sku},223,224,225,non-stock
    Sleep                           2 second
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/updateInventory.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Сhecking Update Inventory
    Sleep                           2 second
    ${number of row}                Get React Rows Count                                                                    ${react table}
    Is Full Table                   ${number of row}
    ${number of new row}            Get React Rows Count                                                                    ${react table}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[2]              223
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[3]              224
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[4]              225
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]              non-stock

Edit Inventory
    [Tags]                          Edit
    Sleep                           2 second
    ${number of row}                Get React Rows Count                                                                ${react table}
    Is Full Table                   ${number of row}
    Click Element                   xpath:((${react table raw})[${number of row}]${react table column})[6]/*
    Input Text                      xpath://input[contains(@name, 'inventoryLevel')]                                    323
    Input Text                      xpath://input[contains(@name, 'leadTime')]                                          324
    Input Text                      xpath://input[contains(@name, 'customerNo')]                                        325
    Click Element                   xpath:${button submit}

Checking Edit
    Sleep                           2 second
    ${number of row}                Get React Rows Count                                                                ${react table}
    Is Full Table                   ${number of row}
    ${number of row}                Get React Rows Count                                                                ${react table}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[1]              ${catalog sku}
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[2]              323
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[3]              324
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[4]              325
    Element Text Should Be          xpath:((${react table raw})[${number of row}]${react table column})[5]              non-stock

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Sidebar Catalog
    Sleep                           3 second
    ${number of row}                Get React Rows Count                                                  ${react table}
    Set Suite Variable              ${number of row}