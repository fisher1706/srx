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
    Create File                     ${CURDIR}/../../../resources/generated/${filename}.txt     ${filename}

Connect To SFTP
    ${sftp}                         sftpConnect     ${sftp_customer_user}    ${CURDIR}/../../../resources/my-key
    Set Suite Variable              ${sftp}

Put File By SFTP
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${filename}.txt      /srx-data-bucket-${environment}/customers/${sftp_customer_user}/shipTos/${shipto_name}_${shipto_id}/discrepancy/input/${filename}.txt
    Sleep                           5 second

Get File From SFTP
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/customers/${sftp_customer_user}/shipTos/${shipto_name}_${shipto_id}/discrepancy/processed/${filename}.txt    ${CURDIR}/../../../resources/generated/${filename}-output.txt

Remove Files
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${filename}.txt
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${filename}-output.txt
    Remove Files                    ${CURDIR}/../../../resources/generated/${filename}.txt      ${CURDIR}/../../../resources/generated/${filename}-output.txt
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True

*** Keywords ***
Close SFTP Connection
    sftpClose                       ${sftp}