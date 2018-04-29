import requests
import twilio.rest
import json
import sys
import os

HOME_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
response = requests.get("http://ip.42.pl/raw")

if response.status_code != 200:
	print(f"Could not retrieve IP. The status code was {response.status_code}")
	sys.exit()

current_ip = response.text
with open(os.path.join(HOME_DIRECTORY, "ip_address.txt")) as f:
	previous_ip = f.read()
	
if current_ip == previous_ip:
	print("Public facing IP has not changed.")
	sys.exit()
print("Public facing IP has changed!")
	
with open(os.path.join(HOME_DIRECTORY, "ip_address.txt"), 'w') as f:
	f.write(current_ip)
	
with open(os.path.join(HOME_DIRECTORY, "message.json"), encoding='utf-8') as f:
	message = json.load(f)

credentials = json.load(open(os.path.join(HOME_DIRECTORY, "auth.json")))
client = twilio.rest.Client(credentials["account_sid"], credentials["auth_token"])
message = client.messages.create(message["to"], body=message["message"].format(current_ip), from_=message["from"])

print(message.sid)