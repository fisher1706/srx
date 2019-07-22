*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
SortingDocuments
    [Tags]                          Sorting
    Sorting Column                  1
    Sorting Column                  2
    Sorting Column                  3
    Sorting Column                  5

Documents Filtration
    Filter Field                    1       1       Static Test
    Filter Field                    2       2       aefimenko+test10@agilevision.io

*** Keywords ***
Preparation
    Start Admin
    Sleep                           5 second
    Click Link                      xpath://*[@href="/documents"]
    ${number of row}                Get Rows Count              ${table xpath}
    Set Suite Variable              ${number of row}
