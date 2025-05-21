import configparser
from flask import Flask, request

keys = configparser.ConfigParser()
keys.read("keys.ini")

app = Flask(__name__)

VERIFY_TOKEN = keys["Messenger"]["Request Token"]

def verify_token(req):
  if req.args.get("hub.verify_token") == VERIFY_TOKEN:
    print("Token Verified")
    return req.args.get("hub.challenge")
  else:
    print("Token was not Verified")
    return "Incorrect"

@app.route("/webhook", methods=["GET", "POST"])
def listen():
  if request.method == "GET":
    return verify_token(request)
  else:
    print("Not Implemented Yet")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3000)