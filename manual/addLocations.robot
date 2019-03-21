*** Settings ***
Suite Teardown                      Close SFTP Connection
Library                             Selenium2Library
Library                             String
Library                             OperatingSystem
Library                             String
Library                             Collections
Library                             ../resources/py/sftp.py
Resource                            ../resources/resource.robot
Resource                            ../resources/testData.robot

*** Variable ***
${set}                              dev.robot
${amount}                           1

*** Test Cases ***
Connect To SFTP
    ${sftp}                         sftpConnect     ${sftp_distributor_user}    ${CURDIR}/../resources/my-key
    Set Suite Variable              ${sftp}

Create Products And Locations
    ${product filename}             Generate Random Name U
    Set Suite Variable              ${product filename}
    ${location filename}            Generate Random Name U
    Set Suite Variable              ${location filename}
    Create File                     ${CURDIR}/../resources/generated/${product filename}.csv        a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r
    Create File                     ${CURDIR}/../resources/generated/${location filename}.csv       a,b,c,d,e,f,g,h,i,j,k,l,m,n
    : FOR   ${index}    IN RANGE    1       ${amount}+1
    \   ${product name}             Generate Random Name U
    \   Append To File              ${CURDIR}/../resources/generated/${product filename}.csv        ${\n}${product name},,,${product name},,,,,,,,,,10,,,,
    \   Append To File              ${CURDIR}/../resources/generated/${location filename}.csv       ${\n}${product name},${product name},,,,,,,${product name},20,30,RFID,,0
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../resources/generated/${product filename}.csv        /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/import/${product filename}.csv
    Sleep                           5 second
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../resources/generated/${location filename}.csv       /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/import/${location filename}.csv
    Sleep                           5 second

*** Keywords ***
Close SFTP Connection
    Remove Directory                ${CURDIR}/../resources/generated    recursive=True
    sftpClose                       ${sftp}