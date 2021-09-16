# How this Page Works:

## Getting Cookies for DOE login page
-------------------------------------------------------
```HTTP 
GET /home/login
Host: healthscreening.schools.nyc
Cookie: ai_user=<TIME> _ga=<NO CLUE> ; _gid=<NO CLUE>
```
```HTTP 
RESPONCE /home/login
Host: healthscreening.schools.nyc
RESPONCE: HTTP/1.1 302 Found 
Location: https://idp.nycenet.edu/mga/sps/oauth/oauth20/authorize?client_id=<REDACTED>&redirect_uri=https%3A%2F%2Fhealthscreening.schools.nyc%2Fauthorization-code%2Fcallback&response_type=code%20id_token&scope=openid%20profile&response_mode=form_post&nonce=<REDACTED>&state=<REDACTED>&x-client-SKU=ID_NETSTANDARD2_0&x-client-ver=5.5.0.0
Set-Cookie: .AspNetCore.OpenIdConnect.Nonce.<RANDOM B64 BLOB>=N
Set-Cookie: .AspNetCore.Correlation.OpenIdConnect.<RANDOM B64 BLOB>=N;
```


```HTTP 
GET /mga/sps/oauth/oauth20/authorize?client_id=<REDACTED>&redirect_uri=https%3A%2F%2Fhealthscreening.schools.nyc%2Fauthorization-code%2Fcallback&response_type=code%20id_token&scope=openid%20profile&response_mode=form_post&nonce=<REDACTED>&state=<REDACTED>&x-client-SKU=ID_NETSTANDARD2_0&x-client-ver=5.5.0.0
Host: idp.nycenet.edu
Cookie: NONE
```

```HTTP 
RESPONCE /mga/sps/oauth/oauth20/authorize?client_id=<REDACTED>&redirect_uri=https%3A%2F%2Fhealthscreening.schools.nyc%2Fauthorization-code%2Fcallback&response_type=code%20id_token&scope=openid%20profile&response_mode=form_post&nonce=<REDACTED>&state=<REDACTED>&x-client-SKU=ID_NETSTANDARD2_0&x-client-ver=5.5.0.0
Location: /mga/sps/auth
Set-Cookie: AMWEBJCT!%2Fmga!JSESSIONID=<RANDOM B64 BLOB>
Set-Cookie: BIGipServerPR_IDP_NYCENET_EDU_POOL=000000000.00000.0000  # These numbers have been changed
```

```HTTP 
GET /mga/sps/auth 
Host: idp.nycenet.edu
Cookie: AMWEBJCT!%2Fmga!JSESSIONID=<RANDOM B64 BLOB>; BIGipServerPR_IDP_NYCENET_EDU_POOL=000000000.00000.0000  # These numbers have been changed
```
```HTTP 
RESPONE /mga/sps/auth 
Host: idp.nycenet.edu
Set-Cookie: PD-S-SESSION-ID=<REDACTED>
```
*This is the DOE login page, work done before this was to get the correct cookies*

## After Entering Credentials
-------------------------------------------------------
```HTTP 
POST /pkmslogin.form?token=Unknown HTTP/1.1
Host: idp.nycenet.edu
Cookie: AMWEBJCT!%2Fmga!JSESSIONID=<RANDOM B64 BLOB > ; BIGipServerPR_IDP_NYCENET_EDU_POOL=000000000.00000.0000; PD-S-SESSION-ID=<REDACTED>
POST-DATA : vusername=<USERNAME>&password=<PASSWORD>&login-form-type=pwd&username=<USERNAME>
```
```HTTP 
RESPONCE /pkmslogin.form?token=Unknown HTTP/1.1
Host: idp.nycenet.edu
HTTP/1.1 302 Moved Temporarily
Set-Cookie: PD-S-SESSION-ID=<NEW BLOB>
location: https://idp.nycenet.edu/mga/sps/auth
```


