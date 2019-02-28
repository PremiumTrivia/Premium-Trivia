import random
import requests
from discord.ext.commands import Bot
import discord
from discord.ext import commands
import random
import aiohttp
import csv
import json
import datetime

client = Bot(command_prefix='bb.')
client.remove_command('help')

TOKEN = "BPT_TOKEN"

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print("I'm ready")

@client.command(pass_context=True, no_pm=True)
async def bbphone(ctx, refercode=None, message=None):
    if refercode is None:
        return await client.say("**Wrong Input correct use : `bb.bbphone <refer_code> <number with +1>`**")
    if message is None:
        return await client.say("**Wrong Input correct use : `bb.bbphone <refer_code> <number with +1>`**")

    phonenumber = message
    print(phonenumber)
    url = "http://commander.brainbaazi.com/api/v4/trivia/otp"
    payload = "{\"mob\": \""+str(phonenumber)+"\"}"
 
    headers = {
        'Content-Type': "application/json; charset=utf-8,application/json",
        'client_key': "brainbaazi"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    if json.loads(response.text)["message"] == "Invalid mobile number!":
        return await client.say(json.loads(response.text)["message"])
    else:
        pass
    otptoken=response.headers["otp_token"]
    print(otptoken)
    await client.say("4 digit verification code sent to XXXXXXXXXX\nEnter your code: bb.code xxxx")

    global smscode
    smscode = None

    def code_check(msg1):
        return msg1.content.lower().startswith('bb.code')

    smg = await client.wait_for_message(author=ctx.message.author, check=code_check)
    smscode = smg.content[len('bb.code'):].strip()

    try:
        value = int(smscode)
    except ValueError:
        return await client.say("Incorrect OTP")
        

    url = "http://commander.brainbaazi.com/api/v4/trivia/login"
    
    payload = "{\r\n\t\"unm\": null,\r\n\t\"dtp\": \"A\",\r\n\t\"did\": \"d050990d99a24792\",\r\n\t\"cid\": \"+1\",\r\n\t\"uim\": null,\r\n\t\"aqs\": null,\r\n\t\"rid\": null,\r\n\t\"mob\": \""+str(phonenumber)+"\",\r\n\t\"msg\": \""+str(smscode)+"\",\r\n\t\"lang\": \"0\"\r\n}"
    headers = {
        'otp_token': "{}".format(otptoken),
        'Content-Type': "application/json,application/json; charset=utf-8",
        'client_key': "brainbaazi",
        'acquisition_source': "brainbaazi"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    if json.loads(response.text)["message"] == "Incorrect OTP, try Again":
        return await client.say(json.loads(response.text)["message"])
    else:
        pass
    authtoken = json.loads(response.text)["response"]["auth_token"]
    print(authtoken)

    url = "https://commander.brainbaazi.com/api/v3/trivia/addref"
    
    payload = "{\r\n\t\"rid\": \""+str(refercode)+"\"\r\n}"
    headers = {
        'auth_token': "{}".format(authtoken),
        'Content-Type': "application/json,application/json; charset=utf-8",
        'client_key': "brainbaazi"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    if json.loads(response.text)["message"] == "#TMK error category":
        return await client.say("Number is already used.")
    else:
        pass
    await client.say("**Your life has been send successfully.**")


client.run("NTQ0MTE4Mzk3MzQ0OTQwMDM1.D0aTpw.TszneH9RTYNkSu6lwA6i-NiIjas")