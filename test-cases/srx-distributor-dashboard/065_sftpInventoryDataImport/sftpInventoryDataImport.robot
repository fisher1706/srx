*** Settings ***
Suite Teardown                      Close SFTP Connection And Browser
Suite Setup                         Start Distributor
Library                             Selenium2Library
Library                             String
Library                             OperatingSystem
Library                             String
Library                             Collections
Library                             ../../../resources/py/sftp.py
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Connect To SFTP To Validate
    ${sftp}                         sftpConnect     ${sftp_distributor_user}    ${CURDIR}/../../../resources/my-key
    Set Suite Variable              ${sftp}

Create Product File
    ${product filename}             Generate Random Name U
    Set Suite Variable              ${product filename}
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}.csv          a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v${\n}${product filename},,,${product filename},,,,,,,,,,10,,,,,,,,active

Put Product File By SFTP
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${product filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/import/${product filename}.csv
    Sleep                           5 second

Create InventoryData File To Validate
    ${InventoryData filename}       Generate Random Name U
    Set Suite Variable              ${InventoryData filename}
    Create File                     ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv      a,b,c,d,e${\n}${product filename},123,124,125,stock

Put InventoryData File By SFTP To Validate
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/inventory-data/validate/${InventoryData filename}.csv
    Sleep                           5 second

Get InventoryData File From SFTP To Validate
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/inventory-data/validated/${InventoryData filename}.csv-report    ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv-report

Remove Files To Validate
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv        ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                                      recursive=True

Checking Activity Log To Validate
    Goto Sidebar Activity Feed
    Sleep                           2 second
    Element Text Should Be          xpath:(${react table raw}${react table column})[2]          Import
    Element Text Should Be          xpath:(${react table raw}${react table column})[3]          VALIDATED
    Element Text Should Be          xpath:(${react table raw}${react table column})[5]          USER
    Element Text Should Be          xpath:(${react table raw}${react table column})[6]          SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:(${react table raw}${react table column})[8]          SUCCESS
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     Import
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     VALIDATING
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[5]     USER
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[6]     SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[8]     SUCCESS
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[2]     Import
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[3]     VALIDATE
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[5]     USER
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[6]     SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[8]     SUCCESS

Create InventoryData File To Import
    ${InventoryData filename}       Generate Random Name U
    Set Suite Variable              ${InventoryData filename}
    Create File                     ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv      a,b,c,d,e${\n}${product filename},123,124,125,stock

Put InventoryData File By SFTP To Import
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/inventory-data/import/${InventoryData filename}.csv
    Sleep                           5 second

Get InventoryData File From SFTP To Import
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/inventory-data/imported/${InventoryData filename}.csv-report    ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv-report

Remove Files To Import
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv      ${CURDIR}/../../../resources/generated/${InventoryData filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True

Checking Activity Log To Import
    Reload Page
    Sleep                           2 second
    Element Text Should Be          xpath:(${react table raw}${react table column})[2]          Import
    Element Text Should Be          xpath:(${react table raw}${react table column})[3]          IMPORTED
    Element Text Should Be          xpath:(${react table raw}${react table column})[5]          USER
    Element Text Should Be          xpath:(${react table raw}${react table column})[6]          SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:(${react table raw}${react table column})[8]          SUCCESS
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     Import
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     IMPORTING
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[5]     USER
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[6]     SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[8]     SUCCESS
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[2]     Import
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[3]     IMPORT
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[5]     USER
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[6]     SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[8]     SUCCESS

*** Keywords ***
Close SFTP Connection And Browser
    sftpClose                       ${sftp}
    Close All Browsers