```HTTP 
GET /mga/sps/auth HTTP/1.1
Host: idp.nycenet.edu
Cookie: AMWEBJCT!%2Fmga!JSESSIONID=<RANDOM>; BIGipServerPR_IDP_NYCENET_EDU_POOL=000000000.00000.0000; PD-S-SESSION-ID=<NEW BLOB>
```

```HTTP 
RESPONEC /mga/sps/auth HTTP/1.1
Host: idp.nycenet.edu
```
*3 KEYS TO THE KINGDOM- Code, state, id_token*

## Redeeming Cookies at `/authorization-code/callback`
-------------------------------------------------------

```HTTP 
POST /authorization-code/callback HTTP/1.1
Host: healthscreening.schools.nyc
Cookie: .AspNetCore.OpenIdConnect.Nonce.<RANDOM B64 BLOB>=N; .AspNetCore.Correlation.OpenIdConnect.<RANDOM B64 BLOB>=N;
POST-DATA : code=<code>&id_token=<id_token>&state=<state>
```
*Data posted here is from the keys to the kingdom*

```HTTP 
RESPONCE /authorization-code/callback HTTP/1.1
Host: healthscreening.schools.nyc
HTTP/1.1 302 Found
Location: /home/login
Set-Cookie: .AspNetCore.Correlation.OpenIdConnect.<BLOB>=
Set-Cookie: .AspNetCore.OpenIdConnect.Nonce.<BLOB>=
Set-Cookie: .AspNetCore.Cookies=chunks-2
Set-Cookie: .AspNetCore.CookiesC1=< MASSIVE BLOB>
Set-Cookie: .AspNetCore.CookiesC2=< SMALLER BLOB>
```

## Back to login with new cookies 
--------------------------------------------------
```HTTP
GET /home/login HTTP/1.1
Host: healthscreening.schools.nyc
Cookies: .AspNetCore.Cookies=chunks-2; .AspNetCore.CookiesC1=<MASSIVE BLOB>; .AspNetCore.CookiesC2=<SMALLER BLOB>
```
```HTTP
RESPONCE /home/login HTTP/1.1
Host: healthscreening.schools.nyc
HTTP/1.1 302 Found
Location: /
```

```HTTP 
GET / HTTP/1.1
Cookies: .AspNetCore.Cookies=chunks-2; .AspNetCore.CookiesC1=<MASSIVE BLOB>; .AspNetCore.CookiesC2=<SMALLER BLOB>
```

```HTTP 
RESPONCE / HTTP/1.1
Set-Cookie: .AspNetCore.Antiforgery.<REDACTED>=<BLOB>
```

## Logged in and submit the form 
-----------------------------------------
```HTTP
POST /home/submit HTTP/1.1
Host: healthscreening.schools.nyc
Cookies: .AspNetCore.Cookies=chunks-2; .AspNetCore.CookiesC1=<MASSIVE BLOB>; .AspNetCore.CookiesC2=<SMALLER BLOB>; AspNetCore.Antiforgery.<BLOB>=<BLOB>
POST-DATA : Type=S&FirstName=<FIRST NAME>&LastName=<LAST NAME>&Email=<FIRST NAME, FIRST LETTER OF LAST NAME>%40nycstudents.net&Location=13K430&CaseId=<RANDOM BIG NUMBER>&EmployeeNumber=<OSIS>&Phone=&Answer1=0&Answer2=0&Answer3=0&__RequestVerificationToken=CfDJ8OrQG11xGY1PobX2vUqMR3KtM7Jjr_Zn3S43p8JsSHVr0D6-_bpO6NonQUYYtHzY_xkZ-gqcgrr4e8rUanVOkmT0CAmPNrH2bkpofqhJYD97t6pVhRVUAryU86Bo91nXytNysMEejzUEgFTqijfRefb_1cf6hY3ikoK86gyoX43BGR7jiEh6OZVxPnYNEiPH5A
```


