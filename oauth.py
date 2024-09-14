import requests
from requests.auth import HTTPBasicAuth as Auth

url = 'https://ticktick.com/oauth/authorize?scope=tasks:write%20tasks:read&client_id={client_id}&state=state&redirect_uri=https://www.example.com/&response_type=code'

client_id = input('What is your client ID?\n> ')
client_secret = input('What is your client secret?\n> ')
print()

while True:
  try:
    print('Please go to the following link, follow the prompt, and copy the redirect url below.')
    print()
    print(url.format(client_id=client_id))
    redirect_link = input('> ')

    query_parameters = redirect_link.split('?')[1].split('&')
    code = next(arg.split('=')[1] for arg in query_parameters if arg.split('=')[0] == 'code')
  except StopIteration:
    print('Try Again')
    continue

  break


token_req = requests.post(
  'https://ticktick.com/oauth/token',
  params={
    'code': code,
    'grant_type': 'authorization_code',
    'scope': 'tasks:read tasks:write',
    'redirect_uri': 'https://www.example.com/',
    'state': 'state',
  },
  auth=Auth(client_id, client_secret)
)

token = token_req.json()['access_token']

print(f'\nYour access token is "{token}"')
