*** Settings ***
#Suite Setup                         Preparation
#Suite Teardown                      Finish Suite
Library                             Selenium2Library
Library                             String
Library                             RequestsLibrary
Library                             String
Library                             Collections
Library                             ../../../resources/resource.py
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot

*** Test Cases ***
Connect
    ${sftp}                         sftpConnect     d8528553432042578267dev     /home/provorov/workspace/my-key
    Log To Console                  ${sftp}
    ${file}                         sftpPutFile     ${sftp}     /home/provorov/workspace/2_test.txt     /srx-data-bucket-dev/distributors/d8528553432042578267dev/usage-history/import/2_test.txt
    Log To Console                  ${file}