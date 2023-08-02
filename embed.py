import discord 
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import boto3
import os
from datetime import datetime


load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)




@bot.command()
async def create_embed(ctx, userID, username, numClips, clips, page):
    embed_title = ctx.author.nickname + "'s Clips!"
    embed = discord.Embed(title=embed_title,
                      colour=0x00b0f4,
                      timestamp=datetime.now())

    embed.set_author(name="Clip Manager")
    start_val = page-1*5
    end_val = start_val + 5

    for i in range(start_val, end_val):
        embed.add_field(name="Clip "+str(i+1)+": " +clips[i]["title"],
                value=clips[i]['link'])

    embed.set_thumbnail(url="https://i.pinimg.com/564x/8e/3e/ff/8e3eff7aa6f1147fabcc866666a6c22c.jpg")

    embed.set_footer(text="10/10 Bot",
                    icon_url="https://slate.dan.onl/slate.png")

    await ctx.send(embed=embed)


    bot.run(DISCORD_TOKEN)
