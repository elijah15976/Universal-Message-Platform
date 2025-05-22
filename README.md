# **Universal Message Platform (UMP)**
Technically, more like universal announcement platform. There's no back and forth messaging happening.  
Anyways, here's how to use the application :)

## Table of Contents:
- [Setting Up](#setting-up)  
  - [Create Necessary Files](#1-create-necessary-files)  
  - [Set Up Ngrok](#2-set-up-ngrok)  
  - [Set Up Messenger Bot](#3-set-up-messenger-bot)  
  - [Set Up Discord Bot](#4-set-up-discord-bot)  
- [Running the Platform](#running-the-platform)


## Setting Up

### 1. Create Necessary Files
1. Create `keys.ini`  
This will store your messenger and discord tokens, alongside client's secret.  
Copy and paste the following into `keys.ini`
```
[Client]
secret = 

[Messenger]
App Id = 
App Secret = 
Access Token = 
Request Token = 

[Discord]
Client Id = 
Client Secret = 
Token = 
```

2. Create `discord_subscription.json` and `messenger_subscription.json`  
This will store the users who are subscribed  
Copy and paste the following into `discord_subscription.json` and `messenger_subscription.json`
```
[]
```

### 2. Set Up Ngrok
1. Start ngrok by running `run_ngrok.bat`  
Follow all the instructions to set up ngrok if it isn't already set up

### 3. Set Up Messenger Bot
1. On Facebook, create a public page  
This page will be your bot's profile
2. Go to [Meta for Developers](https://developers.facebook.com/)
3. Create an app  
  \- Allow it to `Engage with customers on Messenger from Meta`  
  \- Don't connect a business portfolio
4. Once in dashboard:  
  \- Go to "Use cases", click "Customize", and go to "Messenger API Settings"  
  \- For `Configure Webhook`, the "Callback URL" will be the generated URL when ngrok is running. The "Verify Token" is the "Request Token" in `keys.ini`  
  \- Scroll down and make sure the "messages" webhook is `Subscribed`  
  \- For `Generate Access Tokens`, link it to the public page created in `Step 1`  
  \- Generate the Token, and paste it in "Access Token" in `keys.ini`

### 4. Set Up Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers)
2. Create a new application
3. Under `Bot`:  
  \- Click `Add Bot`  
  \- Personalize the bot. This is the bot's profile  
  \- For `Token`, click on `Reset Token`, and paste it in "Token" in `keys.ini`


## Running the Platform
1. Make sure ngrok is running  
If not, run `run_ngrok.bat`

2. Install the necessary dependencies by running `install_dependencies.bat`  
Python will install the necessary packages onto your computer

3. Run the application by clicking `run.bat`  
There should be 3 terminals (4 if including ngrok). 1st for Messenger, 2nd for Discord, and 3rd for Web UI