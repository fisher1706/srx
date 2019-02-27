*** Settings ***
Suite Setup                             Preparation
Suite Teardown                          Finish Suite
Library                                 SeleniumLibrary
Resource                                ../../../resources/resource.robot
Resource                                ../../../resources/testData.robot

*** Variable ***
*** Test Cases ***
Notification Settings
    [Tags]                              Notification Settings
    Goto Notification Settings
    UnSelect all Checkboxes
    Click Element                       xpath:(${customer settings notify}${checkbox type})[1]
    Click Element                       xpath:(${customer settings notify}${checkbox type})[4]
    Click Element                       xpath:(${customer settings notify}${checkbox type})[5]
    Click Element                       xpath:(${customer settings notify}${checkbox type})[7]
    Click Element                       xpath:(${customer settings notify}${radio button type})[1]
    Click Element                       xpath:${customer settings notify}${button primary}
    Reload Page
    Sleep                               5 second
    Click Element                       id:settings-tab-notification-settings
    Checkbox Should Be Selected         xpath:(${customer settings notify}${checkbox type})[1]
    Checkbox Should Be Selected         xpath:(${customer settings notify}${checkbox type})[4]
    Checkbox Should Be Selected         xpath:(${customer settings notify}${checkbox type})[5]
    Checkbox Should Be Selected         xpath:(${customer settings notify}${checkbox type})[7]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[2]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[3]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[6]
    Radio Button Should Be Set To       freqTimes    AFTER_FIVE_MINUTES
    Goto Notification Settings
    UnSelect all Checkboxes
    Click Element                       xpath:(${customer settings notify}${checkbox type})[2]
    Click Element                       xpath:(${customer settings notify}${checkbox type})[3]
    Click Element                       xpath:(${customer settings notify}${checkbox type})[6]
    Click Element                       xpath:(${customer settings notify}${radio button type})[2]
    Click Element                       xpath:${customer settings notify}${button primary}
    Reload Page
    Sleep                               5 second
    Click Element                       id:settings-tab-notification-settings
    Checkbox Should Be Selected         xpath:(${customer settings notify}${checkbox type})[2]
    Checkbox Should Be Selected         xpath:(${customer settings notify}${checkbox type})[3]
    Checkbox Should Be Selected         xpath:(${customer settings notify}${checkbox type})[6]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[1]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[4]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[5]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[7]
    Radio Button Should Be Set To       freqTimes    TWICE_A_DAY
    Goto Notification Settings
    UnSelect all Checkboxes
    Click Element                       xpath:(${customer settings notify}${checkbox type})[5]
    Click Element                       xpath:(${customer settings notify}${radio button type})[3]
    Click Element                       xpath:${customer settings notify}${button primary}
    Reload Page
    Sleep                               5 second
    Click Element                       id:settings-tab-notification-settings
    Checkbox Should Be Selected         xpath:(${customer settings notify}${checkbox type})[5]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[1]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[2]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[3]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[4]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[6]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[7]
    Radio Button Should Be Set To       freqTimes    DAILY_AT_12PM
    Goto Notification Settings
    Click Element                       xpath:(${customer settings notify}${radio button type})[4]
    Click Element                       xpath:${customer settings notify}${button primary}
    Reload Page
    Sleep                               5 second
    Click Element                       id:settings-tab-notification-settings
    Radio Button Should Be Set To       freqTimes    DAILY_AT_8AM
    Goto Notification Settings
    Click Element                       xpath:(${customer settings notify}${radio button type})[5]
    Click Element                       xpath:${customer settings notify}${button primary}
    Reload Page
    Sleep                               5 second
    Click Element                       id:settings-tab-notification-settings
    Radio Button Should Be Set To       freqTimes    DAILY_AT_2PM
    UnSelect all Checkboxes


*** Keywords ***
Preparation
    Start Customer
    Sleep                               2 second
    Click Element                       xpath:(${list group}${shipto})[1]
    Click Element                       css:.select-shipto-button
    Is Customer Portal
    Click Element                       xpath:(${sidebar item})[3]
    Sleep                               3 second

Goto Notification Settings
    Click Element                       id:settings-tab-notification-settings

UnSelect all Checkboxes
    Unselect Checkbox                   xpath:(${customer settings notify}${checkbox type})[1]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[1]
    Unselect Checkbox                   xpath:(${customer settings notify}${checkbox type})[2]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[2]
    Unselect Checkbox                   xpath:(${customer settings notify}${checkbox type})[3]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[3]
    Unselect Checkbox                   xpath:(${customer settings notify}${checkbox type})[4]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[4]
    Unselect Checkbox                   xpath:(${customer settings notify}${checkbox type})[5]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[5]
    Unselect Checkbox                   xpath:(${customer settings notify}${checkbox type})[6]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[6]
    Unselect Checkbox                   xpath:(${customer settings notify}${checkbox type})[7]
    Checkbox Should Not Be Selected     xpath:(${customer settings notify}${checkbox type})[7]