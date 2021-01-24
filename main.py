import discord
import os
import requests 
import json
import random
import joke_api
from replit import db
from keep_alive import keep_alive

client=discord.Client()

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    #checks if there is already a column named encouragements in db if yes it appends the message and updates the db else it creates a coulmn and adds
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
  else:
    db["encouragements"]=[encouraging_message]

def get_quote():
  response=requests.get('https://zenquotes.io/api/random')
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+ " -" + json_data[0]['a']
  return(quote)

def get_weather(city):
  response=requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city,os.getenv('Api_key')))
  data=response.json()
  return(data)

sad_words=["sad","goodbye","lonely","regrets","depressed","angry","suicide","depressing",    "bitter","dismal","heartbroken","melancholy","pessimistic","somber","sorry","wistful"]

starter_encouragements=["Chal zyada nautanki mat maar,kuch nhi hua h tuhje",
"Hang in there buddy! Bas 40 saal ki baat h phir tu bhi mukht aur duniya bhi terese mukht ;)","Tu aacha aadmi h ,seh le thoda!",
"Yeh Duniya baadi zaalim h mere dost ,thoda adjust kar sab changa ho jaayega:)","Tu hai hi isi layak","Tushar ke saath thoda ghuma kar sab thik ho jaayega,mast aadmi h woh","Chal jhutha ","Paaji kadha has bhi liya karo"]

if "responding"  not in db.keys():
  db["responding"]=True


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if (message.author == client.user):
      return

    msg=message.content

    if(msg.startswith('$hello')):
      await message.channel.send('Hello Paaji! Hows the josh ?')

    if(msg.startswith('$inspire')):
      quote=get_quote()
      await message.channel.send(quote)
    
    if db["responding"]:
      options=starter_encouragements
      if "encouragements" in db.keys():
        options=options+db["encouragements"]
      
      if(any(word in msg for word in sad_words)):
        await message.channel.send(random.choice(options))

    if(msg.startswith("$add")):
      encouraging_message=msg.split("$add ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("Happy hojaao,message add hogya h aapka!")

    if(msg.startswith("$responding")):
      value=msg.split("$responding ",1)[1]
      if(value.lower() =="false"):
        db["responding"]=False
        await message.channel.send("Bye bye tata sab khatam")
      else:
        db["responding"]=True
        await message.channel.send("Guru  lo hogya mein shuru")

    if message.content.startswith('$joke'):
        joke = joke_api.get_joke()
        # print(joke)

        if joke == False:
            await message.channel.send("Couldn't get joke from API. Try again later.")
        else:
            await message.channel.send(f"**{joke['setup']}**\n\n ||{joke['punchline']}||")

    if(msg.startswith('$weather')):
      city=msg.split("$weather ",1)[1]
      weather=get_weather(city)
      await message.channel.send(weather["coord"])
      await message.channel.send(weather["main"])
       

keep_alive()

client.run(os.getenv('Token'));