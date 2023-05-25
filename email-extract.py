import requests
import json
import pandas as pd

url_auth = 'https://api.dinamize.com/auth'
auth_info = {
    "user": "######@##########",
    "password": "#######################",
    "client_code": "######"
  }
header_auth = {'Content-Type': 'application/json'}
post_auth = requests.post(url_auth, headers = header_auth, json = auth_info)
response_auth = json.loads(post_auth.text)
auth_token = response_auth['body']['auth-token']

url = 'https://api.dinamize.com/emkt/action/search'
header = {
    'auth-token': auth_token,
    'content-type': 'application/json'
}
parameters = {
    "page_number": "1",
    "page_size": "100",
    "show_children": True
}
post = requests.post(url, headers = header, json = parameters)
response = json.loads(post.text)

code = []
created_at = []
started_at = []
ended_at = []
subject = []
title = []

num_actions = len(response['body']['items'])

for i in range(num_actions):
  code.append(response['body']['items'][i]['code'])
  created_at.append(response['body']['items'][i]['date_create'])
  started_at.append(response['body']['items'][i]['date_start'])
  ended_at.append(response['body']['items'][i]['date_end'])
  subject.append(response['body']['items'][i]['subject'])
  title.append(response['body']['items'][i]['title'])

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

for i in range(num_actions):
  parameters = {
  'action_code':code[i],
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
    'id': code,
    'title': title,
    'subject': subject,
    'contacts': contacts,
    'sent': sent,
    'delivered': delivered,
    'view': view,
    'spam': spam,
    'error': error,
    'clicks': click,
    'started_at': started_at,
    'ended_at': ended_at,
    'created_at': created_at
}

df_emails = pd.DataFrame(dicti)
df_emails