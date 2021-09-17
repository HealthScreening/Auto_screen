import requests, re ,json
import os
from bs4 import BeautifulSoup

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def lambda_handler(event, context):
    base = 'https://healthscreening.schools.nyc/'

    CREDS = {"vusername":os.environ.get('username') ,"password":os.environ['password'],"login-form-type":"pwd","username":os.environ['username'] }

    get_home_login = requests.get(base+ '/home/login', allow_redirects=False)
    AspNetCore = {}
    for i in get_home_login.cookies:
        AspNetCore[i.name] = i.value

    get_header1 = {
            "Host":"idp.nycenet.edu",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site":"cross-site",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-User":"?1",
            "Sec-Fetch-Dest":"document",
            "Sec-Ch-Ua":"\"Chromium\";v=\"93\", \" Not;A Brand\";v=\"99\"",
            "Sec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"\"Linux\"",
            "Referer":"https://healthscreening.schools.nyc/",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.9"
    }

    redirected_w_oauth = requests.get(get_home_login.headers['Location'], headers = get_header1 , cookies=AspNetCore, allow_redirects=False)

    Js_Bigip = {}
    for i in redirected_w_oauth.cookies:
        Js_Bigip[i.name] = i.value


    ipd_mga_auth = requests.get( redirected_w_oauth.headers['Location'] ,headers=get_header1,cookies=Js_Bigip, allow_redirects=False )
    pd_s_session = { "PD-S-SESSION-ID" : ipd_mga_auth.cookies['PD-S-SESSION-ID'] } 


    post_pkms = requests.post( "https://idp.nycenet.edu/pkmslogin.form?token=Unknown" , data=CREDS , allow_redirects=False, cookies=Merge(pd_s_session, Js_Bigip))     # This is 302 permendently moved
    pd_s_session['PD-S-SESSION-ID'] = post_pkms.cookies['PD-S-SESSION-ID']

    get_oath_keys = requests.get( post_pkms.headers['Location'] ,headers=get_header1, cookies=Merge( Js_Bigip, pd_s_session ) , verify=False )

    soup = BeautifulSoup(get_oath_keys.text, features="html.parser")
    oauth_creds = {}
    for link in soup.find_all('input'):
        oauth_creds[link.get('name')] = link.get("value")

    post_header1 = {
            "Cache-Control":"max-age=0",
            "Sec-Ch-Ua":"\"Chromium\";v=\"93\", \" Not;A Brand\";v=\"99\"",
            "Sec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"\"Linux\"",
            "Upgrade-Insecure-Requests":"1",
            "Origin":"https://idp.nycenet.edu",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site":"cross-site",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-Dest":"document",
            "Referer":"https://idp.nycenet.edu/",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.9"
    }
    validate_oath = requests.post("https://healthscreening.schools.nyc/authorization-code/callback", cookies=AspNetCore, headers=post_header1, data=oauth_creds, verify=False, allow_redirects=False)

    login_cookies= {}

    for i in validate_oath.cookies:
        login_cookies[i.name] = i.value


    login_with_keys = requests.get(base + validate_oath.headers['Location'], headers=post_header1, cookies=login_cookies , verify=False )

    anti_forgery = {}
    for i in login_with_keys.cookies:
        anti_forgery[i.name] = i.value



    submit_form = requests.post(base + "/home/submit",headers=post_header1, cookies=Merge(anti_forgery, login_cookies), data="Type=S&FirstName=EDDIE&LastName=XIAO&Email=eddiex4%40nycstudents.net&Location=13K430&CaseId=1384268&EmployeeNumber=234154722&Phone=&Answer1=0&Answer2=0&Answer3=0")
    return {
        'statusCode': 200,
        'body': json.dumps(submit_form.text)
    }

