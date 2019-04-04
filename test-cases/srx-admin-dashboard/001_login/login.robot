*** Settings ***
Suite Setup                         Preparation
Suite Teardown                      Finish Suite
Library                             SeleniumLibrary
Resource                            ../../../resources/resource.robot
Resource                            ../../../resources/testData.robot
***Variables***
${page header}                      xpath://div[contains(@class, 'page-header')]

*** Test Cases ***
Invalid Login
    [Tags]                          InvalidLogin
    Click Element                   id:email
    Click Element                   id:password
    Element Should Be Disabled      ${button submit}
    Enter Incorrect Email
    Element Should Be Visible       id:email-helper-text
    Enter Incorrect Password
    Sleep                           1 second
    Element Should Be Disabled      ${button submit}
    Enter Correct Wrong Email
    Sleep                           1 second
    Element Should Be Enabled       ${button submit}
    Click Element                   ${button submit}
    Element Text Should Be          xpath://div/span        Incorrect email address or password.
    Enter Correct Email
    Click Element                   ${button submit}
    Element Text Should Be          xpath://div/span        Incorrect email address or password.
    Clear Element Text              id:password
    Element Should Be Visible       id:password-helper-text
    Sleep                           1 second
    Element Should Be Disabled      ${button submit}

Valid Login
    [Tags]                          ValidLogin
    Clear Element Text              id:email
    Clear Element Text              id:password
    Enter Correct Email
    Enter Correct Password
    Sleep                           3 second
    Click Element                   ${button submit}
    Sleep                           3 second
    Element Text Should Be          ${page header}                                  Distributor Management
    Element Text Should Be          css:.sidebar-user-info > p:nth-child(2)         ${email_adm}
    Sign Out

Forget Password
    [Tags]                          ForgetPassword
    Click Link                      xpath://*[@href="/forgot-password"]
    Is Forgot Password Page
    Enter Incorrect Email
    Sleep                           3 second
    Element Should Be Disabled      ${button submit}
    Enter Correct Wrong Email
    Sleep                           2 second
    Click Element                   ${button submit}
    Sleep                           2 second
    Element Text Should Be          xpath://div/span                                Please check if the entered email address is correct and try again.
    Click Link                      xpath://*[@href="/sign-in"]

*** Keywords ***
Is Forgot Password Page
    Element Text Should Be          xpath:/html/body/div/main/div/div/form/div[2]/a      Go back

Enter Correct Wrong Email
    Input Text                      id:email            ${correct wrong email}

Enter Incorrect Email
    Input Text                      id:email            ${incorrect email}

Enter Correct Email
    Input Text                      id:email            ${email_adm}

Enter Correct Password
    Input Text                      id:password         ${password_adm}

Enter Incorrect Password
    Input Text                      id:password            ${incorrect password}

Preparation
    Start Suite Adv                 https://${host_adm}/sign-in

