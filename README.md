# SRX Robot

This project contains automation tests using Robot Framework for the SRX platform.

## Project Structure

* **resources** --  folder with resources for tests running;
* **test-cases/srx-[portalName]-dashboard/[NNN_testName]/[testName].robot** -- source code of automation tests, where NNN in the folder name means test execution order.

#### Using resources

* **resources.robot** -- frequently used keywords;
* **testData.robot** -- main test data;
* **path.robot** -- frequently used path;
* **py** -- folder with python functions;
* **dev.rovot**, **pipeline.robot** -- files with environment variables.

## Test execution

Examples of use:
```
robot -v set:pipeline.robot test-cases
```

**-v set:[fileName].robot** -- using for select file with environment variables

#### Variables

**${email_adm}** -- email for *admin* portal

**${email_dist}** -- email for *distributor* portal

**${email cust}** -- email for *customer* portal

**${email_perm}** -- email for *distributor* portal by account for permission tests


**${password_adm** -- password for *admin* portal

**${password_dist}** -- password for *distributor* portal

**${password_cust}** -- password for *customer* portal

**${password_perm}** -- password for *distributor* portal by account for permission tests


**${host_adm}** -- URL for *admin* portal

**${host_auth}** -- URL for *auth* portal


**${environment}** -- can be *dev*, *staging* or *prod*

**${browser}** -- can be *ff* (for FireFox), *chrome* (for Google Chrome) or *xvfb* for (headless FireFox)


**${API_key}** -- API Key for tests

**${RFID_SN}** -- RFID Serial Number for tests

**${LOCKER_SN}** -- Locker Serial Number for tests


**${shipto_id}** -- ShipTo ID

**${shipto_name}** -- ShipTo Name

**${customer_id}** -- Customer ID

**${customer_name}** -- Customer Name


**${sftp_distributor_user}** -- SFTP Username for *customer* portal

**${sftp_customer_user}** -- SFTP Username for *distributor* portal
