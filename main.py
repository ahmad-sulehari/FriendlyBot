import discord
import os, requests, json, random, urllib.parse as parse
from replit import db
from keep_alive import keep_alive


client = discord.Client() # client is a connection to discord

sad_words = ['awful', 'sad', 'dreadful', 'unhappy', 'miserable']

starter_engcouragements = ['Hang in there!', 'Cheer up!', 'your awesome don\'t forget that']

if "responding" not in db.keys():
  db['responding'] = True



def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragement(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]


def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements


@client.event # to register an event
async def on_ready(): # call back function
  print("we are logged in as {0.user}".format(client))

#these function name are from discord .py library

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  if db['responding']:
    options = starter_engcouragements

    if "encouragements" in db.keys():
      options += db['encouragements']

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)
  

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragement(encouraging_message)
    await message.channel.send("New encouraging message added!")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del ",1)[1])
      delete_encouragement(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)
  
  if msg.startswith("$resp"):
    value = msg.split("$resp ",1)[1]
    if value.lower() == "true":
      db['responding'] = True
      await message.channel.send("Responding is on.")
    else:
      db['responding'] = False
      await message.channel.send("Responding is off.")
  
  if msg.startswith("!"):
    embd_url = get_gif_url(msg)
    await message.channel.send(embd_url)

  elif any(word.startswith("!") for word in msg.split()):
    for word in msg.split():
      if word.startswith("!"):
        await message.channel.send(get_gif_url(word[1:]))
        break

def get_gif_url(phrase):
  
  url = "https://api.giphy.com/v1/gifs/search"
  
  params = { "api_key": "fDii9zmzvFEMRnBtDAkDA96HxTc6hfhl", "q": phrase, "limit": "25", "offset": "0", "rating": "g", "lang": "en"}
  
  request_url = url + "?" + parse.urlencode(params)

  response = requests.request("GET", request_url)

  return response.json()["data"][random.randint(1,26)]["embed_url"]


keep_alive()
# to run the bot
client.run(os.getenv('TOKEN'))
