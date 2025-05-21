import configparser
from flask import Flask, request
import requests

import json
import os

keys = configparser.ConfigParser()
keys.read("keys.ini")

app = Flask(__name__)

VERIFY_TOKEN = keys["Messenger"]["Request Token"]
FB_API_URL = 'https://graph.facebook.com/v21.0/me/messages'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

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
      elif "SUBSCRIBE" == message_text:
        #Adds user to messenger_subscription.json
        subscription_tracker = open(os.path.join(THIS_FOLDER, 'messenger_subscription.json'), "r")
        tracker_json = json.loads(subscription_tracker.read())

        for item in tracker_json:
          if sender_id == item:
            send_text_message(sender_id, "You are already subscribed")
            return "User Already Subscribed"
        tracker_json.append(sender_id)

        subscription_tracker_write = open(os.path.join(THIS_FOLDER, 'messenger_subscription.json'), "w")
        subscription_tracker_write.write(json.dumps(tracker_json))
        subscription_tracker.close()
        subscription_tracker_write.close()

        send_text_message(sender_id, "You are now subscribed to receive text notifications")
      elif "UNSUBSCRIBE" == message_text:
        #Removes user from messenger_subscription.json
        subscription_tracker = open(os.path.join(THIS_FOLDER, 'messenger_subscription.json'), "r")
        tracker_json = json.loads(subscription_tracker.read())

        for item in tracker_json:
          if sender_id == item:
            tracker_json.remove(sender_id)

            subscription_tracker_write = open(os.path.join(THIS_FOLDER, 'messenger_subscription.json'), "w")
            subscription_tracker_write.write(json.dumps(tracker_json))
            subscription_tracker.close()
            subscription_tracker_write.close()

            send_text_message(sender_id, "You are no longer subscribed to receive text notifications")
            return "User Removed from Subscription"
        
        subscription_tracker.close()

        send_text_message(sender_id, "You are already not subscribed")
    return "Done"

@app.route("/send", methods=["POST"])
def send():
  message = request.json["message"]

  subscription_tracker = open(os.path.join(THIS_FOLDER, 'messenger_subscription.json'), "r")
  tracker_json = json.loads(subscription_tracker.read())

  for item in tracker_json:
    send_text_message(item, message)

  return "Finished"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3000)