```HTTP
POST /home/submit HTTP/1.1
Host: healthscreening.schools.nyc
Cookies: .AspNetCore.Cookies=chunks-2; .AspNetCore.CookiesC1=<MASSIVE BLOB>; .AspNetCore.CookiesC2=<SMALLER BLOB>
POST-DATA : Type=S&FirstName=<FIRST NAME>&LastName=<LAST NAME>&Email=<FIRST NAME, FIRST LETTER OF LAST NAME>%40nycstudents.net&Location=13K430&CaseId=<RANDOM BIG NUMBER>&EmployeeNumber=<OSIS>&Phone=&Answer1=0&Answer2=0&Answer3=0&__RequestVerificationToken=CfDJ8OrQG11xGY1PobX2vUqMR3KtM7Jjr_Zn3S43p8JsSHVr0D6-_bpO6NonQUYYtHzY_xkZ-gqcgrr4e8rUanVOkmT0CAmPNrH2bkpofqhJYD97t6pVhRVUAryU86Bo91nXytNysMEejzUEgFTqijfRefb_1cf6hY3ikoK86gyoX43BGR7jiEh6OZVxPnYNEiPH5A
```

```HTTP
RESPONCE /home/submit HTTP/1.1
Host: healthscreening.schools.nyc 
HTTP/1.1 200 OK
JSON DATA: {"success":true,"model":{"CASE_ID":<ID>,"FIRST_NAME":"<FIRST_NAME>","LAST_NAME":"<LAST_NAME>","EMAIL":"<EMAIL>","LOCATION":"13K430","TYPE":"S","CREATE_DATE":"<CREATE DATE","CREATE_USER":"<USERNAME","ANSWER_1":false,"ANSWER_2":false,"ANSWER_3":false,"ANSWER_4":false,"FLOOR":null,"STATUS":false,"EMPLOYEE_NUMBER":"<OSIS>","OTHER":false,"LocationObj":null,"LocationNonDOE":null,"Employee":null}}
```

## Displaying Success Message 
```HTTP
GET /home/success?Type=S&FirstName=<FIRST NAME>&LastName=<LAST NAME>&Email=<FIRST NAME, FIRST LETTER OF LAST NAME>%40nycstudents.net&Location=13K430&CaseId=<RANDOM BIG NUMBER>&EmployeeNumber=<OSIS>&Phone=&Answer1=0&Answer2=0&Answer3=0&__RequestVerificationToken=CfDJ8OrQG11xGY1PobX2vUqMR3KtM7Jjr_Zn3S43p8JsSHVr0D6-_bpO6NonQUYYtHzY_xkZ-gqcgrr4e8rUanVOkmT0CAmPNrH2bkpofqhJYD97t6pVhRVUAryU86Bo91nXytNysMEejzUEgFTqijfRefb_1cf6hY3ikoK86gyoX43BGR7jiEh6OZVxPnYNEiPH5A
Host: healthscreening.schools.nyc
Cookie: .AspNetCore.Cookies=chunks-2; .AspNetCore.CookiesC1=<MASSIVE BLOB>; .AspNetCore.CookiesC2=<SMALLER BLOB>; .AspNetCore.Antiforgery.<BLOB>=<BLOB>
```
```HTTP
RESPONCE /home/success?Type=S&FirstName=<FIRST NAME>&LastName=<LAST NAME>&Email=<FIRST NAME, FIRST LETTER OF LAST NAME>%40nycstudents.net&Location=13K430&CaseId=<RANDOM BIG NUMBER>&EmployeeNumber=<OSIS>&Phone=&Answer1=0&Answer2=0&Answer3=0&__RequestVerificationToken=CfDJ8OrQG11xGY1PobX2vUqMR3KtM7Jjr_Zn3S43p8JsSHVr0D6-_bpO6NonQUYYtHzY_xkZ-gqcgrr4e8rUanVOkmT0CAmPNrH2bkpofqhJYD97t6pVhRVUAryU86Bo91nXytNysMEejzUEgFTqijfRefb_1cf6hY3ikoK86gyoX43BGR7jiEh6OZVxPnYNEiPH5A
Host: healthscreening.schools.nyc
```
*Note:Sucess message without imported libraries so its a bit ugly*
