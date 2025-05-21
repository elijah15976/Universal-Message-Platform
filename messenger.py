import configparser
from flask import Flask, request
import requests

keys = configparser.ConfigParser()
keys.read("keys.ini")

app = Flask(__name__)

VERIFY_TOKEN = keys["Messenger"]["Request Token"]
FB_API_URL = 'https://graph.facebook.com/v21.0/me/messages'

def verify_token(req):
  if req.args.get("hub.verify_token") == VERIFY_TOKEN:
    print("Token Verified")
    return req.args.get("hub.challenge")
  else:
    print("Token was not Verified")
    return "Incorrect"
  
def send_text_message(recipient_id, text):
  message_payload = {
    'message': {
      'text': text
    },
    'recipient': {
        'id': recipient_id
    }
  }
  auth = {
    'access_token': keys["Messenger"]["Access Token"]
  }

  requests.post(
    FB_API_URL,
    params=auth,
    json=message_payload
  )

@app.route("/webhook", methods=["GET", "POST"])
def listen():
  if request.method == "GET":
    return verify_token(request)
  elif request.method == "POST":
    payload = request.json
    events = payload["entry"][0]["messaging"]

    for event in events:
      sender_id = event["sender"]["id"]
      message_text = event["message"]["text"]

      if "TEST" == message_text:
        send_text_message(sender_id, "This bot is sucessfully connected")
    return "Done"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3000)
