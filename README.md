# SRX Robot

This project contains automation tests using Robot Framework for the SRX platform.

## Project Structure

* **resources** --  using in the tests including resources;
* **test-cases/[NNN_testName]/[testName].txt** -- source code of automation test, where NNN in the folder name means test execution order.

#### Using resources

* **resources.txt** -- frequently used keywords;
* **testData.txt** -- main test data.

## Test execution

To run tests you need to execute command:
```
pybot -v email:<your_email> -v password:<your_password> -v url:<project_url> [testFolder]
```
Also, you can use a test file instead of a folder:
```
pybot -v email:<your_email> -v password:<your_password> -v url:<project_url> [testName].txt
```
To run tests without using browser you need to execute command ***-v browser:xvbf***.
Examples of use:
```
user@user-PC:~/../../srx-robot/test-cases/001_login$ pybot -v email:example@example.com -v password:qwerty -v url:https://admin-staging.storeroomlogix.com -v browser:xvbf login.txt
```
```
user@user-PC:~/../../srx-robot$ pybot -v email:example@example.com -v password:qwerty -v url:https://admin-staging.storeroomlogix.com -v browser:xvbf test-cases
```