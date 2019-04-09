*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***
${number of new row}
${number of row}
${edit product}                     //button[contains(@title, 'Edit Product')]
${view product}                     //button[contains(@title, 'View Details')]
${dist sku}                         AD

*** Test Cases ***
Invalid Create New Product
    [Tags]                          CatalogInvalid
    Click Element                   ${create button}
    Sleep                           2 second
    Click Element                   xpath:${button submit}
    ${data shrink}                  Get Element Attribute                                   xpath://input[contains(@name, 'partSku')]/../..//label                  data-shrink
    Should Be Equal As Strings      ${data shrink}                                          true
    Input Text                      xpath://input[contains(@name, 'partSku')]               ${random string}
    Click Element                   xpath:${button submit}
    ${data shrink}                  Get Element Attribute                                   xpath://input[contains(@name, 'shortDescription')]/../..//label         data-shrink
    Should Be Equal As Strings      ${data shrink}                                          true
    Input Text                      xpath://input[contains(@name, 'shortDescription')]      ${user last name}
    Click Element                   xpath:${button submit}
    ${data shrink}                  Get Element Attribute                                   xpath://input[contains(@name, 'roundBuy')]/../..//label                 data-shrink
    Should Be Equal As Strings      ${data shrink}                                          true
    Input Text                      xpath://input[contains(@name, 'roundBuy')]              ${round by}
    Clear Element Text              xpath://input[contains(@name, 'partSku')]
    Input Text                      xpath://input[contains(@name, 'partSku')]               ${dist sku}
    Click Element                   xpath:${button submit}
    Sleep                           2 second
    Page Should Contain Element     ${alert dialog}
    Sleep                           1 second
    Click Element                   ${close dialog}

Valid Create New Product
    [Tags]                          CatalogValid
    Click Element                   ${create button}
    Input Text                      xpath://input[contains(@name, 'partSku')]                   ${random string}
    Input Text                      xpath://input[contains(@name, 'shortDescription')]          ${user last name}
    Input Text                      xpath://input[contains(@name, 'weight')]                    10
    Input Text                      xpath://input[contains(@name, 'roundBuy')]                  ${round by}
    Input Text                      xpath://input[contains(@name, 'height')]                    15
    Input Text                      xpath://input[contains(@name, 'width')]                     22
    Input Text                      xpath://input[contains(@name, 'length')]                    30
    Input Text                      xpath://input[contains(@name, 'manufacturerPartNumber')]    ${dynamic code}
    Input Text                      xpath://input[contains(@name, 'longDescription')]           ${dynamic adress1}
    Input Text                      xpath://input[contains(@name, 'productLvl1')]               ${level 1}
    Input Text                      xpath://input[contains(@name, 'productLvl2')]               ${level 2}
    Input Text                      xpath://input[contains(@name, 'productLvl3')]               ${level 3}
    Input Text                      xpath://input[contains(@name, 'attribute1')]                ${sub 1}
    Input Text                      xpath://input[contains(@name, 'attribute2')]                ${sub 2}
    Input Text                      xpath://input[contains(@name, 'attribute3')]                ${sub 3}
    Input Text                      xpath://input[contains(@name, 'gtin')]                      ${dynamic city}
    Input Text                      xpath://input[contains(@name, 'upc')]                       ${test string}
    Input Text                      xpath://input[contains(@name, 'alternative')]               ${test number}
    Input Text                      xpath://input[contains(@name, 'keyword')]                   ${keyword}
    Input Text                      xpath://input[contains(@name, 'image')]                     ${keyword}
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    React Last
    Sleep                           3 second
    ${number of new row}            Get React Rows Count                ${react table raw}
    Set Suite Variable              ${number of new row}

