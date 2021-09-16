import requests, re 
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def submit():
    base = 'https://healthscreening.schools.nyc/'
    PROXIES = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

    CREDS = {"vusername":os.environ.get('username') ,"password":os.environ['password'],"login-form-type":"pwd","username":os.environ['username'] }


    get_home_login = requests.get(base+ '/home/login', allow_redirects=False)
    AspNetCore = {}
    for i in get_home_login.cookies:
        AspNetCore[i.name] = i.value

    redirected_w_oauth_headers = {
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

    redirected_w_oauth = requests.get(get_home_login.headers['Location'], headers = redirected_w_oauth_headers , cookies=AspNetCore, allow_redirects=False)

    Js_Bigip = {}
    for i in redirected_w_oauth.cookies:
        Js_Bigip[i.name] = i.value

    ipd_mga_auth_headers = {
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

    ipd_mga_auth = requests.get( redirected_w_oauth.headers['Location'] ,headers=ipd_mga_auth_headers,cookies=Js_Bigip, allow_redirects=False )
    pd_s_session = { "PD-S-SESSION-ID" : ipd_mga_auth.cookies['PD-S-SESSION-ID'] } 


    post_pkms = requests.post( "https://idp.nycenet.edu/pkmslogin.form?token=Unknown" , data=CREDS , allow_redirects=False, cookies=Merge(pd_s_session, Js_Bigip))     # This is 302 permendently moved
    pd_s_session['PD-S-SESSION-ID'] = post_pkms.cookies['PD-S-SESSION-ID']

    get_oath_keys_headers = {
            "Cache-Control":"max-age=0",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site":"same-origin",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-User":"?1",
            "Sec-Fetch-Dest":"document",
            "Sec-Ch-Ua":"\"Chromium\";v=\"93\", \" Not;A Brand\";v=\"99\"",
            "Sec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"\"Linux\"",
            "Referer":"https://idp.nycenet.edu/mga/sps/auth",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.9"
            }

    get_oath_keys = requests.get( post_pkms.headers['Location'] ,headers=get_oath_keys_headers, cookies=Merge( Js_Bigip, pd_s_session ) , verify=False )

    soup = BeautifulSoup(get_oath_keys.text, features="html.parser")
    oauth_creds = {}
    for link in soup.find_all('input'):
        oauth_creds[link.get('name')] = link.get("value")

    validate_oath_headers = {
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
    validate_oath = requests.post("https://healthscreening.schools.nyc/authorization-code/callback", cookies=AspNetCore, headers=validate_oath_headers, data=oauth_creds, verify=False, allow_redirects=False)

    login_cookies= {}

    for i in validate_oath.cookies:
        login_cookies[i.name] = i.value

    login_with_keys_headers = {
            "Cache-Control":"max-age=0",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site":"cross-site",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-Dest":"document",
            "Sec-Ch-Ua":"\"Chromium\";v=\"93\", \" Not;A Brand\";v=\"99\"",
            "Sec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"\"Linux\"",
            "Referer":"https://idp.nycenet.edu/",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.9"
    }


    login_with_keys = requests.get(base + validate_oath.headers['Location'], headers=login_with_keys_headers, cookies=login_cookies , verify=False )

    anti_forgery = {}
    for i in login_with_keys.cookies:
        anti_forgery[i.name] = i.value


    submit_form_headers = {
            "Sec-Ch-Ua":"\"Chromium\";v=\"93\", \" Not;A Brand\";v=\"99\"",
            "Sec-Ch-Ua-Mobile":"?0",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Accept":"*/*",
            "X-Requested-With":"XMLHttpRequest",
            "Request-Context":"appId=cid-v1:d30722be-c0fe-4052-9f21-656e879e76b0",
            "Request-Id":"|rE+hX.ZMMiE",
            "Sec-Ch-Ua-Platform":"\"Linux\"",
            "Origin":"https://healthscreening.schools.nyc",
            "Sec-Fetch-Site":"same-origin",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Dest":"empty",
            "Referer":"https://healthscreening.schools.nyc/",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.9"
            }
    submit_form = requests.post(base + "/home/submit",headers=submit_form_headers, cookies=Merge(anti_forgery, login_cookies), data="Type=S&FirstName=EDDIE&LastName=XIAO&Email=eddiex4%40nycstudents.net&Location=13K430&CaseId=1384268&EmployeeNumber=234154722&Phone=&Answer1=0&Answer2=0&Answer3=0" )
    get_sucess = requests.get(base + "/home/success?Type=S&FirstName=EDDIE&LastName=XIAO&Email=eddiex4%40nycstudents.net&Location=13K430&CaseId=0&EmployeeNumber=234154722&Phone=&Answer1=0&Answer2=0&Answer3=0", cookies= Merge(anti_forgery, login_cookies))

    return submit_form.text
print(submit())

