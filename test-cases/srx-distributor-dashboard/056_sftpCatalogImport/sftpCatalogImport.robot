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
    Create File                     ${CURDIR}/../../../resources/generated/${filename}.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r${\n}${filename},,,${filename},,,,,,,,,,10,,,,

Connect To SFTP
    ${sftp}                         sftpConnect     ${sftp_distributor_user}    ${CURDIR}/../../../resources/my-key
    Set Suite Variable              ${sftp}

Put File By SFTP To Validate
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/validate/${filename}.csv
    Sleep                           5 second

Get File From SFTP To Validate
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/validated/${filename}.csv-report    ${CURDIR}/../../../resources/generated/${filename}.csv-report

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
    Create File                     ${CURDIR}/../../../resources/generated/${filename}.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r${\n}${filename},,,${filename},,,,,,,,,,10,,,,

Put File By SFTP To Import
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/import/${filename}.csv
    Sleep                           5 second

Get File From SFTP To Import
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/imported/${filename}.csv-report    ${CURDIR}/../../../resources/generated/${filename}.csv-report

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

Checking Catalog
    Goto Sidebar Catalog
    Click Element                   xpath:${button right margin}
    Input Text                      xpath:(${form control})[1]                      ${filename}
    Click Element                   xpath:${modal dialog}${button primary}
    Sleep                           3 second
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[1]/div      ${filename}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[3]/div      ${filename}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[1]/td[6]/div      10

*** Keywords ***
Close SFTP Connection And Browser
    sftpClose                       ${sftp}
    Close All Browsers