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
    Create File                     ${CURDIR}/../../../resources/importLocations.csv    a,b,c,d,e,f,g,h,i,j,k,l,m,o,p,q,r,s${\n}Cabinet1,Cabinet_value1,Shelf1,Shelf_value1,Location1,Location_value1,,,LOCIMPORT,20,30,Button,customer_sku_1,0,CUSTOMER,Off,110
    Execute Javascript              document.getElementById("file-upload").style.display='block'
    Sleep                           1 second
    Choose File                     id:file-upload                                      ${CURDIR}/../../../resources/importLocations.csv
    Sleep                           5 second
    Element Text Should Be          xpath:${modal title}                                Validation status: valid
    Click Element                   xpath:${button modal dialog ok}
    Sleep                           5 second

Checking locations
    ${number of row}                Get Rows Count                          ${table xpath}
    Simple Table Comparing          Owned by            CUSTOMER            ${number of new row}
    Simple Table Comparing          Location 1 Name     Cabinet1            ${number of new row}
    Simple Table Comparing          Location 1 Value    Cabinet_value1      ${number of new row}
    Simple Table Comparing          Location 2 Name     Shelf1              ${number of new row}
    Simple Table Comparing          Location 2 Value    Shelf_value1        ${number of new row}
    Simple Table Comparing          Location 3 Name     Location1           ${number of new row}
    Simple Table Comparing          Location 3 Value    Location_value1     ${number of new row}
    Simple Table Comparing          SKU                 LOCIMPORT           ${number of new row}
    Simple Table Comparing          Customer SKU        customer_sku_1      ${number of new row}
    Simple Table Comparing          Type                BUTTON              ${number of new row}
    Simple Table Comparing          Min                 20                  ${number of new row}
    Simple Table Comparing          Max                 30                  ${number of new row}
    Simple Table Comparing          Auto Submit         OFF                 ${number of new row}
    Simple Table Comparing          Surplus             OFF                 ${number of new row}
    #Simple Table Comparing          OHI                 110                 ${number of new row}

Delete Location
    Click Element                   xpath:${table xpath}/tbody/tr[${number of new row}]/td[1]/input
    Click Element                   xpath:${button danger}
    Simple Table Comparing          Owned by            CUSTOMER                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Name     Cabinet1                1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 1 Value    Cabinet_value1          1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 2 Name     Shelf1                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 2 Value    Shelf_value1            1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 3 Name     Location1               1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Location 3 Value    Location_value1         1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          SKU                 LOCIMPORT               1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Type                BUTTON                  1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Critical Min        0                       1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Min                 20                      1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
    Simple Table Comparing          Max                 30                      1       ${modal dialog}${simple table}   ${modal dialog}${simple table}
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