Checking New Product
    [Tags]                          CatalogChecking
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]              ${random string}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[3]              ${user last name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[4]              ${round by}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]              10
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[6]              15
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[7]              22
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[8]              30
    Click Element                   xpath:(${react table raw})[${number of new row}]${view product}
    Sleep                           3 second
    Element Text Should Be          xpath://table/tbody/tr[1]/td[2]                                                         ${random string}
    Element Text Should Be          xpath://table/tbody/tr[2]/td[2]                                                         ACTIVE
    Element Text Should Be          xpath://table/tbody/tr[3]/td[2]                                                         ${dynamic adress1}
    Element Text Should Be          xpath://table/tbody/tr[4]/td[2]                                                         ${user last name}
    Element Text Should Be          xpath://table/tbody/tr[5]/td[2]                                                         10
    Element Text Should Be          xpath://table/tbody/tr[6]/td[2]                                                         15
    Element Text Should Be          xpath://table/tbody/tr[7]/td[2]                                                         22
    Element Text Should Be          xpath://table/tbody/tr[8]/td[2]                                                         30
    Element Text Should Be          xpath://table/tbody/tr[9]/td[2]                                                         ${round by}
    Element Text Should Be          xpath://table/tbody/tr[10]/td[2]                                                        ${dynamic code}
    Element Text Should Be          xpath://table/tbody/tr[12]/td[2]                                                        ${level 1}
    Element Text Should Be          xpath://table/tbody/tr[13]/td[2]                                                        ${level 2}
    Element Text Should Be          xpath://table/tbody/tr[14]/td[2]                                                        ${level 3}
    Element Text Should Be          xpath://table/tbody/tr[15]/td[2]                                                        ${sub 1}
    Element Text Should Be          xpath://table/tbody/tr[16]/td[2]                                                        ${sub 2}
    Element Text Should Be          xpath://table/tbody/tr[17]/td[2]                                                        ${sub 3}
    Element Text Should Be          xpath://table/tbody/tr[18]/td[2]                                                        ${dynamic city}
    Element Text Should Be          xpath://table/tbody/tr[19]/td[2]                                                        ${test string}
    Element Text Should Be          xpath://table/tbody/tr[20]/td[2]                                                        ${test number}
    Element Text Should Be          xpath://table/tbody/tr[21]/td[2]                                                        ${keyword}
    Element Text Should Be          xpath://table/tbody/tr[22]/td[2]                                                        ${keyword}
    Click Element                   xpath:${close dialog}
    Sleep                           5 second

Edit Product
    [Tags]                          CatalogEdit
    Click Element                   xpath:(${react table raw})[${number of new row}]${edit product}
    Input Text                      xpath://input[contains(@name, 'partSku')]                   ${edit random string}
    Input Text                      xpath://input[contains(@name, 'shortDescription')]          ${edit last name}
    Input Text                      xpath://input[contains(@name, 'weight')]                    20
    Input Text                      xpath://input[contains(@name, 'roundBuy')]                  ${edit round by}
    Input Text                      xpath://input[contains(@name, 'height')]                    20
    Input Text                      xpath://input[contains(@name, 'width')]                     27
    Input Text                      xpath://input[contains(@name, 'length')]                    32
    Input Text                      xpath://input[contains(@name, 'manufacturerPartNumber')]    ${edit code}
    Input Text                      xpath://input[contains(@name, 'longDescription')]           ${edit adress1}
    Input Text                      xpath://input[contains(@name, 'productLvl1')]               ${edit level 1}
    Input Text                      xpath://input[contains(@name, 'productLvl2')]               ${edit level 2}
    Input Text                      xpath://input[contains(@name, 'productLvl3')]               ${edit level 3}
    Input Text                      xpath://input[contains(@name, 'attribute1')]                ${edit sub 1}
    Input Text                      xpath://input[contains(@name, 'attribute2')]                ${edit sub 2}
    Input Text                      xpath://input[contains(@name, 'attribute3')]                ${edit sub 3}
    Input Text                      xpath://input[contains(@name, 'gtin')]                      ${edit city}
    Input Text                      xpath://input[contains(@name, 'upc')]                       ${edit string}
    Input Text                      xpath://input[contains(@name, 'alternative')]               ${edit test number}
    Input Text                      xpath://input[contains(@name, 'keyword')]                   ${edit keyword}
    Input Text                      xpath://input[contains(@name, 'image')]                     ${edit keyword}
    Select From Dropdown            (${dropdown menu})[1]                                       OBSOLETE
    Click Element                   xpath:${button submit}
    Sleep                           3 second

