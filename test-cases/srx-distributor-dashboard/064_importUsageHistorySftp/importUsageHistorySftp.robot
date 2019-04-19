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

Create Usage History File To Validate
    ${UH filename}                  Generate Random Name U
    Set Suite Variable              ${UH filename}
    Create File                     ${CURDIR}/../../../resources/generated/${UH filename}.csv      a,b,c,d,e,f,g${\n}${UH filename},${customer_name},${shipto_name},${shipto_id},USAGE HISTORY,50,2018/12/30 10:15:30

Put Usage History File By SFTP To Validate
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${UH filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/usage-history/validate/${UH filename}.csv
    Sleep                           5 second

Get Usage History File From SFTP To Validate
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/usage-history/validated/${UH filename}.csv-report    ${CURDIR}/../../../resources/generated/${UH filename}.csv-report

Remove Files To Validate
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${UH filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${UH filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${UH filename}.csv           ${CURDIR}/../../../resources/generated/${UH filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                              recursive=True

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

Create Usage History File To Import
    ${UH filename}                  Generate Random Name U
    Set Suite Variable              ${UH filename}
    Create File                     ${CURDIR}/../../../resources/generated/${UH filename}.csv           a,b,c,d,e,f,g${\n}${UH filename},${customer_name},${shipto_name},${shipto_id},USAGE HISTORY,50,2018/12/30 10:15:30

Put Usage History File By SFTP To Import
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${UH filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/usage-history/import/${UH filename}.csv
    Sleep                           5 second

Get Usage Historyn File From SFTP To Import
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/usage-history/imported/${UH filename}.csv-report    ${CURDIR}/../../../resources/generated/${UH filename}.csv-report

Remove Files To Import
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${UH filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${UH filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${UH filename}.csv           ${CURDIR}/../../../resources/generated/${UH filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                              recursive=True

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