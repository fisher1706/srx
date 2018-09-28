*** Settings ***
Library				XvfbRobot

*** Variables ***
${LOGIN URL}			https://${HOST}/sign-in
${browser}			ff			
${correct wrong email}		example@example.com
${incorrect email}		example.agilevision.io
${element login button}		css:.btn
${static distributor}		css:.table-striped > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(1) > a:nth-child(1)

*** Keywords ***
Login In Distributor Portal
	Start Suite
	Enter Correct Email
	Enter Password
	Correct Submit Login
	Is Warehouse Management

Goto User Managemant
	Login In Distributor Portal
	Click Element		css:.sidebar-items-container > li:nth-child(1) > a:nth-child(1)
	Is User Management

Goto Fees
	Login In Admin Portal
	Click Element		css:li.sidebar-item:nth-child(2) > a:nth-child(1)
	Is Fees Managemant

Goto Admin Users
	Login In Admin Portal
	Click Element		${static distributor}

Login In Admin Portal
	Start Suite
	Enter Correct Email
	Enter Password
	Correct Submit Login
	Is Distributors Page

Enter Correct Email
	Input Text			id:email		${email}

Enter Password
	Input Text			id:password		${password}

Correct Submit Login
	Click Element			${element login button}

Sign Out
	Click Element			xpath:/html/body/div/div/div/div[1]/div/ul/li[4]/a

Start Suite
	Run Keyword If			"${browser}"=="xvbf"	Run Xvbf
	Run Keyword Unless		"${browser}"=="xvbf"	Run Ff
	Set Selenium Implicit Wait	20 second
	Set Selenium Timeout		10 second

Run Xvbf
	Start Virtual Display		1920	1080
	Open Browser			${LOGIN URL}
	Set Window Size			1920	1080

Run Ff
	Open Browser			${LOGIN URL}	ff

Finish Suite
	Close All Browsers

Is Login Page
	Element Text Should Be		xpath:/html/body/div/div/div/div/div/form/div[4]/label		Password

Is Distributors Page
	Element Text Should Be		xpath:/html/body/div/div/div/div[2]/div/div[1]/div/div/h1	Distributor Management
	Element Text Should Be		css:.sidebar-user-info > p:nth-child(2)				${email}

Is Distributor Info
	Element Text Should Be		css:.back-link							Back to Distributors List

Is Fees Managemant
	Element Text Should Be		css:.distributor-management-header > h1:nth-child(1)		Fees Management

Is User Management
	Element Text Should Be		css:.user-management-header > h1:nth-child(1)			User Management

Is Warehouse Management
	Element Text Should Be		css:.warehouse-management-header > h1:nth-child(1)		Warehouse Management
