# Auto Health Screen
Automatic System to login to the DOE portal and then fill out the daily health screening form.

## How it works 
Check out the how-it-works page to see an in-depth explanation

tl;dr : Hits the login page from the portal to get cookies, logins with cookies to get OAuth keys to the kingdom, redeems those keys at an endpoint to get login cookies, uses login cookies to submit the form as the user 


## Installation 
This project currently uses python requests to send the requests and uses BS4 from Beautiful Soup to scrape out the keys to the kingdom. The requests library had a couple of other dependencies such as idna and cerfifi
Create a .env file at the directory root and add your information in

```
FirstName = "foobar"
LastName = "baz"
OSIS = "000000000"
username = "foobarbaz0"
password = "Password123"
``````


## Todo
* Add a function to screenshot the success message so users can SMS the image to themselves 
* Clean up the code with functions and more comments 

#### Don't blame me if the DOE comes knocking at your door 

