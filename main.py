import discord

import os

from dotenv import load_dotenv
# Loads the .env file that resides on the same level as the script.
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    guild_count = 0

    async for guild in bot.fetch_guilds(limit=100):
        print(guild.name)

        guild_count += 1

    print ("Clip Manager is in " + str(guild_count) + " guilds")


@bot.event

async def on_message(message):
    if message.content == "testing":
        await message.channel.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    

bot.run(DISCORD_TOKEN)



