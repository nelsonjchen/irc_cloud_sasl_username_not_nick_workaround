import asyncio
import json
import os
import sys

import requests
import websockets

IRCCLOUD_EMAIL = os.environ['IRCCLOUD_EMAIL']
IRCCLOUD_PASSWORD = os.environ['IRCCLOUD_PASSWORD']
# Fancy Server Name in IRCCloud GUI, eg. Rizon, SynIRC, freenode, Secret Server
IRC_SERVER_IRCCLOUD_NETWORK_NAME = os.environ['IRC_SERVER_IRCCLOUD_NETWORK_NAME']
# user(12333)
IRC_SERVER_IRCCLOUD_SASL_NAME = os.environ['IRC_SERVER_IRCCLOUD_SASL_NAME']
# xXxDongSmasherVegeta420xXx
IRC_SERVER_IRCCLOUD_NICK_NAME = os.environ['IRC_SERVER_IRCCLOUD_NICK_NAME']

# curl -X POST 'https://www.irccloud.com/chat/auth-formtoken' --header 'content-length: 0'

auth_token_request_json = requests.post('https://www.irccloud.com/chat/auth-formtoken').json()
if not auth_token_request_json['success']:
    raise Exception('Auth Token Request not successful')
token = auth_token_request_json['token']

# curl -d email=XXX -d password=XXX -d token=1397241172970.9a87f9s7fad9f7s9f8a7fa9sd77 --header 'content-type: application/x-www-form-urlencoded' --header 'x-auth-formtoken: 1397241172970.9a87f9s7fad9f7s9f8a7fa9sd77' 'https://www.irccloud.com/chat/login'

login_response = requests.post('https://www.irccloud.com/chat/login', headers={
    'content-type': 'application/x-www-form-urlencoded',
    'x-auth-formtoken': token,
}, data={
    'email': IRCCLOUD_EMAIL,
    'password': IRCCLOUD_PASSWORD,
    'token': token
}).json()

session = login_response['session']


async def consumer(message_json: str, websocket: websockets.client.WebSocketClientProtocol, state) -> dict:
    message = json.loads(message_json)
    print(f'< {message}')
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
                await consumer(json.dumps(message_json), websocket, state)
        if message['type'] == 'makeserver':
            if message['name'] != IRC_SERVER_IRCCLOUD_NETWORK_NAME:
                return state
            print('--- CONSIDERING NETWORK ---')
            # Store CID for processing later
            state['cid'] = message['cid']
            edit_server_values = {
                '_method': 'edit-server',
                'cid': message['cid'],
                'hostname': message['hostname'],
                'port': message['port'],
                'ssl': message['ssl'],
                'netname': message['name'],
                'nickname': message['nick'],
                'realname': message['realname'],
                'server_pass': message['server_pass'],
                'nspass': message['nickserv_pass'],
                'joincommands': message['join_commands'],
            }
            state['edit_server_values'] = edit_server_values.copy()

            if message['status'] == 'connected' and message['nick'] != IRC_SERVER_IRCCLOUD_NICK_NAME:
                print('--- ALREADY CONNECTED BUT BAD NICK ---')
                edit_server_values['nickname'] = IRC_SERVER_IRCCLOUD_NICK_NAME
                await websocket.send(json.dumps(edit_server_values))

            if message['status'] != 'connected' and message['nick'] != IRC_SERVER_IRCCLOUD_SASL_NAME:
                # Set the name to be the correct nickname
                edit_server_values['nickname'] = IRC_SERVER_IRCCLOUD_SASL_NAME
                await websocket.send(json.dumps(edit_server_values))

                pass

            if message['status'] == 'disconnected':
                await websocket.send(json.dumps({
                    '_method': 'reconnect',
                    'cid': message['cid']
                }))

            if message['status'] == 'connected' and message['nick'] == IRC_SERVER_IRCCLOUD_NICK_NAME:
                print('--- ALL IS WELL ---')
                sys.exit(0)

        if message['type'] == 'status_changed':
            if message['cid'] == state['cid']:
                if message['new_status'] == 'connected':
                    if message['nick'] != IRC_SERVER_IRCCLOUD_NICK_NAME:
                        state['edit_server_values']['nickname'] = IRC_SERVER_IRCCLOUD_NICK_NAME
                        await websocket.send(json.dumps(state['edit_server_values']))
                    if message['nick'] == IRC_SERVER_IRCCLOUD_NICK_NAME:
                        print('--- ALL IS WELL ---')
                        sys.exit(0)
    return state


async def connect_and_check():
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
        state = {}
        async for message_json in websocket:
            state = await consumer(message_json, websocket, state)


async def check_multiple_times():
    for _i in range(5):
        try:
            await asyncio.wait_for(connect_and_check(), timeout=10)
        except asyncio.TimeoutError:
            print(f'#### Check {_i + 1}! ####')


async def main():
    # Wait for at most 100 seconds
    try:
        await asyncio.wait_for(check_multiple_times(), timeout=30)
    except asyncio.TimeoutError:
        print('Finished!')


asyncio.get_event_loop().run_until_complete(main())
