import discord
from discord.ext import commands
from flask import Flask, request
import threading
import asyncio

# Configuration du bot Discord
bot_token = 'MTA5Njc3ODY5MDY5MzcxNDAzMQ.GwcULP.c-K8vpohiw4ZlTTdto1dMG1UpQ9K84rn6jQ-Qc'  # Remplacez par le jeton de votre bot Discord
channel_id = 1118691939429126175  # Remplacez par l'ID du canal Discord dans lequel envoyer les messages

# Création du client Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration de l'API Flask
app = Flask(__name__)

# Route pour recevoir la requête "log"
@app.route('/log', methods=['POST'])
def log_message():
    if 'log' in request.form:
        message = request.form['log']
        send_discord_message(message)
        return 'Log message sent to Discord!'
    else:
        return 'No log message provided.'

# Fonction pour envoyer un message dans le canal Discord
def send_discord_message(message):
    channel = bot.get_channel(channel_id)
    if channel:
        asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)

# Événement lorsque le bot Discord est prêt
@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

# Fonction pour lancer le bot Discord dans un thread
def run_discord_bot():
    bot.run(bot_token)

# Lancement du bot Discord dans un thread
discord_thread = threading.Thread(target=run_discord_bot)
discord_thread.start()

# Lancement de l'API Flask dans le thread principal
app.run()
