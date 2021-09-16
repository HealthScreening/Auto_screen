# Auto Health Screen
Automatic System to login to the DOE portal and then fill out the daily health screening form.

## How it works in a nutshell
The health screening page uses OAUTH to login and then redirect the user to the form. This process uses Authorization Code Grant. More information can be found here 
```
https://portswigger.net/web-security/oauth
```
During the first login theirs a PD-SESSION that is established and this is added to the cookies to remind the page to redirect users to the login page after inital login. 

The form itself uses javascript so the final request is POST to the /home/submit with all the information. This includes a `__RequestVerificationToke` but the server does not seem to validate the code so we can spoof this by deleteing that parameter completly. After submitting the form a second request is made to the `/home/sucess.html` with paramters very simular to the post request. 

For the login with the OATUH given cookies and the form posting a `AspNetCore.Antiforgery` is needed but this can be accssed from the pages with redirection


## Installation 
This project currently uses python requests to send the requests and uses BS4 from Beautiful Soup to scrapy out the keys to the kingdom. The requests library had a couple of other dependenncies such as idna and cerfifi


## Todo
Add a fuction to screenshot the sucess message so users can SMS the image to themselves 
Clean up the code with functions and more comments 

