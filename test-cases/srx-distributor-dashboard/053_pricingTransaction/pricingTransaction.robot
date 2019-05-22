*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Close SFTP Connection And Browser
Library                             Selenium2Library
Library                             String
Library                             RequestsLibrary
Library                             String
Library                             Collections
Library                             json
Library                             OperatingSystem
Library                             ../../../resources/py/sftp.py
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

***Variables***
${pricing sku}                      PRICING_SKU
${pricing customer}                 Static Customer
${pricing shipto}                   2048
*** Test Cases ***
Connect To SFTP To Validate
    ${sftp}                         sftpConnect     ${sftp_distributor_user}    ${CURDIR}/../../../resources/my-key
    Set Suite Variable              ${sftp}

Create Product File
    ${product filename}             Generate Random Name U
    Set Suite Variable              ${product filename}
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v${\n}${product filename},,,${product filename},,,,,,,,,,10,,,,,,,,active

Put Product File By SFTP
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${product filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/import/${product filename}.csv
    Sleep                           5 second

Pricing For Customer
    Goto Sidebar Pricing
    Choose From Select Box          (${select control})[1]      ${pricing customer}
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv      a,b,c,d${\n}${product filename},10,22,2021-12-12T10:15:30
    Sleep                           2 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second
    Remove Files                    ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True
    Sleep                           2 second

Create Location File To Import
    ${location filename}            Generate Random Name U
    Set Suite Variable              ${location filename}
    Create File                     ${CURDIR}/../../../resources/generated/${location filename}.csv      a,b,c,d,e,f,g,j,h,k,l,m,o,p,q,r${\n}${product filename},${product filename},,,,,,,${product filename},20,60,LOCKER,,0,customer,Off

Put Location File By SFTP To Import
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${location filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/import/${location filename}.csv
    Sleep                           5 second

Get Location File From SFTP To Import
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/imported/${location filename}.csv-report    ${CURDIR}/../../../resources/generated/${location filename}.csv-report

Remove Files To Import
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${location filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${location filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${location filename}.csv      ${CURDIR}/../../../resources/generated/${location filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True

Request Locker
    [Tags]          Locker
    ${request url locker}           Get Locker URL
    Create Session                  httpbin                 ${request url locker}        verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin    /        data={ "currentWeight": 0, "distributorSku": "${product filename}", "kioskId": "${shipto_id}", "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": 210, "quantityRequested": 10, "timestamp": "2018-10-30T11:22:48.806", "transactionStatus": "Issued", "weightOfProduct": 0, "user":"qweqwewe" }    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Check Transactions
    Sleep                           5 second
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           1 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      3   ${product filename}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${product filename}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[10]     ACTIVE
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[5]      $0.45
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            DELIVERED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Pricing For Shipto
    Goto Sidebar Pricing
    Choose From Select Box          (${select control})[1]      ${pricing customer}
    Choose From Select Box          (${select control})[2]      ${pricing shipto}
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv      a,b,c,d${\n}${product filename},80,22,2021-12-12T10:15:30
    Sleep                           2 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           10 second

Request Locker New
    [Tags]          Locker
    ${request url locker}           Get Locker URL
    Create Session                  httpbin                 ${request url locker}        verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin    /        data={ "currentWeight": 0, "distributorSku": "${product filename}", "kioskId": "${shipto_id}", "lastWeight": 0, "location1": 1, "location2": 11, "location3": 111, "lockerId": 9999, "quantityIssued": 100, "quantityRequested": 10, "timestamp": "2019-03-04T11:22:48.806", "transactionStatus": "Issued", "weightOfProduct": 0, "user":"qweqwewe" }    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Check Transactions New
    Sleep                           5 second
    Goto Sidebar Order Status
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Click Element                   xpath:${header xpath}/thead/tr/th[9]
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${my transaction}               Get Row By Text     ${table xpath}      3   ${product filename}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[3]      ${product filename}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${my transaction}]/td[5]      $3.64
    Click Element                   xpath:${table xpath}/tbody/tr[${my transaction}]${button success}
    Choose From Select Box          ${modal dialog}${select control}            DELIVERED
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Delete Location
    [Tags]                          DeleteLocation
    Goto Locations
    ${number of row}                Get Rows Count              ${table xpath}
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Simple Table Comparing          Location 1 Name     ${product filename}                 1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Value    ${product filename}                 1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          SKU                 ${product filename}                 1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Type                LOCKER                              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Critical Min        0                                   1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Min                 20                                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Max                 60                                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           5 second
    Goto Sidebar Settings
    Click Element                   id:settings-tab-erp-integration
    Sleep                           1 second
    Click Element                   id:erp-integration-tab-pricing-integration
    Select Radio Button             pricingInfoSettings         SRX
    Sleep                           5 second
    Set Order Status Settings

Close SFTP Connection And Browser
    sftpClose                       ${sftp}
    Close All Browsers