# Auto Health Screen
Automatic System to login to the DOE portal and then fill out the daily health screening form.

## How it works 
Check out the how-it-works page to see a in depth explination

tl;dr : Hits the login page from the portal to get cookies, logins with cookies to get oauth keys to kingdom, redeems those keys at a endpoint to get login cookies, uses login cookies to submit form as user 


## Installation 
This project currently uses python requests to send the requests and uses BS4 from Beautiful Soup to scrapy out the keys to the kingdom. The requests library had a couple of other dependenncies such as idna and cerfifi


## Todo
* Add a fuction to screenshot the sucess message so users can SMS the image to themselves 
* Clean up the code with functions and more comments 

#### Don't blame me if the DOE comes knocking at your door 
