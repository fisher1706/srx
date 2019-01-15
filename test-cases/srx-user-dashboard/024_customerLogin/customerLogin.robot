*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Reload Customer Page
    Click Element                   xpath:/html/body/div/div/div/div/div/div/button[1]
    Click Element                   css:.select-shipto-button
    Is Customer Portal
    Reload Page
    Is Customer Portal

*** Keywords ***
Preparation
    Start Customer
    Sleep                           2 second