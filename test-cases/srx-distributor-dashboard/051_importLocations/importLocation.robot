*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Library                             String
Library                             Collections
Library                             OperatingSystem
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

***Test Cases***
Import locations
    Create File                     ${CURDIR}/../../../resources/importLocations.csv    a,b,c,d,e,f,g,h,i,j,k,l${\n}Cabinet1,Cabinet_value1,Shelf1,Shelf_value1,Location1,Location_value1,,,CDF,20,30,Button,customer_sku_1
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importLocations.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Reload Page
    Sleep                           5 second

Checking locations
    ${number of row}                Get Rows Count                                                  ${table xpath}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]           Cabinet1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[4]           Cabinet_value1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[5]           Shelf1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[6]           Shelf_value1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[7]           Location1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[8]           Location_value1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[9]           ${EMPTY}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[10]          ${EMPTY}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[11]          CDF
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[12]          customer_sku_1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[13]          BUTTON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[14]          20
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[15]          30

Update Location
    Create File                     ${CURDIR}/../../../resources/updateLocations.csv    a,b,c,d,e,f,g,h,i,j,k,l${\n}Cabinet1,Cabinet_value1,Shelf1,Shelf_value1,Location1,Location_value1,,,CDF,20,30,Button,customer_sku_1
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importLocations.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Reload Page
    Sleep                           5 second

Delete Location
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     Cabinet1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     Cabinet_value1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     Shelf1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     Shelf_value1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]     Location1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]     Location_value1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[10]    CDF
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[11]    customer_sku_1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[12]    BUTTON
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]    20
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    30
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[17]    OFF 
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

**Keywords***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Sidebar Locations
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}