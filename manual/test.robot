*** Settings ***
Library                             String
Library                             OperatingSystem

*** Test Cases ***
Create File To Upload To Validate Less
    Create File                     ${CURDIR}/../resources/generated/1.csv      ${EMPTY}