*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Variables ***
${edit product}                     //button[contains(@title, 'Edit Product')]
${view product}                     //button[contains(@title, 'View Details')]
${dist sku}                         AD

*** Test Cases ***
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
    Element Text Should Be          xpath://table/tbody/tr[11]/td[2]                                                         ${round by}
    Element Text Should Be          xpath://table/tbody/tr[12]/td[2]                                                        ${dynamic code}
    Element Text Should Be          xpath://table/tbody/tr[14]/td[2]                                                        ${level 1}
    Element Text Should Be          xpath://table/tbody/tr[15]/td[2]                                                        ${level 2}
    Element Text Should Be          xpath://table/tbody/tr[16]/td[2]                                                        ${level 3}
    Element Text Should Be          xpath://table/tbody/tr[17]/td[2]                                                        ${sub 1}
    Element Text Should Be          xpath://table/tbody/tr[18]/td[2]                                                        ${sub 2}
    Element Text Should Be          xpath://table/tbody/tr[19]/td[2]                                                        ${sub 3}
    Element Text Should Be          xpath://table/tbody/tr[20]/td[2]                                                        ${dynamic city}
    Element Text Should Be          xpath://table/tbody/tr[21]/td[2]                                                        ${test string}
    Element Text Should Be          xpath://table/tbody/tr[22]/td[2]                                                        ${test number}
    Element Text Should Be          xpath://table/tbody/tr[23]/td[2]                                                        ${keyword}
    Element Text Should Be          xpath://table/tbody/tr[24]/td[2]                                                        ${keyword}
    Click Element                   xpath:${close dialog}
    Sleep                           3 second

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
    Element Text Should Be          xpath://table/tbody/tr[11]/td[2]                                                         ${edit round by}
    Element Text Should Be          xpath://table/tbody/tr[12]/td[2]                                                        ${edit code}
    Element Text Should Be          xpath://table/tbody/tr[14]/td[2]                                                        ${edit level 1}
    Element Text Should Be          xpath://table/tbody/tr[15]/td[2]                                                        ${edit level 2}
    Element Text Should Be          xpath://table/tbody/tr[16]/td[2]                                                        ${edit level 3}
    Element Text Should Be          xpath://table/tbody/tr[17]/td[2]                                                        ${edit sub 1}
    Element Text Should Be          xpath://table/tbody/tr[18]/td[2]                                                        ${edit sub 2}
    Element Text Should Be          xpath://table/tbody/tr[19]/td[2]                                                        ${edit sub 3}
    Element Text Should Be          xpath://table/tbody/tr[20]/td[2]                                                        ${edit city}
    Element Text Should Be          xpath://table/tbody/tr[21]/td[2]                                                        ${edit string}
    Element Text Should Be          xpath://table/tbody/tr[22]/td[2]                                                        ${edit test number}
    Element Text Should Be          xpath://table/tbody/tr[23]/td[2]                                                        ${edit keyword}
    Element Text Should Be          xpath://table/tbody/tr[24]/td[2]                                                        ${edit keyword}
    Click Element                   xpath:${close dialog}
    Sleep                           3 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           2 second
    Goto Sidebar Security Groups
    Sleep                           2 second
    ${permission test group}        Get Row Number      1       Permissions Test
    Click Element                   xpath:(${react table raw})[${permission test group}]${edit security group}
    Click Element                   xpath:${general permission card}
    Clear All General Permissions
    Set General Permission          Catalog     1
    Click Element                   xpath:${settings permission card}
    Clear All Settings Permissions
    Click Element                   xpath:${button submit}
    Sleep                           5 second
    Finish Suite
    Sleep                           3 second
    Start Permission
    Sleep                           2 second
    Goto Sidebar Catalog
    Sleep                           3 second
    ${random string}                Generate Random Name U
    ${edit random string}           Generate Random Name U
    Set Suite Variable              ${random string}
    Set Suite Variable              ${edit random string}