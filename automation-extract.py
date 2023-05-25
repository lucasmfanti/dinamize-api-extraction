import requests
import json
import pandas as pd

url_auth = 'https://api.dinamize.com/auth'
auth_info = {
    "user": "#####@##########",
    "password": "#######################",
    "client_code": "######"
  }
header_auth = {'Content-Type': 'application/json'}
post_auth = requests.post(url_auth, headers = header_auth, json = auth_info)
response_auth = json.loads(post_auth.text)
auth_token = response_auth['body']['auth-token']

url = 'https://api.dinamize.com/emkt/action/automation_list'
header = {
    'auth-token': auth_token,
    'content-type': 'application/json'
}
parameters = {
  'contact-list_code':'1'
}
post = requests.post(url, headers = header, json = parameters)
response = json.loads(post.text)

automation_title = []
automation_inserted_at = []
action_code = []
action_title = []
action_started_at = []

num_automations = len(response['body']['items'])

for i in range(num_automations):
  num_action = len(response['body']['items'][0]['action_list'])
  for j in range(num_action):
    automation_title.append(response['body']['items'][i]['title'])
    automation_inserted_at.append(response['body']['items'][i]['insert_date'])
    action_code.append(response['body']['items'][i]['action_list'][j]['action_code'])
    action_title.append(response['body']['items'][i]['action_list'][j]['action_title'])
    action_started_at.append(response['body']['items'][i]['action_list'][j]['action_start_date'])

click = []
contacts = []
delivered = []
error = []
sent = []
spam = []
view = []

url = 'https://api.dinamize.com/emkt/action/report'
header = {
    'auth-token': auth_token,
    'content-type': 'application/json'
}

num_actions = len(action_code)

for i in range(num_actions):
  parameters = {
  'action_code':action_code[i],
  'type':'summary'
  }
  post = requests.post(url, headers = header, json = parameters)
  response = json.loads(post.text)
  click.append(response['body']['click'])
  contacts.append(response['body']['contacts'])
  delivered.append(response['body']['delivered'])
  error.append(response['body']['error'])
  sent.append(response['body']['sent'])
  spam.append(response['body']['spam'])
  view.append(response['body']['view'])

dicti = {
    'id': action_code,
    'title': action_title,
    'automation_title': automation_title,
    'automation_inserted_at': automation_inserted_at,
    'contacts': contacts,
    'sent': sent,
    'delivered': delivered,
    'view': view,
    'spam': spam,
    'error': error,
    'clicks': click,
    'started_at': action_started_at
}

df_automations = pd.DataFrame(dicti)
df_automations