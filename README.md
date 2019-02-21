# SRX Robot

This project contains automation tests using Robot Framework for the SRX platform.

## Project Structure

* **resources** --  using in the tests including resources;
* **test-cases/srx-[portalName]-dashboard/[NNN_testName]/[testName].robot** -- source code of automation test, where NNN in the folder name means test execution order.

#### Using resources

* **resources.robot** -- frequently used keywords;
* **testData.robot** -- main test data.

## Test execution

To run tests by headless browser you need to execute command **-v browser:xvfb**.

Examples of use:
```
robot -v set:pipeline.robot test-cases
```
**email_adm**, **email_dist**, **email_cust** -- emails for *admin*, *distributor* and *customer* portals.

**password_adm**, **password_dist**, **password_cust** -- passwords for *admin*, *distributor* and *customer* portals.

**host_adm**, **host_dist**, **host_cust** -- URLs for *admin*, *distributor* and *customer* portals.

**RFID_SN** -- RFID Serial Number for tests.

**environment** -- can be *dev*, *staging* or *prod*.

**API_key** -- API Key for tests.

**email_perm** -- email for test permissions account.

**password_perm** -- password for test permissions account.