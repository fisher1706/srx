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
    Create File                     ${CURDIR}/../../../resources/importLocations.csv    a,b,c,d,e,f,g,h,i,j,k,l,m,o,p,q,r${\n}Cabinet1,Cabinet_value1,Shelf1,Shelf_value1,Location1,Location_value1,,,CDF,20,30,Button,customer_sku_1,0,CUSTOMER,Off
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
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[2]           MOVING
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[3]           CUSTOMER
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[4]           Cabinet1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[5]           Cabinet_value1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[6]           Shelf1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[7]           Shelf_value1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[8]           Location1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[9]           Location_value1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[10]          ${EMPTY}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[11]          ${EMPTY}
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[12]          CDF
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[14]          customer_sku_1
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[15]          BUTTON
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[16]          0
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[17]          20
    Element Text Should Be          xpath:${table xpath}/tbody/tr[${number of row}]/td[18]          30

Delete Location
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[1]     MOVING
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[2]     CUSTOMER
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[3]     Cabinet1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[4]     Cabinet_value1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[5]     Shelf1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[6]     Shelf_value1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[7]     Location1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[8]     Location_value1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[11]    CDF
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[13]    customer_sku_1
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[14]    BUTTON
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[15]    0
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[16]    20
    Element Text Should Be          xpath:${modal dialog}${simple table}/tbody/tr/td[17]    30
    Click Element                   xpath:${modal dialog}${button danger}
    Sleep                           5 second

**Keywords***
Preparation
    Start Distributor
    Sleep                           3 second
    Goto Locations
    Sleep                           5 second
    ${number of row}                Get Rows Count              ${table xpath}
    ${number of new row}=           Evaluate                    ${number of row}+1
    Set Suite Variable              ${number of row}
    Set Suite Variable              ${number of new row}