# How this Page Works:

## Getting Cookies for DOE login page
-------------------------------------------------------
```HTTP 
GET /home/login
Host: healthscreening.schools.nyc
Cookie: ai_user=<TIME> _ga=<NO CLUE> ; _gid=<NO CLUE>
```
```HTTP 
RESPONSE /home/login
Host: healthscreening.schools.nyc
RESPONSE: HTTP/1.1 302 Found 
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
RESPONSE /mga/sps/oauth/oauth20/authorize?client_id=<REDACTED>&redirect_uri=https%3A%2F%2Fhealthscreening.schools.nyc%2Fauthorization-code%2Fcallback&response_type=code%20id_token&scope=openid%20profile&response_mode=form_post&nonce=<REDACTED>&state=<REDACTED>&x-client-SKU=ID_NETSTANDARD2_0&x-client-ver=5.5.0.0
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
# This is the DOE login page, work done before this was to get the correct cookies
```

## After Entering Credentials
-------------------------------------------------------
```HTTP 
POST /pkmslogin.form?token=Unknown HTTP/1.1
Host: idp.nycenet.edu
Cookie: AMWEBJCT!%2Fmga!JSESSIONID=<RANDOM B64 BLOB > ; BIGipServerPR_IDP_NYCENET_EDU_POOL=000000000.00000.0000; PD-S-SESSION-ID=<REDACTED>
POST-DATA : vusername=<USERNAME>&password=<PASSWORD>&login-form-type=pwd&username=<USERNAME>
```
```HTTP 
RESPONSE /pkmslogin.form?token=Unknown HTTP/1.1
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
3 KEYS TO THE KINGDOM- Code, state, id_token
```
## Redeeming Cookies at `/authorization-code/callback`
-------------------------------------------------------

```HTTP 
POST /authorization-code/callback HTTP/1.1
Host: healthscreening.schools.nyc
Cookie: .AspNetCore.OpenIdConnect.Nonce.<RANDOM B64 BLOB>=N; .AspNetCore.Correlation.OpenIdConnect.<RANDOM B64 BLOB>=N;
POST-DATA : code=<code>&id_token=<id_token>&state=<state>   # All this is from teh KEYS TO THE KINGDOM
```

```HTTP 
RESPONSE /authorization-code/callback HTTP/1.1
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
```HTTP
GET /home/login HTTP/1.1
Host: healthscreening.schools.nyc
Cookies: .AspNetCore.Cookies=chunks-2; .AspNetCore.CookiesC1=<MASSIVE BLOB>; .AspNetCore.CookiesC2=<SMALLER BLOB>
```
```HTTP
RESPONSE /home/login HTTP/1.1
Host: healthscreening.schools.nyc
HTTP/1.1 302 Found
Location: /
```
