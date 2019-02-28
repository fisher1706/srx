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
    Sleep                           5 second
    ${buffer1}                      Generate Random String                              18          [LETTERS]
    ${catalog sku}                  Convert To Uppercase                                ${buffer1}
    Set Suite Variable              ${catalog sku}
    Create File                     ${CURDIR}/../../../resources/importCatalog.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r${\n}${catalog sku},,,${catalog sku},,,,,,,,,,10,,,,
    Sleep                           2 second
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importCatalog.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Сhecking Import
    click Element                   xpath:${last page}
    ${number of row}                Get Rows Count                                                  ${table xpath}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[1]           ${catalog sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]           ${catalog sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[6]           10
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[17]          ${EMPTY}

Update Catalog
    Sleep                           5 second
    Create File                     ${CURDIR}/../../../resources/updateCatalog.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r${\n}${catalog sku},,,${catalog sku},,,,,,,,,,20,,,,25
    Sleep                           2 second
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/updateCatalog.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Сhecking Update Catalog
    click Element                   xpath:${last page}
    ${number of row}                Get Rows Count                                                  ${table xpath}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[1]           ${catalog sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]           ${catalog sku}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[6]           20
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[17]          25

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Sidebar Catalog
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    Set Suite Variable              ${number of row}