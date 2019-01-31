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
robot -v password_adm:srx-group -v email_adm:srx-group+dev@agilevision.io -v host_adm:admin-dev.storeroomlogix.com -v email_dist:srx-group+dev-distributor@agilevision.io -v password_dist:srx-group -v host_dist:distributor-dev.storeroomlogix.com -v email_cust:srx-group+dev-customer@agilevision.io -v password_cust:srx-group -v host_cust:customer-dev.storeroomlogix.com -v RFID_SN:RFID230820106808 -v environment:dev -v API_key:m4DAfPuRurdzlsVrlen2 -v email_perm:srx-group+dev-permissions@agilevision.io -v password_perm:srx-group -v browser:xvfb
```
**email_adm**, **email_dist**, **email_cust** -- emails for *admin*, *distributor* and *customer* portals.

**password_adm**, **password_dist**, **password_cust** -- passwords for *admin*, *distributor* and *customer* portals.

**host_adm**, **host_dist**, **host_cust** -- URLs for *admin*, *distributor* and *customer* portals.

**RFID_SN** -- RFID Serial Number for tests.

**environment** -- can be *dev*, *staging* or *prod*.

**API_key** -- API Key for tests.

**email_perm** -- email for test permissions account.

**password_perm** -- password for test permissions account.