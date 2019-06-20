*** Variable ***
${button submit}                //button[contains(@type, 'submit')]
${dropdown menu}                //input[contains(@aria-autocomplete, 'list')]
${close dialog}                 //button[contains(@aria-label, 'Close')]
${delete customer}              //button[contains(@title, 'Delete Customer')]
${delete shipto}                //button[contains(@title, 'Delete Shipto')]
${delete user}                  //button[contains(@title, 'Delete User')]
${delete fob}                   //button[contains(@title, 'Delete FOB')]
${edit user}                    //button[contains(@title, 'Edit User')]
${edit status}                  //button[contains(@title, 'Edit status')]
${customer info}                //button[contains(@title, 'Customer info')]
${user info}                    //button[contains(@title, 'User info')]
${unassign rfid}                //button[contains(@title, 'Unassign')]
${edit transaction}             //button[contains(@title, 'Edit Transaction')]
${tab element}                  //button[contains(@role, 'tab')]
${dialog tab}                   //a[contains(@role, 'tab')]
${menu}                         //ul[contains(@role, 'menu')]
${menu item}                    //li[contains(@role, 'menuitem')]
${text field}                   //input[contains(@type, 'text')]
${button filter}                //span[text()='Add filter']/..
${button}                       //button[contains(@type, 'button')]
${listbox}                      //ul[contains(@role, 'listbox')]
${alert dialog}                 //div[contains(@role, 'alertdialog')]
${create button}                id:item-action-create
${filter type}                  //div[contains(@data-type, 'filter')]
${dialog}                       //div[contains(@role, 'dialog')]
${role button}                  //div[contains(@role, 'button')]
${edit}                         //button[contains(@title, 'edit')]
${expanded not}                 //div[contains(@aria-expanded, 'false')]
${srx select}                   //div[contains(@class, 'srx-select')]
${react modal dialog}           //div[contains(@data-testid, 'modal-dialog')]
${select control}               ${srx select}/div/div
${tab pane}                     //div[contains(@role, 'tabpanel')]
${selector shipto}              //div[contains(@id, 'rfid-select-shipto')]/div
${selector sku}                 //div[contains(@id, 'rfid-select-sku')]/div
${selector customer pricing}    //div[contains(@id, 'pricing-select-customer')]/div
${selector customer shpto}      //div[contains(@id, 'pricing-select-shipto')]/div
${selector transactions}        //div[contains(@id, 'transaction-select-shipto')]/div
${confirm button}               //button[@data-testid='confirm-button']
${columnheader}                 //div[@role='columnheader']