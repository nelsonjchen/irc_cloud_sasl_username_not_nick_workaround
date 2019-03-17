import asyncio
import json
import os
import requests
import websockets

IRCCLOUD_EMAIL = os.environ['IRCCLOUD_EMAIL']
IRCCLOUD_PASSWORD = os.environ['IRCCLOUD_PASSWORD']
# Fancy Server Name in IRCCloud GUI, eg. Rizon, SynIRC, freenode, Secret Server
IRC_SERVER_IRCCLOUD_NAME = os.environ['IRC_SERVER_IRCCLOUD_NAME']
# user(12333)
IRC_SERVER_IRCCLOUD_SASL_NAME = os.environ['IRC_SERVER_IRCCLOUD_SASL_NAME']
# xXxDongSmasherVegeta420xXx
IRC_SERVER_IRCCLOUD_NICK_NAME = os.environ['IRC_SERVER_IRCCLOUD_NICK_NAME']

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

session = login_response['session']


async def consumer(message_json: str, websocket: websockets.client.WebSocketClientProtocol):
    message = json.loads(message_json)
    print(f"< {message}")
    if 'type' in message:
        if message['type'] == 'oob_include':
            backlog = requests.get(
                f"https://www.irccloud.com{message['url']}",
                headers={
                    'Cookie': f'session={session}',
                    'Origin': 'https://api.irccloud.com',
                }
            ).json()
            for message_json in backlog:
                await consumer(json.dumps(message_json), websocket)
        if message['type'] == 'makeserver':
            if message['name'] != IRC_SERVER_IRCCLOUD_NAME:
                return
            if not message['disconnected']:
                return
            # Begin Reconnect Process


async def hello():
    # noinspection PyUnusedLocal
    websocket: websockets.client.WebSocketClientProtocol
    async with websockets.connect(
        'wss://api.irccloud.com/',
        ssl=True,
        extra_headers={
            'Cookie': f'session={session}',
            'Origin': 'https://api.irccloud.com',
        }
    ) as websocket:
        # noinspection PyUnusedLocal
        message_json: str
        async for message_json in websocket:
            await consumer(message_json, websocket)


asyncio.get_event_loop().run_until_complete(hello())