Checking Edit Product
    [Tags]                          Catalog
    Sleep                           3 second
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[1]              ${edit random string}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[3]              ${edit last name}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[4]              ${edit round by}
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[5]              20
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[6]              20
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[7]              27
    Element Text Should Be          xpath:((${react table raw})[${number of new row}]${react table column})[8]              32
    Click Element                   xpath:(${react table raw})[${number of new row}]${view product}
    Sleep                           3 second
    Element Text Should Be          xpath://table/tbody/tr[1]/td[2]                                                         ${edit random string}
    Element Text Should Be          xpath://table/tbody/tr[2]/td[2]                                                         OBSOLETE
    Element Text Should Be          xpath://table/tbody/tr[3]/td[2]                                                         ${edit adress1}
    Element Text Should Be          xpath://table/tbody/tr[4]/td[2]                                                         ${edit last name}
    Element Text Should Be          xpath://table/tbody/tr[5]/td[2]                                                         20
    Element Text Should Be          xpath://table/tbody/tr[6]/td[2]                                                         20
    Element Text Should Be          xpath://table/tbody/tr[7]/td[2]                                                         27
    Element Text Should Be          xpath://table/tbody/tr[8]/td[2]                                                         32
    Element Text Should Be          xpath://table/tbody/tr[9]/td[2]                                                         ${edit round by}
    Element Text Should Be          xpath://table/tbody/tr[10]/td[2]                                                        ${edit code}
    Element Text Should Be          xpath://table/tbody/tr[12]/td[2]                                                        ${edit level 1}
    Element Text Should Be          xpath://table/tbody/tr[13]/td[2]                                                        ${edit level 2}
    Element Text Should Be          xpath://table/tbody/tr[14]/td[2]                                                        ${edit level 3}
    Element Text Should Be          xpath://table/tbody/tr[15]/td[2]                                                        ${edit sub 1}
    Element Text Should Be          xpath://table/tbody/tr[16]/td[2]                                                        ${edit sub 2}
    Element Text Should Be          xpath://table/tbody/tr[17]/td[2]                                                        ${edit sub 3}
    Element Text Should Be          xpath://table/tbody/tr[18]/td[2]                                                        ${edit city}
    Element Text Should Be          xpath://table/tbody/tr[19]/td[2]                                                        ${edit string}
    Element Text Should Be          xpath://table/tbody/tr[20]/td[2]                                                        ${edit test number}
    Element Text Should Be          xpath://table/tbody/tr[21]/td[2]                                                        ${edit keyword}
    Element Text Should Be          xpath://table/tbody/tr[22]/td[2]                                                        ${edit keyword}
    Click Element                   xpath:${close dialog}
    Sleep                           1 second

Sorting Catalog
    [Tags]                                              Sorting                 ProductSorting      Catalog
    React First
    Sleep                                               2 second
    Sorting React With Last Page                        1
    Sorting React With Last Page                        2
    Sorting React With Last Page                        3
    Sorting React With Last Page                        4
    Sorting React With Last Page                        5
    Sorting React With Last Page                        6
    Sorting React With Last Page                        7
    Sorting React With Last Page                        8

Catalog Filtration
    [Tags]                          Filter
    Filter Add                      1   1   NYSFUCWSLUUUMJUUOZ

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Catalog
    Sleep                           3 second
    ${random string}                Generate Random Name U
    ${edit random string}           Generate Random Name U
    Set Suite Variable              ${random string}
    Set Suite Variable              ${edit random string}
    Set Suite Variable              ${number of new row}
    Set Suite Variable              ${number of row}