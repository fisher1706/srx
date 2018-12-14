# SRX Robot

This project contains automation tests using Robot Framework for the SRX platform.

## Project Structure

* **resources** --  using in the tests including resources;
* **test-cases/srx-[portalName]-dashboard/[NNN_testName]/[testName].robot** -- source code of automation test, where NNN in the folder name means test execution order.

#### Using resources

* **resources.robot** -- frequently used keywords;
* **testData.robot** -- main test data.

## Test execution

To run tests you need to execute command:
```
robot -v email:<your_email> -v password:<your_password> -v HOST:<project_url> [testFolder]
```
Also, you can use a test file instead of a folder:
```
robot -v email:<your_email> -v password:<your_password> -v HOST:<project_url> [testName].robot
```
To run tests by headless browser you need to execute command ***-v browser:xvfb***.

Examples of use:
```
user@user-PC:~/../../srx-robot/test-cases/srx-admin-dashboard/001_login$ robot -v email:example@example.com -v password:qwerty -v HOST:admin-staging.storeroomlogix.com -v browser:xvfb login.robot
```
```
user@user-PC:~/../../srx-robot$ robot -v email:example@example.com -v password:qwerty -v HOST:admin-staging.storeroomlogix.com -v browser:xvfb test-cases/srx-admin-dashboard
```