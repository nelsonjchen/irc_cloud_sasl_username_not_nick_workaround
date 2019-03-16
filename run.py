import os
import requests

IRCCLOUD_EMAIL = os.environ['IRCCLOUD_EMAIL']
IRCCLOUD_PASSWORD = os.environ['IRCCLOUD_PASSWORD']

# curl -X POST "https://www.irccloud.com/chat/auth-formtoken" --header "content-length: 0"

auth_token_request_json = requests.post("https://www.irccloud.com/chat/auth-formtoken").json()
if not auth_token_request_json['success']:
    raise Exception("Auth Token Request not successful")
token = auth_token_request_json['token']

# curl -d email=XXX -d password=XXX -d token=1397241172970.9a87f9s7fad9f7s9f8a7fa9sd77 --header "content-type: application/x-www-form-urlencoded" --header "x-auth-formtoken: 1397241172970.9a87f9s7fad9f7s9f8a7fa9sd77" "https://www.irccloud.com/chat/login"

login_response = requests.post('https://www.irccloud.com/chat/login', headers={
    'content-type': 'application/x-www-form-urlencoded',
    'x-auth-formtoken': token,
}, data={
    'email': IRCCLOUD_EMAIL,
    'password': IRCCLOUD_PASSWORD,
    'token': token
}).json()
pass
