# Auto Health Screen
Automatic System to login to the DOE portal and then fill out the daily health screening form.
Option to run the code locally or be hip and cool and use AWS Lambda to fully automate this. Using aws you can fill it out once and never do it again

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
0. Create an aws account, the free tier will work for this
1. Download the upload.zip file only
3. On the aws page create a new function at `https://console.aws.amazon.com/lambda/home?region=us-east-1#/create/function`
4. Select the normal code package, select python3.9 from the drop-down menu, and then create the function
![image](https://user-images.githubusercontent.com/77011982/133705679-fb50d70e-57c5-4cd3-8fda-0738fdccd376.png)
5. Select **Upload From** > **.zip** and select the file named upload.zip
![image](https://user-images.githubusercontent.com/77011982/133706599-da1d1429-be38-48d8-8415-1ffdf0770751.png)

7. Select **Configuration** > **Environment variables** > **Edit**
![image](https://user-images.githubusercontent.com/77011982/133706391-8d747e4a-2c8c-4de6-aa58-e5333b8e9c2e.png)

8. Add in FirstName, LastName, OSIS, password and username (Casing matters here) 
![image](https://user-images.githubusercontent.com/77011982/133706485-5f0be623-8621-47e3-a70d-f4f92f3002ec.png)

9. On the home dashboard select **Add Trigger** and search for **CloudWatch Events** 
![image](https://user-images.githubusercontent.com/77011982/133706703-6a613edb-ac00-4c16-892a-cd13b5b11e42.png)

10. Create a new rule, name it anything, Schedule Expression for Rule type, and Set Schedule Expression to `cron(0 10 * * ? *)`. The 10 in this equation means 10AM in UTC time which is 6AM in GMT-4. Change this number to suit your needs 

![image](https://user-images.githubusercontent.com/77011982/133706858-c25acd84-37cf-4bc7-8722-1e9a013ed091.png)

11. Fun and Profit 

## How it works 
Check out the how-it-works page to see an in-depth explanation

tl;dr : Hits the login page from the portal to get cookies, logins with cookies to get OAuth keys to the kingdom, redeems those keys at an endpoint to get login cookies, uses login cookies to submit the form as the user 

## Todo
* Add a function to screenshot the success message so users can SMS the image to themselves 
* Clean up the code with functions and more comments 

#### Don't blame me if anyone comes knocking at your door 

