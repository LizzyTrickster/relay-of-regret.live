#!/usr/bin/env python3
# Copyright Lizzy Trickster (Lizzy Green)
import os
import sys

import requests
from datetime import datetime, timedelta

r = requests.Session()
burl = "https://v5api.tiltify.com/api/public"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
currency_map = dict(USD="US$", EUR="€", GBP="£", AUD="AU$", CAD="CA$")


ww = r.post(f"https://v5api.tiltify.com/oauth/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials&scope=public")
if ww.status_code == 200:
    data = ww.json()
    r.headers['Authorization'] = data['access_token']
    token_expires_at = datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%SZ")+timedelta(seconds=data['expires_in'])
else:
    sys.exit(1)

RR = r.get(f"{burl}/teams/e32acae9-cf04-459a-8577-be8df38efa37")
# RR.json()  # Team
all_total_amount_raised = RR.json()['data']['total_amount_raised']

charity_data = dict()

for entry in r.get(f"{burl}/teams/e32acae9-cf04-459a-8577-be8df38efa37/team_campaigns?limit=50").json()['data']:
  charity_data[ entry['id'] ] =  entry['amount_raised']


res = r.post("http://127.0.0.1:5000/update", json=dict(charity_data=charity_data, total=all_total_amount_raised))
