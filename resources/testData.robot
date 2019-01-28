*** Variables ***
${dynamic name}                 Dynamic Test
${dynamic adress1}              Test Street 1
${dynamic adress2}              Test Street 2
${dynamic full adress}          Test Street 1 Test Street 2 Test City AK 14033
${dynamic city}                 Test City
${dynamic email}                dynamic.test@example.com
${dynamic code}                 14033
${static name}                  Static Test
${static adress1}               Baker Street 221b
${static adress2}               Unnamed Street
${static full adress}           Baker Street 221b Unnamed Street CN AK 14033
${static city}                  CN
${static state}                 AK
${static email}                 test@example.com
${static code}                  14033
${edit name}                    Edit Test Name
${edit adress1}                 Edit Adress 1
${edit adress2}                 Edit Adress 2
${edit full adress}             Edit Adress 1 Edit Adress 2 Edit City AL 89000
${edit city}                    Edit City
${edit email}                   edit.test@example.com
${edit code}                    89000
${user first name}              First
${user last name}               Last
${edit first name}              edit first
${edit last name}               edit last
${counter}                      0
${warehouse number}             1137
${edit warehouse number}        2020
${test number}                  5553535
${edit test number}             8800
${distributor contact info}     Last\n14033 5553535\ndynamic.test@example.com
${distributor edit info}        edit last\n89000 8800\nedit.test@example.com
${round by}                     10
${edit round by}                20
${level 1}                      level 1
${level 2}                      level 2
${level 3}                      level 3
${level 4}                      level 4
${sub 1}                        sub 1
${sub 2}                        sub 2
${sub 3}                        sub 3
${sub 4}                        sub 4
${edit level 1}                 edit level 1
${edit level 2}                 edit level 2
${edit level 3}                 edit level 3
${edit level 4}                 edit level 4
${edit sub 1}                   edit sub 1
${edit sub 2}                   edit sub 2
${edit sub 3}                   edit sub 3
${edit sub 4}                   edit sub 4
${keyword}                      keyword
${edit keyword}                 edit keyword
${test string}                  test string
${edit string}                  edit string
${dynamic sku}                  DYNAMIC SKU
${edit sku}                     EDIT SKU
${test number 1}                100
${test number 2}                200 
${test number 3}                300
${test number 4}                400
${test number 5}                500
${edit test number 1}           1000
${edit test number 2}           2000
${edit test number 3}           3000
${edit test number 4}           4000
${edit test number 5}           5000
${test type}                    auto-type
${edit test type}               edit-auto-type
${test del type}                auto-type-del
${edit test del type}           edit-auto-type-del
${year fee}                     4320
${month fee}                    500
${edit year fee}                9000
${edit month fee}               1000
${filter email}                 filter@example.com
${filter first}                 filter first
${filter last}                  filter last
${user email}                   origin.user@example.com
${edit user email}              edituser@example.com
${admin email}                  admin@example.com
${admin edit email}             edit.admin@example.com
${admin first}                  admin first
${admin last}                   admin last
${edit admin first}             edit admin first
${edit admin last}              edit admin last
${market type}                  auto-market
${edit market type}             edit-auto-market
${market del type}              auto-market-del
${edit market del type}         edit-auto-market-del
${locationName}                 testLocName1
${locationValue}                testLocValue1
${minValue}                     20
${maxValue}                     30
${rfid sorting rows}            xpath:${header xpath}/thead/tr/
@{RfidVandTsortingFields}       ${rfid sorting rows}th[1]   ${rfid sorting rows}th[2]   ${rfid sorting rows}th[3]   ${rfid sorting rows}th[4]   ${rfid sorting rows}th[5]
${RfidAssociatedData}           TestDATA
${APIKEY}                       m4DAfPuRurdzlsVrlen2
${security group}               auto-security-group
${edit security group}          auto-edit-security-group
${replenishment email}          replenishment@ukr.net
${simple table}                 //table[contains(@class, 'table')]
${table xpath}                  //table[contains(@class, 'table table-striped table-bordered table-hover table-condensed')]
${header xpath}                 //table[contains(@class, 'table table-hover table-bordered table-condensed')]
${shiptos pane}                 //div[contains(@id, 'customer-details-pane-shiptos')]
${users pane}                   //div[contains(@id, 'customer-details-pane-users')]
${base fee pane}                //div[contains(@id, 'fees-pane-base-fees')]
${button monthly pane}          //div[contains(@id, 'fees-pane-button-monthly-fee')]
${shipto monthly pane}          //div[contains(@id, 'fees-pane-shipto-monthly-fee')]
${label monthly pane}           //div[contains(@id, 'fees-pane-label-monthly-fee')]
${rfid monthly pane}            //div[contains(@id, 'fees-pane-rfid-monthly-fee')]
${deeplens monthly pane}        //div[contains(@id, 'fees-pane-deeplens-monthly-fee')]
${select control}               //div[contains(@class, 'Select-control')]
${select menu outer}            //div[contains(@class, 'Select-menu-outer')]
${select is focused}            //div[contains(@class, 'Select-option is-focused')]
${documents pane}               //div[contains(@id, 'pricing-billing-pane-documents')]
${keys pane}                    //div[contains(@id, 'erp-integration-pane-api-keys')]
${claiming hardware pane}       //div[contains(@id, 'erp-integration-pane-claiming-hardware')]
${taxes pane}                   //div[contains(@id, 'pricing-billing-pane-taxes')]
${transaction submission pane}  //div[contains(@id, 'erp-integration-pane-rl-submit-integration')]
${order close logic}            //div[contains(@id, 'enterprise-workflow-pane-order-close')]
${pricing integrations}         //div[contains(@id, 'erp-integration-pane-pricing-integration')]
${radio button}                 //label[contains(@class, 'select-options')]
${radio button type}            //input[contains(@type, 'radio')]
${customer repl rule}           //div[contains(@id, 'customer-settings-pane-replenishment-rules')]
${customer order close logic}   //div[contains(@id, 'customer-settings-pane-order-close-logic')]
${customer contact info}        //div[contains(@id, 'customer-settings-pane-contact-info')]
${customer cost saving}         //div[contains(@id, 'customer-settings-pane-cost-savings')]
${modal dialog}                 //div[contains(@class, 'modal-dialog')]
${modal title}                  //*[contains(@class, 'modal-title')]
${control button}               //button[contains(@class, 'control-button')]
${button lg}                    //button[contains(@class, 'btn-lg')]
${button danger}                //button[contains(@class, 'btn-danger')]
${button close}                 //button[contains(@class, 'close')]
${button modal dialog ok}       //button[contains(@class, 'modal-dialog-ok-button')]
${button modal dialog cancel}   //button[contains(@class, 'modal-dialog-cancel-button')]
${button info}                  //button[contains(@class, 'btn-info')]
${button primary}               //button[contains(@class, 'btn-primary')]
${button success}               //button[contains(@class, 'btn-success')]
${button default}               //button[contains(@class, 'btn-default')]
${button right margin}          //button[contains(@class, 'button-right-margin')]
${button import}                //button[contains(@class, 'import-button-style')]
${report pricing pane}          //div[contains(@id, 'reports-pane-pricing-report')]
${users pane users}             //div[contains(@id, 'users-pane-users')]
${users pane super users}       //div[contains(@id, 'users-pane-super-users')]
${form control}                 //input[contains(@class, 'form-control')]
${checkbox}                     //div[contains(@class, 'checkbox')]
${checkbox type}                //input[contains(@type, 'checkbox')]
${distributors admin pane}      //div[contains(@id,'distributor-details-pane-2')]
${alert warning}                //div[contains(@class, 'alert-warning')]
${dropdown}                     //span[contains(@class, 'dropdown')]
${dropdown menu item}           //a[contains(@role, 'menuitem')]
${inactive account}             //div[contains(@class, 'inactive-account')]
${sidebar item}                 //li[contains(@class, 'sidebar-item')]
${last page}                    //li[contains(@title, 'last page')]/a
${add rfid button}              //button[contains(text(), "Add RFID")]
${import rfid button}           //button[contains(text(), "Import")]
${help block}                   //span[contains(@class, 'help-block')]
${react table}                  //div[contains(@class, 'rt-table')]
${react table raw}              //div[contains(@class, 'rt-tr-group')]
${react table column}           //div[contains(@class, 'rt-td')]
${expanded react table}         //div[contains(@class, 'Table__expandedContainer')]