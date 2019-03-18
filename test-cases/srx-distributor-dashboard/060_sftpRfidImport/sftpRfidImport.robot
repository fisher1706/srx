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
Connect To SFTP
    ${sftp}                         sftpConnect     ${sftp_distributor_user}    ${CURDIR}/../../../resources/my-key
    Set Suite Variable              ${sftp}

Create Product File
    ${product filename}             Generate Random Name U
    Set Suite Variable              ${product filename}
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r${\n}${product filename},,,${product filename},,,,,,,,,,10,,,,

Put Product File By SFTP
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${product filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/import/${product filename}.csv
    Sleep                           5 second

Check First List Of Folder
    ${first list}                   sftpListFolder   ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations
    Set Suite Variable              ${first list}

Create Location File
    ${location filename}            Generate Random Name U
    Set Suite Variable              ${location filename}
    Create File                     ${CURDIR}/../../../resources/generated/${location filename}.csv      a,b,c,d,e,f,g,j,h,k,l,m,o,p${\n}${product filename},${product filename},,,,,,,${product filename},20,30,RFID,,0

Put Location File By SFTP
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${location filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/import/${location filename}.csv
    Sleep                           5 second

Check Second List Of Folder
    ${second list}                  sftpListFolder   ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations
    Set Suite Variable              ${second list}

Compare Folder Lists
    ${new location id}              sftpCompareLists                ${first list}   ${second list}
    Set Suite Variable              ${location id}                  ${new location id}[0]

Create RFID File To Validate
    ${rfid filename}                Generate Random Name U
    Set Suite Variable              ${rfid filename}
    Create File                     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      RFID${\n}${rfid filename}

Put RFID File By SFTP To Validate
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid/validate/${rfid filename}.csv
    Sleep                           5 second

Get RFID File From SFTP To Validate
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid/validated/${rfid filename}.csv-report      ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Remove RFID Files To Validate
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${rfid filename}.csv         ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Checking Activity Log RFID To Validate
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

Create RFID File To Import
    ${rfid filename}                Generate Random Name U
    Set Suite Variable              ${rfid filename}
    Create File                     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      RFID${\n}${rfid filename}

Put RFID File By SFTP To Import
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid/import/${rfid filename}.csv
    Sleep                           5 second

Get RFID File From SFTP To Import
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid/imported/${rfid filename}.csv-report      ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Remove RFID Files To Import
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${rfid filename}.csv         ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Checking Activity Log RFID To Import
    Reload Page
    Sleep                           3 second
    Element Text Should Be          xpath:(${react table raw}${react table column})[2]          Import
    Element Text Should Be          xpath:(${react table raw}${react table column})[3]          IMPORTED
    Element Text Should Be          xpath:(${react table raw}${react table column})[5]          USER
    Element Text Should Be          xpath:(${react table raw}${react table column})[6]          SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:(${react table raw}${react table column})[8]          SUCCESS
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     RFID
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     RFID_TAG_ASSIGN
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[4]     Import CSV
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[5]     JOB
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

Create RFID Available File To Validate
    ${rfid filename}                Generate Random Name U
    Set Suite Variable              ${rfid filename}
    Create File                     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      a,b,c${\n}${rfid filename},${product filename},

Put RFID Available File By SFTP To Validate
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid-available/validate/${rfid filename}.csv
    Sleep                           5 second

Get RFID Available File From SFTP To Validate
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid-available/validated/${rfid filename}.csv-report      ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Remove RFID Available Files To Validate
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${rfid filename}.csv         ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Checking Activity Log RFID Available To Validate
    Reload Page
    Sleep                           3 second
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

Create RFID Available File To Import
    ${rfid filename}                Generate Random Name U
    Set Suite Variable              ${rfid filename}
    Create File                     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      a,b,c${\n}${rfid filename},${product filename},

Put RFID Available File By SFTP To Import
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid-available/import/${rfid filename}.csv
    Sleep                           5 second

Get RFID Available File From SFTP To Import
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid-available/imported/${rfid filename}.csv-report      ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Remove RFID Available Files To Import
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${rfid filename}.csv         ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Checking Activity Log RFID Available To Import
    Reload Page
    Sleep                           3 second
    Element Text Should Be          xpath:(${react table raw}${react table column})[2]          Import
    Element Text Should Be          xpath:(${react table raw}${react table column})[3]          IMPORTED
    Element Text Should Be          xpath:(${react table raw}${react table column})[5]          USER
    Element Text Should Be          xpath:(${react table raw}${react table column})[6]          SFTP user: ${sftp_distributor_user}
    Element Text Should Be          xpath:(${react table raw}${react table column})[8]          SUCCESS
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[2]     RFID
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[3]     RFID_TAG_IMPORTAVAILABLE
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[4]     Import CSV
    Element Text Should Be          xpath:((${react table raw})[2]${react table column})[5]     JOB
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
    Goto Sidebar Locations
    Sleep                           2 second
    ${my location}                  Get Row By Text             ${table xpath}      11      ${product filename}
    Click Element                   xpath:${table xpath}/tbody/tr[${my location}]/td[1]
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     ${product filename}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     ${product filename}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]    ${product filename}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[12]    RFID
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]    0
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    20
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]    30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[18]    OFF
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

*** Keywords ***
Close SFTP Connection And Browser
    sftpClose                       ${sftp}
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True
    Close All Browsers