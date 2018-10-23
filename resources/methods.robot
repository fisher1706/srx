*** Keywords ***
Go to homepage
    Open Browser        ${HOMEPAGE}        ${BROWSER}
    Login to site

Login to site
    Input Text      id=email        ${USEREMAIL}
    Input Text      id=password     ${USERPASSWORD}
    Sleep       2 seconds
    Click Element      xpath://*[@id="root"]/div/div/div/div/form/div[5]/div[2]/button
    Sleep       5 seconds
