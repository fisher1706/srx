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
Create File To Upload To Validate
    ${filename}                     Generate Random Name U
    Set Suite Variable              ${filename}
    Create File                     ${CURDIR}/../../../resources/generated/${filename}.csv      a,b,c,d${\n}PRICING_SKU,10,EACH,2023-12-12T10:15:30

Connect To SFTP
    ${sftp}                         sftpConnect     ${sftp_distributor_user}    ${CURDIR}/../../../resources/my-key
    Set Suite Variable              ${sftp}

Put File By SFTP To Validate
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/product-prices/validate/${filename}.csv
    Sleep                           8 second

Get File From SFTP To Validate
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/product-prices/validated/${filename}.csv-report      ${CURDIR}/../../../resources/generated/${filename}.csv-report

Remove Files To Validate
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${filename}.csv      ${CURDIR}/../../../resources/generated/${filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True

Checking Activity Log To Validate
    Goto Sidebar Activity Feed
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

Create File To Upload To Import
    ${filename}                     Generate Random Name U
    Set Suite Variable              ${filename}
    Create File                     ${CURDIR}/../../../resources/generated/${filename}.csv      a,b,c,d${\n}PRICING_SKU,10,M,2023-12-12T10:15:30

Put File By SFTP To Import
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/product-prices/import/${filename}.csv
    Sleep                           8 second

Get File From SFTP To Import
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/product-prices/imported/${filename}.csv-report      ${CURDIR}/../../../resources/generated/${filename}.csv-report

Remove Files To Import
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${filename}.csv      ${CURDIR}/../../../resources/generated/${filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True

Checking Activity Log To Import
    Reload Page
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

Checking Pricing Table
    Goto Sidebar Pricing
    Select Pricing Customer         ${customer_name}
    Select Pricing Shipto           ${shipto_name}
    Filter Add                      1       1       ${filename}

*** Keywords ***
Close SFTP Connection And Browser
    sftpClose                       ${sftp}
    Close All Browsers