# Auto Health Screen
Automatic System to login to the DOE portal and then fill out the daily health screening form.
TWo methods of installation as running this locally a waste of time. Using something like AWS lambda can be more efficant and convienent


## Installation and usage
### Running this locally:
1. Clone the repo `git clone  https://github.com/ex4722/Auto_screen.git`
2. Move into that directory `cd Auto_screen`
3. Install requirements `pip install -r requirements.txt`
4. Create a .env file with your credentials 
```
FirstName = "foobar"
LastName = "baz"
OSIS = "000000000"
username = "foobarbaz0"
password = "Password123"
``````
5. Run the script
6. ?????
7. Profit

### Using AWS
0. Create a aws account, the free tier will work for this
1. Clone the repo `git clone  https://github.com/ex4722/Auto_screen.git`
2. Move into that directory `cd Auto_screen`
3. 

## How it works 
Check out the how-it-works page to see an in-depth explanation

tl;dr : Hits the login page from the portal to get cookies, logins with cookies to get OAuth keys to the kingdom, redeems those keys at an endpoint to get login cookies, uses login cookies to submit the form as the user 

## Todo
* Add a function to screenshot the success message so users can SMS the image to themselves 
* Clean up the code with functions and more comments 

#### Don't blame me if anyone comes knocking at your door 

