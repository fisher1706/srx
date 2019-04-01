*** Settings ***
Suite Teardown                      Close SFTP Connection
Library                             Selenium2Library
Library                             String
Library                             OperatingSystem
Library                             String
Library                             Collections
Library                             ../../../resources/py/sftp.py
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Create File To Upload
    ${filename}                     Generate Random Name U
    Set Suite Variable              ${filename}
    Create File                     ${CURDIR}/../../../resources/generated/${filename}.csv     a,b,c${\n}1,2,3

Connect To SFTP
    ${sftp}                         sftpConnect     ${sftp_distributor_user}    ${CURDIR}/../../../resources/my-key
    Set Suite Variable              ${sftp}

Put File By SFTP
    #${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/usage-history/import/${filename}.csv
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/usage-history/import/${filename}.csv
    Sleep                           5 second

Get File From SFTP
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/usage-history/imported/${filename}.csv-report    ${CURDIR}/../../../resources/generated/${filename}.csv-report

Remove Files
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${filename}.csv      ${CURDIR}/../../../resources/generated/${filename}.csv-report
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True

*** Keywords ***
Close SFTP Connection
    sftpClose                       ${sftp}