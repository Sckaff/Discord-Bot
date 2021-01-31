import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

if "respond" not in db.keys():
  db["respond"] = True

sad_words = ["sad", "angry", "depressed", "ódio", "odeio", "ajuda","alguém"]

start_encouragement = [
  "Você será mais forte do que pensa e será mais feliz do que imagina.",
  "Você vai vencer, mas antes, Deus vai lhe ensinar a ser forte",
  "Sua arma é a oração!",
  "Sua armadura é a palavra de Deus!",
  "Seu advogado é Jesus!"
  ]

def get_quote():
  response = requests.get("http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "\"" + json_data[0]['q'] + "\"" + " -" + json_data[0]['a']
  return(quote)

def update_encouragement(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"] 
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]

  if len(encouragements) > index:
    del encouragements[index]

  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith('$hello'):
    await message.channel.send("Hello!")

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["respond"]:  
    options = start_encouragement
    if "encouragements" in db.keys():
      options = start_encouragement + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith('$list'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith('$new '):
    encouraging_message = msg.split("$new ", 1)[1] 
    update_encouragement(encouraging_message)
    await message.channel.send("\"" + encouraging_message + "\" " + " adicionado(a) à lista!")

  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]

    await message.channel.send(encouragements)

  if msg.startswith('$respond '):
    status = msg.split('$respond ',1)[1]

    if status.lower() == 'true':
      db["respond"] = True
      await message.channel.send("Dale, tô aqui pra alegrar")

    if status.lower() == 'false':
      db["respond"] = False
      await message.channel.send("Deboas, parei.")

keep_alive()
client.run(os.getenv('TOKEN'))