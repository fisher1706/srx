*** Settings ***
Suite Teardown                      Close SFTP Connection And Browser
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
    Log To Console                  ${first list}

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
    Log To Console                  ${second list}

Compare Folder Lists
    ${new location id}              sftpCompareLists                ${first list}   ${second list}
    Log To Console                  ${new location id}

*** Keywords ***
Close SFTP Connection And Browser
    sftpClose                       ${sftp}
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True
    Close All Browsers