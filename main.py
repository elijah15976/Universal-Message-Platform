import configparser
from flask import Flask, request
import requests

import os

keys = configparser.ConfigParser()
keys.read("keys.ini")

app = Flask(__name__)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
URL_MESSENGER = "http://localhost:3000/send"
URL_DISCORD = "http://localhost:3001/send"

@app.route("/")
def index():
  file = open(os.path.join(THIS_FOLDER, 'Web UI\\index.html'), "r").read()
  return file

@app.route("/script.js")
def scriptjs():
  file = open(os.path.join(THIS_FOLDER, 'Web UI\\script.js'), "r").read()
  return file

@app.route("/style.css")
def stylecss():
  file = open(os.path.join(THIS_FOLDER, 'Web UI\\style.css'), "r").read()
  return file

@app.route("/send", methods=["POST"])
def send():
  print(request.json)
  msg = request.json["message"]
  sec = request.json["secret"]

  secret_keys = keys["Client"]["secret"].split(',')

  if not (sec in secret_keys):
    return "not authorized"
  
  response_messenger = requests.post(URL_MESSENGER, json={"message": msg})
  response_discord = requests.post(URL_DISCORD, json={"message": msg})

  if(response_messenger.text == "Finished" and response_discord.text == "Finished"):
    return "success"
  else:
    return "error"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=65501)