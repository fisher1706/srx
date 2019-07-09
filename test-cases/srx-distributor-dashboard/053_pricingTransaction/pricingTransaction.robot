*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Close SFTP Connection And Browser
Library                             Selenium2Library
Library                             String
Library                             RequestsLibrary
Library                             String
Library                             Collections
Library                             json
Library                             OperatingSystem
Library                             ../../../resources/py/sftp.py
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

***Variables***
${pricing sku}                      PRICING_SKU
${pricing customer}                 Static Customer
${pricing shipto}                   2048
*** Test Cases ***
Connect To SFTP To Validate
    ${sftp}                         sftpConnect     ${sftp_distributor_user}    ${CURDIR}/../../../resources/my-key
    Set Suite Variable              ${sftp}

Create Product File
    ${product filename}             Generate Random Name U
    Set Suite Variable              ${product filename}
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}.csv      a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x${\n}${product filename},,,${product filename},,,,,,,,,,10,,,,,,,,active,1,1

Put Product File By SFTP
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${product filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/products/import/${product filename}.csv
    Sleep                           5 second

Pricing For Customer
    Goto Sidebar Pricing
    Select Pricing Customer         ${pricing customer}
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv      a,b,c,d${\n}${product filename},10,22,2021-12-12T10:15:30
    Sleep                           2 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv
    Sleep                           5 second
    Page Should Contain             Validation status: valid
    Click Element                   xpath:(${dialog}${button})[2]
    Sleep                           10 second
    Remove Files                    ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True
    Sleep                           2 second

Create Location File To Import
    ${location filename}            Generate Random Name U
    Set Suite Variable              ${location filename}
    Create File                     ${CURDIR}/../../../resources/generated/${location filename}.csv      a,b,c,d,e,f,g,j,h,k,l,m,o,p,q,r,s${\n}${product filename},${product filename},,,,,,,${product filename},20,60,RFID,,0,customer,Off,100

Check First List Of Folder
    ${first list}                   sftpListFolder   ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations
    Set Suite Variable              ${first list}

Put Location File By SFTP To Import
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${location filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/import/${location filename}.csv
    Sleep                           5 second

Get Location File From SFTP To Import
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/imported/${location filename}.csv-report    ${CURDIR}/../../../resources/generated/${location filename}.csv-report

Check Second List Of Folder
    ${second list}                  sftpListFolder   ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations
    Set Suite Variable              ${second list}

Compare Folder Lists
    ${new location id}              sftpCompareLists                ${first list}   ${second list}
    Set Suite Variable              ${location id}                  ${new location id}[0]

Create RFID Available File To Validate
    ${rfid filename}                Generate Random Name U
    ${rfid 1}                       Generate Random Name U
    ${rfid 2}                       Generate Random Name U
    Set Suite Variable              ${rfid filename}
    Set Suite Variable              ${rfid 1}
    Set Suite Variable              ${rfid 2}
    Create File                     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      a,b,c${\n}${rfid 1},${product filename},${\n}${rfid 2},${product filename},

Put RFID Available File By SFTP To Validate
    ${putfile}                      sftpPutFile     ${sftp}     ${CURDIR}/../../../resources/generated/${rfid filename}.csv      /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid-available/import/${rfid filename}.csv
    Sleep                           5 second

Get RFID Available File From SFTP To Validate
    ${getfile}                      sftpGetFile     ${sftp}     /srx-data-bucket-${environment}/distributors/${sftp_distributor_user}/customers/${customer_name}_${customer_id}/shipTos/${shipto_name}_${shipto_id}/locations/${location id}/rfid-available/imported/${rfid filename}.csv-report      ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report

Remove Files To Import
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${location filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${location filename}.csv-report
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv
    File Should Not Be Empty        ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report
    Remove Files                    ${CURDIR}/../../../resources/generated/${location filename}.csv      ${CURDIR}/../../../resources/generated/${location filename}.csv-report     ${CURDIR}/../../../resources/generated/${rfid filename}.csv-report      ${CURDIR}/../../../resources/generated/${rfid filename}.csv
    Remove Directory                ${CURDIR}/../../../resources/generated                      recursive=True

Request RFID
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${rfid 1}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Check Transaction
    Goto Sidebar Order Status
    Sleep                           2 second
    Select Transaction Customer Shipto      ${customer_name} - ${shipto_name}
    Sleep                           2 second
    ${my transaction}               Get Row Number      3   ${product filename}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:((${react table raw})[${my transaction}]${react table column})[3]     ${product filename}
    Element Text Should Be          xpath:((${react table raw})[${my transaction}]${react table column})[10]    ACTIVE
    Element Text Should Be          xpath:((${react table raw})[${my transaction}]${react table column})[5]     $0.45
    Click Element                   xpath:(${react table raw})[${my transaction}]${edit transaction}
    Select From Dropdown            ${dialog}${dropdown menu}   DELIVERED
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Pricing For Shipto
    Goto Sidebar Pricing
    Select Pricing Customer         ${pricing customer}
    Select Pricing Shipto           ${pricing shipto}
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Create File                     ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv      a,b,c,d${\n}${product filename},80,22,2021-12-12T10:15:30
    Sleep                           2 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/generated/${product filename}_pricing.csv
    Sleep                           5 second
    Page Should Contain             Validation status: valid
    Click Element                   xpath:(${dialog}${button})[2]
    Sleep                           10 second

Request RFID New
    ${request url rfid}             Get RFID URL
    Create Session                  httpbin                 ${request url rfid}     verify=true
    &{headers}=                     Create Dictionary       Content-Type=application/json
    ${resp}=                        Post Request            httpbin     /issued     data={"reader_name": "reader", "mac_address": "12:12:12:12:12:12", "tag_reads": [{"antennaPort": 1, "epc": "${rfid 2}", "firstSeenTimestamp": "2018-06-14T00:15:54.373293Z", "peakRssi": -50, "isHeartBeat": false }]}    headers=${headers}
    Should Be Equal As Strings      ${resp}                 <Response [200]>

Check Transaction New
    Goto Sidebar Order Status
    Sleep                           2 second
    Select Transaction Customer Shipto      ${customer_name} - ${shipto_name}
    Sleep                           2 second
    ${my transaction}               Get Row Number      3   ${product filename}
    Set Suite Variable              ${my transaction}
    Element Text Should Be          xpath:((${react table raw})[${my transaction}]${react table column})[3]     ${product filename}
    Element Text Should Be          xpath:((${react table raw})[${my transaction}]${react table column})[10]    ACTIVE
    Element Text Should Be          xpath:((${react table raw})[${my transaction}]${react table column})[5]     $3.64
    Click Element                   xpath:(${react table raw})[${my transaction}]${edit transaction}
    Select From Dropdown            ${dialog}${dropdown menu}   DELIVERED
    Click Element                   xpath:${button submit}
    Sleep                           5 second

Delete Location
    [Tags]                          DeleteLocation
    Goto Locations
    ${number of row}                Get Rows Count              ${table xpath}
    Click Element                   xpath:${table xpath}/tbody/tr[${number of row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Simple Table Comparing          Location 1 Name     ${product filename}                 1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Value    ${product filename}                 1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          SKU                 ${product filename}                 1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Type                RFID                                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Critical Min        0                                   1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Min                 20                                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Max                 60                                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

*** Keywords ***
Preparation
    Start Distributor
    Sleep                           5 second
    Goto Sidebar Settings
    Click Element                   id:settings-tab-erp-integration
    Sleep                           1 second
    Click Element                   id:erp-integration-tab-pricing-integration
    Select Radio Button             pricingInfoSettings         SRX
    Sleep                           5 second
    Set Order Status Settings

Close SFTP Connection And Browser
    sftpClose                       ${sftp}
    Close All Browsers