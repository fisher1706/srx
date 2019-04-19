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
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v${\n}${product filename},,,${product filename},,,,,,,,,,10,,,,,,,,active

Put Product File By SFTP
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${product filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/import/${product filename}.csv
    Sleep                           5 second

Create Location File To Validate
    ${location filename}            Generate Random Name U
    Set Suite Variable              ${location filename}
    Create File                     ${CURDIR}/../../../resources/generated/${location filename}.csv      a,b,c,d,e,f,g,j,h,k,l,m,o,p,q,r${\n}${product filename},${product filename},,,,,,,${product filename},20,30,RFID,,0,customer,Off

Put Location File By SFTP To Validate
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${location filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/validate/${location filename}.csv
    Sleep                           5 second

Get Location File From SFTP To Validate
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/validated/${location filename}.csv-report    ${CURDIR}/../../../resources/generated/${location filename}.csv-report

Remove Files To Validate
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${location filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${location filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${location filename}.csv      ${CURDIR}/../../../resources/generated/${location filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True

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

Create Location File To Import
    ${location filename}            Generate Random Name U
    Set Suite Variable              ${location filename}
    Create File                     ${CURDIR}/../../../resources/generated/${location filename}.csv      a,b,c,d,e,f,g,j,h,k,l,m,o,p,q,r${\n}${product filename},${product filename},,,,,,,${product filename},20,30,RFID,,0,customer,Off

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

Checking Activity Log To Import
    Reload Page
    Sleep                           2 second
    Element Text Should Be          xpath:(${react table raw}${react table column})[2]          Import
    Element Text Should Be          xpath:(${react table raw}${react table column})[3]          IMPORTED
    Element Text Should Be          xpath:(${react table raw}${react table column})[5]          USER
    Element Text Should Be          xpath:(${react table raw}${react table column})[6]          SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:(${react table raw}${react table column})[8]          SUCCESS
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     Location
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     LOCATION_CREATE
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[8]     SUCCESS
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[2]     Import
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[3]     IMPORTING
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[5]     USER
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[6]     SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:((${react table raw})[3]${react table column})[8]     SUCCESS
    Element Text Should Be          xpath:((${react table raw})[4]${react table column})[2]     Import
    Element Text Should Be          xpath:((${react table raw})[4]${react table column})[3]     IMPORT
    Element Text Should Be          xpath:((${react table raw})[4]${react table column})[5]     USER
    Element Text Should Be          xpath:((${react table raw})[4]${react table column})[6]     SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:((${react table raw})[4]${react table column})[8]     SUCCESS

Delete Location
    Goto Locations
    Sleep                           5 second
    ${my location}                  Get Row By Text             ${table xpath}      12      ${product filename}
    Click Element                   xpath:${table xpath}/tbody/tr[${my location}]/td[1]
    Click Element                   xpath:${button danger}
    Simple Table Comparing          Location 1 Name     ${product filename}             1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Value    ${product filename}             1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          SKU                 ${edit sku}                     1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Type                RFID                            1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Critical Min        0                               1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Min                 20                              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Max                 30                              1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

*** Keywords ***
Close SFTP Connection And Browser
    sftpClose                       ${sftp}
    Close All Browsers